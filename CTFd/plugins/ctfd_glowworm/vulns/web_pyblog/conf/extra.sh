#!/bin/bash
echo postgres:postgres | chpasswd;
/etc/init.d/postgresql start;
# a=`python -c "import random,string; print ''.join(random.sample(string.ascii_letters + string.digits, 16))"`
# echo $a;
# sed -i "s/blog123456/$a/g" /home/web/blog/django_blog/settings.py
sleep 2;
sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"
sudo -u postgres psql -U postgres -d postgres -c "CREATE USER blog WITH PASSWORD 'blog123456';"
sudo -u postgres psql -U postgres -d postgres -c "create database blog with owner blog;"
sudo -u postgres psql -U postgres -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE blog TO blog;"

sleep 2;
export PGPASSWORD='postgres'
psql -U postgres -h 127.0.0.1 -p 5432 -d blog < /home/web/blog/blog.sql;
sudo -u web nohup python /home/web/blog/manage.py runserver 0.0.0.0:8000 >> /home/web/blog/log.txt 2>&1 &