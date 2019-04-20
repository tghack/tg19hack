FROM node:11

RUN apt-get update && apt-get install -y sqlite3

USER node
RUN mkdir -p /home/node/database
RUN mkdir -p /home/node/app
#RUN mkdir -p /home/node/app/node_modules

# create sqlite database
COPY database/wands.sqlite /home/node/database/wands.sqlite
RUN sqlite3 /home/node/database/wands.db < /home/node/database/wands.sqlite

# clean up sqlite file
RUN rm /home/node/database/wands.sqlite

COPY ./app /home/node/app/
#COPY ./app/package*.json /home/node/app/
WORKDIR /home/node/app/
USER root
RUN chown -R node /home/node
USER node
RUN npm install
EXPOSE 4001

CMD node server.js

