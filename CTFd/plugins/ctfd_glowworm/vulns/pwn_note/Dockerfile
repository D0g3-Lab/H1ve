FROM ubuntu:16.04

# set source download and install xinted
RUN apt update && apt-get install -y lib32z1 xinetd ssh python2.7 && apt-get install -y python-pip && pip install --upgrade pip && python -m pip install pip==9.0.3 && pip2 install setuptools && apt-get install libmysqlclient-dev -y && apt-get install -y gcc && apt-get install -y python-dev && pip2 install requests && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*

COPY ./conf /conf

COPY ./pwn.xinetd /etc/xinetd.d/pwn

# useradd and put flag(random)
RUN useradd -m pwn && echo 'flag{{flag is good}}' > /home/pwn/flag

# copy bin
COPY ./bin/pwn /home/pwn/pwn
COPY ./binsh/sh /home/pwn/bin/sh
COPY ./binsh/cat /home/pwn/bin/cat
COPY ./binsh/ls /home/pwn/bin/ls


# chown & chmod
RUN chown -R root:pwn /home/pwn && chmod -R 750 /home/pwn && chmod 770 /home/pwn/pwn && chmod 740 /home/pwn/flag && chmod -R 700 /conf

# copy lib,/bin 
RUN cp -R /lib* /home/pwn && mkdir /home/pwn/dev && mknod /home/pwn/dev/null c 1 3 && mknod /home/pwn/dev/zero c 1 5 && mknod /home/pwn/dev/random c 1 8 && mknod /home/pwn/dev/urandom c 1 9 && chmod 666 /home/pwn/dev/* 

#change passwd
# RUN echo pwn:1q2q3q4q | chpasswd && echo root:spr1ng | chpasswd

RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

#chroot
# RUN sed -i '$a#define username to apply chroot jail to\nMatch User pwn\n#specify chroot jail\nChrootDirectory /home/pwn' /etc/ssh/sshd_config

CMD ["/conf/service.sh"]
