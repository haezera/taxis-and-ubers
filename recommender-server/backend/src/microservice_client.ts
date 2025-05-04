// TypeScript client for Python modelling microservice

import * as net from "net";
import { json } from "stream/consumers";
import 'dotenv/config'

// initialise dotenv
require('dotenv').config()

const DATABASE_NAME = String(process.env.DATABASE_NAME)
const DATABASE_HOST = String(process.env.DATABASE_HOST)
const DATABASE_PORT = Number(process.env.DATABASE_PORT)
const DATABASE_USERNAME = String(process.env.DATABASE_USERNAME)
const DATABASE_PASSWORD = String(process.env.DATABASE_PASSWORD)

interface PredictionResponse {
    type: string;
    prediction: number;
    expected_revenue: number;
}

interface MessageResponse {
    type: string;
    msg: string;
}

export class MicroserviceClient {
    private socket: net.Socket;
    private port: number;
    private host: string;

    constructor(host: string, port: number) {
        this.host = host;
        this.port = port;
        this.socket = new net.Socket();
    }

    public async connect(): Promise<void> {
        return new Promise((resolve, reject) => {
            this.socket.connect(this.port, this.host, async () => {
                console.log(`Connected to server at ${this.host}:${this.port}`);
    
                try {
                    const reply = await this.initiation();
                    console.log("Server reply: ", reply.type);
                    resolve();
                } catch (err) {
                    console.error("Error during initiation:", err);
                    this.disconnect();
                    reject(err);
                }
            });
    
            this.socket.on("error", (err) => {
                console.log("Error occurred in microservice: ", err.toString());
                reject(err);
            });
        });
    }

    public async initiation(): Promise<MessageResponse> {
        return new Promise((resolve, reject) => {
            this.socket.once("data", (data) => {
                resolve(JSON.parse(data.toString()));
            });

            this.socket.once("error", (err) => {
                reject(err);
            });
            
            this.socket.write(JSON.stringify({
                'type': 'INIT',
                'tr_start': '2023-01-01',
                'tr_end': '2024-01-01',
                'db_name': DATABASE_NAME,
                'db_host': DATABASE_HOST,
                'db_port': DATABASE_HOST,
                'db_username': DATABASE_USERNAME,
                'db_password': DATABASE_PASSWORD
            }));
        })
    }

    public async predict(trip_distance: number, datetime: string): Promise<PredictionResponse> {
        return new Promise((resolve, reject) => {
            this.socket.once("data", (data) => {
                resolve(JSON.parse(data.toString()));
            });

            this.socket.once("error", (err) => {
                reject(err);
            });

            this.socket.write(JSON.stringify({
                'type': 'PRED',
                'trip_distance': trip_distance,
                'datetime': datetime
            }));
        })
    }

    public disconnect(): void {
        this.socket.end();
    }
}


/*
const host: string = process.argv[2]
const port = Number(process.argv[3])

async function runClient() {
    const client = new MicroserviceClient(host, port);
    await client.connect(); // now we can make connect() async and await inside

    try {
        const prediction = await client.predict(15.4, '2023-04-04T14:11:00+11');
        console.log("Prediction result:", prediction);
    } catch (err) {
        console.error("Prediction failed:", err);
    }
}

runClient();
*/
