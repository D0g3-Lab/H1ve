#!/bin/sh
cd /var/www/html
service ssh start
a2enmod rewrite
service apache2 start
service mysql start
# python flag.py &  2>&1 1>/dev/null
useradd ctf
echo ctf:283cb6a372c0401625e8fb5c98f75585 | chpasswd
sleep 2
mysql -uroot -proot < *.sql
if [ -x "extra.sh" ]; then 
./extra.sh
fi
/bin/bash




# #!/bin/bash
# useradd ctf;
# echo ctf:123456 | chpasswd;
# # echo root:456789 | chpasswd;
# service apache2 start;
# service mysql start;
# /bin/bash;