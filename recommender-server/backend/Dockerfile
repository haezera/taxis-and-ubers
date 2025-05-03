FROM node:20
WORKDIR /backend
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8761
CMD ["npm", "start"]