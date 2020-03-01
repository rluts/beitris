FROM node:latest as build

WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn
COPY frontend/ ./
RUN yarn build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
ADD nginx/conf/prod/nginx.conf /etc/nginx/conf.d