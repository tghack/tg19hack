# specify the node base image with your desired version node:<version>
FROM node:11
# replace this with your application's default port
EXPOSE 2020

COPY ./src /app

WORKDIR /app
RUN npm install
ENTRYPOINT [ "node", "server.js" ]
