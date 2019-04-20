FROM ubuntu:18.04
RUN apt update && apt upgrade -y && apt install -y nginx php7.2-fpm

COPY startup.sh /startup.sh
RUN rm /etc/nginx/sites-enabled/*
COPY nginx_site.conf /etc/nginx/sites-enabled/

RUN rm /var/www/html/*
COPY src/ /var/www/html/
COPY flag.txt /var/www/html/
RUN mkdir /var/www/html/uploads
RUN chown www-data:www-data /var/www/html/uploads

EXPOSE 8080
CMD ["/startup.sh"]
