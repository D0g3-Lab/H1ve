FROM php:5.5-apache


# Install dependencies

RUN echo "deb http://mirrors.ustc.edu.cn/debian/ stretch main non-free contrib" > /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/debian/ stretch-updates main non-free contrib" >> /etc/apt/sources.list  && \
    echo "deb http://mirrors.ustc.edu.cn/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.ustc.edu.cn/debian/ stretch main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.ustc.edu.cn/debian/ stretch-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.ustc.edu.cn/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/debian-security/ stretch/updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.ustc.edu.cn/debian-security/ stretch/updates main non-free contrib" >> /etc/apt/sources.list
    
RUN apt-get update && apt-get install -y wget curl && apt-get clean

ENV APACHE_RUN_USER  www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR   /var/log/apache2
ENV APACHE_PID_FILE  /var/run/apache2/apache2.pid
ENV APACHE_RUN_DIR   /var/run/apache2
ENV APACHE_LOCK_DIR  /var/lock/apache2
ENV APACHE_LOG_DIR   /var/log/apache2

RUN mkdir -p $APACHE_RUN_DIR
RUN mkdir -p $APACHE_LOCK_DIR
RUN mkdir -p $APACHE_LOG_DIR
# Copy files
COPY ./html /var/www/html

RUN chmod -R 777 /var/www/html/uploads/ 

# Setting workdir for docker
WORKDIR /var/www/html

# Exposing Apache port to host
EXPOSE 80

CMD ["/usr/sbin/apache2", "-D",  "FOREGROUND"]