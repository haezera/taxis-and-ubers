import pandas as pd
import numpy as np
from socket import socket, SOCK_STREAM, AF_INET, timeout
from classes import fare_model, tips_model, congestion_model, data_monolith

class FareMicroservice:
    """
    TCP server which implements custom application layer protocol.
    The server starts with no classes loaded. A 'initiation' message
    is required to begin the microservice from the backend. 

    The 'initiation' message contains information about the desired
    training window, which is then used to pull data into the DataMonolith.
    An example initiation message is:
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
        self.server.bind((host, port))

    def packet_parse(self, msg:str) -> dict:
        lines = msg.strip().split('\n')
        result = {'type': lines[0]}

        for line in lines[1:]:
            if line.strip() == 'END': break
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = value.strip()

        return result
    
    def initiation(self, packet: dict):
        # Get required variables
        db_name = packet['Database Name']
        db_host = packet['Database Host']
        db_port = packet['Database Port']
        db_uname = packet['Database Username']
        db_password = packet['Database Password']
        start_date = packet['Training Start']
        end_date = packet['Training End']

        print('Pulling data...')
        self.data = data_monolith.DataMonolith(db_host, db_port, db_uname, db_password, db_name)
        self.data.pull_date_range(start_date, end_date)

        # instantiate the models
        print('Fitting models...')
        self.tips = tips_model.TipsModel(self.data.return_columns(['trip_distance','tip_amount']))
        self.fares = fare_model.FareModel(self.data.return_columns(['trip_distance', 'fare_amount']))
        self.congestion = congestion_model.CongestionModel(self.data.data)

        # fit the models
        self.tips.fit()
        self.fares.fit()
        self.congestion.fit()

    def packet_action(self, packet: dict):
        if packet['type'] == 'INIT': 
            self.initiation(packet)

    def start_server(self):
        print('Starting server...')
        try:
            self.server.settimeout(10)
            self.server.listen()

            conn, addr = self.server.accept()
            with conn:
                print(f'Connection from {addr}')
                data = conn.recv(1024)
                msg = data.decode()
                packet = self.packet_parse(msg)
                self.packet_action(packet)
        except timeout:
            print(f'Request timed out.')
        except Exception as e:
            print(e)

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

