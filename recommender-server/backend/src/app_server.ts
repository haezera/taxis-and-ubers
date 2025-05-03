import express, { Request, Response } from 'express';
import errorHandler from 'middleware-http-errors';
import { MicroserviceClient } from './microservice_client'
import { verifyPassword, hashPassword } from './utils';
import 'dotenv/config'

// initialise dotenv
require('dotenv').config()

const SERVER_PORT = Number(process.env.BACKEND_PORT);
const SERVER_HOST = String(process.env.BACKEND_HOST);
const MICROSERVICE_PORT = Number(process.env.MICROSERVICE_PORT);
const MICROSERVICE_HOST = String(process.env.MICROSERVICE_HOST);
console.log(MICROSERVICE_HOST)

// connect to microservice
console.log('Connecting to microservice...')
const microservice = new MicroserviceClient(MICROSERVICE_HOST, MICROSERVICE_PORT);
microservice.connect()

const app = express();

app.get('/', (req: Request, res: Response) => {
  const response = {
    'response': 'You have reached the root!'
  };

  res.send(JSON.stringify(response));
});

/**
 * Request object:
 * {
 *  username: string,
 *  password: string,
 *  email: string
 * }
 */
app.get('/v1/auth/user/create', (req: Request, res: Response) => {
  const { username, password, email } = req.query;
  console.log(username)
  console.log(password)
  console.log(email)
});

app.get('/v1/auth/driver/create', (req: Request, res: Response) => {

});

app.get('/v1/auth/verify', (req: Request, res: Response) => {

});

// server setup
app.use(errorHandler());

const server = app.listen(SERVER_PORT, '0.0.0.0', () => {
  console.log(`⚡️ Server started on port ${SERVER_PORT} at ${SERVER_HOST}`);
});

process.on('SIGINT', () => {
  server.close(() => console.log('Shutting down server gracefully.'));
});

