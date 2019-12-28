#!/bin/bash
echo ctf:default | chpasswd;
echo root:root | chpasswd;

chown -R ctf:ctf /var/www/html
# chmod -R 777 /var/www/html
chmod 400 /var/www/html/upload.php
# 该文件为属主只读
chmod /conf/apache2.sh
service mysql start;
/etc/init.d/ssh start;
sleep 2
mysql -u root  < /var/www/html/*.sql

python /conf/flag.py team1 team1 300 1>/dev/null 2>&1;
/bin/bash
