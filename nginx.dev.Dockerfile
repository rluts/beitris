FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
ADD nginx/conf/dev/nginx.conf /etc/nginx/conf.d