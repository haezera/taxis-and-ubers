import express, { Request, Response } from 'express';
import errorHandler from 'middleware-http-errors';
import { MicroserviceClient } from './microservice_client'
import 'dotenv/config'

// initialise dotenv
require('dotenv').config()

const SERVER_PORT = Number(process.env.BACKEND_PORT);
const SERVER_HOST = String(process.env.BACKEND_HOST);
const MICROSERVICE_PORT = Number(process.env.MICROSERVICE_PORT);
const MICROSERVICE_HOST = String(process.env.MICROSERVICE_HOST);

// connect to microservice
console.log('Connecting to microservice...')
const microservice = new MicroserviceClient(MICROSERVICE_HOST, MICROSERVICE_PORT);
microservice.connect()

const app = express();

app.get('/', (req: Request, res: Response) => {

});

app.get('/v1/auth/user/create', (req: Request, res: Response) => {

});

app.get('/v1/auth/driver/create', (req: Request, res: Response) => {

});

// server setup
app.use(errorHandler());

const server = app.listen(SERVER_PORT, SERVER_HOST, () => {
  console.log(`⚡️ Server started on port ${SERVER_PORT} at ${SERVER_HOST}`);
});

process.on('SIGINT', () => {
  server.close(() => console.log('Shutting down server gracefully.'));
});

