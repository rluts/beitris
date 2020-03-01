FROM node:latest

WORKDIR /app
COPY ./package*.json ./
RUN yarn install
ENV PATH /app/node_modules/.bin:$PATH

ADD . /app
CMD yarn start
