FROM ubuntu:16.04
RUN sed -i s@/archive.ubuntu.com/@/mirrors.tencentyun.com/@g /etc/apt/sources.list
# RUN sed -i 's/archive.ubuntu.com/asia-east1.gce.archive.ubuntu.com/g' /etc/apt/sources.list
RUN apt-get update \ 
    && apt-get install -y sudo zip vim unzip wget curl openssh-server software-properties-common postgresql-client postgresql python-psycopg2 libpq-dev\
    && apt install -y python-pip && pip install --upgrade pip && python -m pip install pip==9.0.3 && pip2 install setuptools && apt-get install -y libmysqlclient-dev && apt install -y gcc && apt install -y python-dev && pip2 install netifaces requests \
    &&apt-get install -y libxss1 libappindicator1 libindicator7 \ 
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m web
COPY ./conf /conf
COPY ./home/ctf/blog /home/web/blog
RUN chmod -R 700 /conf && chown -R web:web /home/web && pip install -r /home/web/blog/requirements.txt
WORKDIR /home/web

EXPOSE 8000
EXPOSE 22

CMD ['/conf/service.sh']