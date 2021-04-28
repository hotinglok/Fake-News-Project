FROM node:16-alpine
RUN mkdir /frontend
WORKDIR /frontend
COPY package.json .
RUN npm install
COPY . .
