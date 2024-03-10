# build env
# FROM node:20.7 as build
FROM node:20.7
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
CMD cp -r build result_build
