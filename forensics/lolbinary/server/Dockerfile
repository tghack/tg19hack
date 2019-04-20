FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY get_flag /usr/share/nginx/html/
COPY conf /etc/nginx/nginx.conf
