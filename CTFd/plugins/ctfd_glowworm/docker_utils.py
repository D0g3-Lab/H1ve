import os, uuid, subprocess, logging, time, re
from .db_utils import DBUtils
from CTFd import utils
from .models import ADAChallenge, GlowwormContainers, GlowwormCheckLog, GlowwormAttacks
from .extensions import get_round
from CTFd.utils.logging import log
from CTFd.models import db, Users, Teams
from .extensions import get_mode, teampasswd

class DockerUtils:
    @staticmethod
    def get_socket():
        configs = DBUtils.get_all_configs()
        socket = configs.get("docker_api_url")
        return socket

    @staticmethod
    def init_teams(counts):
        platform_name = utils.get_config("ctf_name")
        print(platform_name)
        basePath = os.path.abspath(os.path.dirname(__file__))
        platformDir = os.path.join(basePath, platform_name)
        print(platformDir)

        try:
            for index in counts:
                if not isinstance(index, Teams):
                    if index.type == "admin":
                        pass

                teamDir = os.path.join(basePath, platform_name, 'team' + str(index.id))
                print(teamDir)
                if (os.path.exists(platformDir) == False):
                    os.mkdir(platformDir)
                    os.mkdir(teamDir)
                elif (os.path.exists(teamDir) == False):
                    os.mkdir(teamDir)
            return True
        except Exception as e:
            return False

    @staticmethod
    def check_env(challenge_id):
        from .schedule import scheduler
        with scheduler.app.app_context():
            try:
                mode = utils.get_config("user_mode")
                platform_name = utils.get_config("ctf_name")
                basePath = os.path.abspath(os.path.dirname(__file__))
                platformDir = os.path.join(basePath, platform_name)
                challenge = ADAChallenge.query.filter_by(id=challenge_id).first_or_404()
                dirname = challenge.dirname.split("/")[1]
                containers = GlowwormContainers.query.filter_by(challenge_id=challenge_id).all()
                for index in containers:
                    if mode == "users":
                        victim = Users.query.filter_by(id=index.user_id).first()
                        victim_name = victim.name
                        victim_id = victim.id
                        team_id = victim.team_id if victim.team_id else None
                    else:
                        victim = None
                        team = Teams.query.filter_by(id=index.user_id).first()
                        team_id = team.id
                        victim_id = team_id
                        victim_name = team.name

                    check_file = os.path.join(basePath, challenge.dirname, "conf", "check.py")
                    # Todo: excute check file in containers
                    command = "python3 '%s' %s %s" % (check_file, index.ip, index.service_port)
                    print(command)
                    # 容器Check
                    rq = os.popen(command).read()
                    r = "".join(re.findall(r'team..', rq))
                    if r == "":
                        msg = index.docker_id + " seems ok."
                    else:
                        msg = index.docker_id + " seems down."
                        check_log = GlowwormCheckLog(
                            user_id=victim_id,
                            team_id=team_id,
                            victim_user_id=victim_id,
                            victim_team_id=team_id,
                            challenge_id=challenge.id,
                            ip="127.0.0.1",
                            provided=msg,
                        )
                        check = GlowwormAttacks(
                            attack_id=None,
                            attack_name=None,
                            victim_id=victim_id,
                            victim_name=victim_name,
                            docker_id=index.docker_id,
                            envname=index.docker_id.split("_", 1)[1],
                            flag="",
                            round=get_round()
                        )
                        db.session.add(check)
                        db.session.add(check_log)
                        print(check)
                        print(check_log)
                    print(msg)
                db.session.commit()
                db.session.close()
                return True
            except Exception as e:
                print(e)
                return False

    @staticmethod
    def build_env(challenge_id):
        platform_name = utils.get_config("ctf_name")
        print(platform_name)
        basePath = os.path.abspath(os.path.dirname(__file__))
        platformDir = os.path.join(basePath, platform_name)
        challenge = ADAChallenge.query.filter_by(id=challenge_id).first_or_404()
        envPath = os.path.join(basePath, challenge.dirname)
        command = 'cd ' + envPath + ' && docker build -f ' + envPath + '/Dockerfile -t ' + challenge.image_name + " ."
        print(command)
        try:
            os.system(command)
            return True
        except Exception as e:
            print(e)
            return str(e)

    @staticmethod
    def gen_env(language="PHP", rootpasswd="", teamPath="", key="", teamid="", interval=300):

        # "*/5 * * * * python /conf/flag.py team3_web_pyblog Unknow2Kg 300"
        # f = "*/5 * * * * python /conf/flag.py %s %s %s"
        # echo ${f:12}
        service = {}
        # PHP
        service['PHP'] = '''#!/bin/bash
echo web:%s | chpasswd;
echo root:%s | chpasswd;
chmod -R 700 /conf
chown -R web:web /var/www/html
chmod -R 777 /var/www/html

if [ -f "/conf/apache2.sh" ]; then 
    chmod +x /conf/apache2.sh
    /conf/apache2.sh
fi
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld
service mysql start;
/etc/init.d/ssh start;
sleep 2
mysql -u root  < /var/www/html/*.sql

if [ -f "/conf/extra.sh" ]; then 
    chmod +x /conf/extra.sh
    /conf/extra.sh
fi

f="*/5 * * * * python /conf/flag.py %s %s %s"
echo `${f:12}`
echo "$f" > /conf/cron.txt
crontab /conf/cron.txt
cron
/bin/bash
'''
        # PWN
        service['PWN'] = '''#!/bin/sh
echo pwn:%s | chpasswd;
echo root:%s | chpasswd;
chmod -R 700 /conf
f="*/5 * * * * python /conf/flag.py %s %s %s"
# echo `${f:12}`
echo "$f" > /conf/cron.txt
crontab /conf/cron.txt
cron
if [ -f "/conf/extra.sh" ]; then 
    chmod +x /conf/extra.sh
    /conf/extra.sh
fi
'''

        # Django
        service['Django'] = '''#!/bin/bash
echo web:%s | chpasswd;
echo root:%s | chpasswd;
chmod -R 700 /conf
/etc/init.d/ssh start;

f="*/5 * * * * python /conf/flag.py %s %s %s"
echo `${f:12}`
echo "$f" > /conf/cron.txt
crontab /conf/cron.txt
cron
if [ -f "/conf/extra.sh" ]; then 
    chmod +x /conf/extra.sh
    /conf/extra.sh
fi
/bin/bash
'''

        # Node
        service['Node'] = '''#!/bin/bash
echo web:%s | chpasswd;
echo root:%s | chpasswd;
chmod -R 700 /conf
/etc/init.d/ssh start;

f="*/5 * * * * python /conf/flag.py %s %s %s"
echo `${f:12}`
echo "$f" > /conf/cron.txt
crontab /conf/cron.txt
cron
if [ -f "/conf/extra.sh" ]; then 
    chmod +x /conf/extra.sh
    /conf/extra.sh
fi
/bin/bash
'''

        webpasswd = teampasswd(key)
        servicesh = service[language] % (webpasswd, rootpasswd, key, teamid, interval)
        print(servicesh)
        with open(os.path.join(teamPath, "conf", "service.sh"), 'w') as f:
            f.write(servicesh)
        return webpasswd

    @staticmethod
    def copy_env(source, dest):
        try:
            if not (os.path.exists(dest)):
                # TODO: 重构
                os.system("mkdir -p %s" % dest)
                command = 'cp -r "%s" "%s"' % (source, dest)
                print(command)
                os.system(command)
                return True
            else:
                command = 'cp -r "%s" "%s"' % (source, dest)
                print(command)
                os.system(command)
                return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_env(counts, challenge_id):
        try:
            mode = utils.get_config("user_mode")
            platform_name = utils.get_config("ctf_name")
            basePath = os.path.abspath(os.path.dirname(__file__))
            platformDir = os.path.join(basePath, platform_name)
            challenge = ADAChallenge.query.filter_by(id=challenge_id).first_or_404()
            for index in counts:
                if mode == "users" and index.type == "admin":
                    pass
                else:
                    dirname = challenge.dirname.split("/")[1]
                    envPath = os.path.join(basePath, challenge.dirname)
                    teamDir = os.path.join(basePath, platform_name, 'team' + str(index.id))
                    teamEnvDir = os.path.join(teamDir, dirname)
                    # 容器删除
                    name =  "Team{}_{}".format(str(index.id), dirname)
                    print(name)
                    os.system("docker stop " + name)
                    os.system("docker rm " + name)
                    instance = GlowwormContainers.query.filter_by(docker_id=name).first()
                    if instance == None:
                        pass
                    else:
                        db.session.delete(instance)
                        db.session.commit()
                    # 目录删除
                    command = "rm -rf '%s'" % teamEnvDir
                    print(command)
                    os.system(command)
            challenge.env_status = False
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def run_env(counts, challenge_id):
        try:
            configs = DBUtils.get_all_configs()
            interval = configs.get("per_round") if configs.get("per_round") else "300"
            cpu_limit = configs.get("cpu_limit") if configs.get("cpu_limit") else "0.5"
            memory_limit = configs.get("memory_limit") if configs.get("memory_limit") else "512M"
            rootpwd = configs.get("containers_key") if configs.get("containers_key") else "root"
            mode = utils.get_config("user_mode")
            platform_name = utils.get_config("ctf_name")
            basePath = os.path.abspath(os.path.dirname(__file__))
            platformDir = os.path.join(basePath, platform_name)
            challenge = ADAChallenge.query.filter_by(id=challenge_id).first_or_404()
            for index in counts:
                if mode == "users" and index.type == "admin":
                    pass
                else:
                    dirname = challenge.dirname.split("/")[1]
                    envPath = os.path.join(basePath, challenge.dirname)
                    teamDir = os.path.join(basePath, platform_name, 'team' + str(index.id))
                    teamEnvDir = os.path.join(teamDir, dirname)
                    name = "Team{}_{}".format(str(index.id), dirname)
                    # 目录复制
                    DockerUtils.copy_env(envPath, teamDir)
                    # 容器动态信息初始化
                    # save random key
                    key = str(uuid.uuid3(uuid.UUID(str(uuid.uuid1())), platform_name + str(time.time())))
                    print(key)
                    instance_pwd = DockerUtils.gen_env(language=challenge.env_language, rootpasswd=rootpwd, teamPath=teamEnvDir, key=key, teamid=name, interval=interval)
                    # choose alive random port
                    if configs.get("random_port") == "1":
                        fixedPorts = DBUtils.get_alive_ports()
                        insert_service_port = fixedPorts[0]
                        insert_ssh_port = fixedPorts[1]
                    else:
                        fixedPorts = 100 * int(challenge.id)
                        insert_service_port = int(str(fixedPorts + index.id) + "80")
                        insert_ssh_port = int(str(fixedPorts + index.id) + "22")
                    env_port = challenge.env_port if challenge.env_port != "" else "80"
                    confPath = os.path.join(teamEnvDir, "conf")

                    instance = GlowwormContainers(
                        user_id=index.id
                        , challenge_id=challenge_id
                        , docker_id=name
                        , ip=configs.get("direct_address")
                        , service_port=insert_service_port
                        , ssh_port=insert_ssh_port
                        , ssh_key=instance_pwd
                        , key=key
                    )
                    db.session.add(instance)
                    db.session.commit()
                    command = """#!/bin/sh
    docker run -tid --restart=on-failure:10 --privileged --name %s --cpus=%s -m %s -v "%s":"%s" -p %s:%s -p %s:%s --network h1ve_frp_containers %s "/conf/service.sh"
    """ % ( name, cpu_limit, memory_limit, confPath, "/conf", insert_service_port, env_port, insert_ssh_port, "22", challenge.image_name)
                    print(command)
                    with open(os.path.join(confPath, "docker.sh"), 'w') as f:
                        f.write(command)
                    # 启动容器
                    command = 'cd "%s" && chmod +x ./docker.sh service.sh && ./docker.sh' % confPath
                    print(command)
                    try:
                        os.system(command)
                        msg = name + " up."
                        log(
                            "glowworm",
                            "[{date}] {name} {msg}",
                            msg=msg,
                        )

                    except Exception as e:
                        # print(e)
                        msg = name + " up error." + str(e)
                        log(
                            "glowworm",
                            "[{date}] {name} {msg}",
                            msg=msg,
                        )
                        return str(e)
            challenge.env_status = True
            db.session.commit()
            return True
        except Exception as e:
            return str(e)
