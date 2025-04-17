import pandas as pd
import numpy as np
from threading import Thread
from socket import socket, SOCK_STREAM, AF_INET, timeout
from classes import fare_model, tips_model, congestion_model, data_monolith
import json

class FareMicroservice:
    """
    TCP server which implements custom application layer protocol.
    The server starts with no classes loaded. A 'initiation' message
    is required to begin the microservice from the backend. 

    The 'initiation' message contains JSON information about the desired
    training window, which is then used to pull data into the DataMonolith.
    An example initiation message is:
        {
            'type': 'INIT',
            'tr_start': '2023-06-01',
            'tr_end': '2023-07-01',
            'db_name': 'taxis_and_ubers',
            'db_host': 'localhost',
            'db_port': 5432,
            'db_username': 'haekim',
            'db_password': 'password'
        }
        INIT (message type)
        Training Start: 2023-06-01
        Training End: 2023-07-01
        Database Name: taxis_and_ubers
        Database Host: localhost
        Database Port: 5432
        Database Username: haekim
        Database Password: password 
        END
    """
    def __init__(self, host: str, port: int):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.client_threads: list[Thread] = []
        self.server.bind((host, port))
        self.is_fit = False

    def breakdown(self):
        for t in self.client_threads:
            t.join()

        self.server.close()
    
    def initiation(self, packet: dict, conn: socket):
        # Get required variables
        db_name = packet['db_name']
        db_host = packet['db_host']
        db_port = packet['db_port']
        db_uname = packet['db_username']
        db_password = packet['db_password']
        start_date = packet['tr_start']
        end_date = packet['tr_end']

        print('Pulling data')
        self.data = data_monolith.DataMonolith(db_host, db_port, db_uname, db_password, db_name)
        self.data.pull_date_range(start_date, end_date)

        # instantiate the models
        self.tips = tips_model.TipsModel(self.data.return_columns(['trip_distance','tip_amount']))
        self.tips.fit()
        self.fares = fare_model.FareModel(self.data.return_columns(['trip_distance', 'fare_amount']))
        self.fares.fit()
        self.congestion = congestion_model.CongestionModel(self.data.data)
        self.congestion.fit()

        # fit the models
        print(f'Fitting models')
        self.tips.fit()
        self.fares.fit()
        self.congestion.fit()

        conn.sendall(json.dumps({
            'type': 'ACK',
            'msg': 'Server initiation completed'         
        }).encode())

    def model_expected_fare_and_revenue(self, packet: dict, conn):
        tips = self.tips.predict(packet['trip_distance'])
        fare = self.fares.predict(packet['trip_distance'])
        congestion = self.congestion.predict(pd.to_datetime(packet['datetime']))

        conn.sendall(json.dumps({
            'type': 'ACK',
            'pred_fare': congestion * fare,
            'pred_revenue': congestion * fare + tips
        }).encode())

    def packet_action(self, packet: dict, conn: socket):
        if packet['type'] == 'INIT':
            print('Server received INIT request')
            self.initiation(packet, conn)
        elif packet['type'] == 'PRED':
            print('Server received PRED request')
            self.model_expected_fare_and_revenue(packet, conn)

    def handle_client(self, conn: socket, addr):
        while True:
            try:
                data = conn.recv(1024)
                msg = data.decode()
                packet = json.loads(msg)
                print(packet)
                self.packet_action(packet, conn)
            except ConnectionError:
                print(f'{addr} disconnected')
                return
            except Exception as e:
                print(f'{addr} experienced exception {e}')
                return

    def start_server(self):
        print('Starting server...')
        self.server.listen()
        while True:
            try:
                conn, addr = self.server.accept()
                t = Thread(target=self.handle_client, args=[conn, addr])
                t.start()

                self.client_threads.append(t)
            except KeyboardInterrupt:
                self.breakdown()
                print('Server shutting down')
                break
            except Exception as e:
                print(f'Server experienced exception {e}')

# server start

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: python3 microservice.py <host> <port>')
        exit()
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    f = FareMicroservice(host, port)
    f.start_server()

