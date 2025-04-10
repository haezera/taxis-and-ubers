// TypeScript client for Python modelling microservice

import * as net from "net";

class MicroserviceClient {
    private socket: net.Socket;
    private port: number;
    private host: string;

    constructor(host: string, port: number) {
        this.host = host;
        this.port = port;
        this.socket = new net.Socket();
    }

    public connect(): void {
        this.socket.connect(this.port, this.host, () => {
            console.log(`Connected to server at ${this.host}:${this.port}`);
        });
    }
}
