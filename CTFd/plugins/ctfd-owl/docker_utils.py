import os, uuid, subprocess, logging, time
from .db_utils import DBUtils
from .models import DynamicCheckChallenge, OwlContainers
from CTFd.utils.logging import log

class DockerUtils:
    @staticmethod
    def gen_flag():
        configs = DBUtils.get_all_configs()
        prefix = configs.get("docker_flag_prefix")
        flag = "{" + str(uuid.uuid4()) + "}"
        flag = prefix + flag.replace("-","")
        while OwlContainers.query.filter_by(flag=flag).first() != None:
            flag = prefix + "{" + str(uuid.uuid4()) + "}"
        return flag

    @staticmethod
    def get_socket():
        configs = DBUtils.get_all_configs()
        socket = configs.get("docker_api_url")
        return socket

    @staticmethod
    def up_docker_compose(user_id, challenge_id):
        configs = DBUtils.get_all_configs()
        basedir = os.path.dirname(__file__)
        challenge = DynamicCheckChallenge.query.filter_by(id=challenge_id).first_or_404()
        port = str(int(configs.get("frp_direct_port_minimum")) + int(user_id))
        flag = DockerUtils.gen_flag()
        socket = DockerUtils.get_socket()
        sname = os.path.join(basedir, "source/" + challenge.dirname)
        print(sname)
        dirname = challenge.dirname.split("/")[1]
        print(dirname)
        name = "User{}_{}".format(user_id,dirname)
        dname = os.path.join(basedir, "source/run/" + name)
        command = "cp -r " + sname + " " + dname
        print(command)
        os.system(command)

        # sed port
        os.system("cd " + dname + " && echo '{0}' > flag && sed 's/9999/{1}/g' docker-compose.yml > run.yml".format(flag, port))
        print("Flag: " + flag + " && Sed Success")

        command = "cd " + dname + " && docker-compose \
-H={} -f run.yml up -d".format(socket)
        print(command)

        try:
            os.system(command)
            docker_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, name)).replace("-","")
            msg = name + " up."
            log(
                "owl",
                "[{date}] {name} {msg}",
                msg=msg,
            )
            return docker_id, port, flag, challenge.redirect_type
        except Exception as e:
            # print(e)
            msg = name + " up error." + str(e)
            log(
                "owl",
                "[{date}] {name} {msg}",
                msg=msg,
            )
            return False


    @staticmethod
    def down_docker_compose(user_id, challenge_id):
        basedir = os.path.dirname(__file__)
        socket = DockerUtils.get_socket()
        challenge = DynamicCheckChallenge.query.filter_by(id=challenge_id).first_or_404()
        dirname = challenge.dirname.split("/")[1]
        name = "User{}_{}".format(user_id, dirname)
        dname = os.path.join(basedir, "source/run/" + name)
        command = "cd " + dname + " && docker-compose \
-H={} -f run.yml down".format(socket)
        print(command)

        try:
            os.system(command)
            os.system("rm -rf " + dname)
            msg = name + " down."
            log(
                "owl",
                "[{date}] {name} {msg}",
                msg=msg,
            )
            return True
        except Exception as e:
            msg = name + " up." + str(e)
            log(
                "owl",
                "[{date}] {name} {msg}",
                msg=msg,
            )
            return False

    @staticmethod
    def remove_current_docker_container(user_id, is_retry=False):
        configs = DBUtils.get_all_configs()
        container = DBUtils.get_current_containers(user_id=user_id)

        if container is None:
            return False
        try:
            DockerUtils.down_docker_compose(user_id,challenge_id=container.challenge_id)
            DBUtils.remove_current_container(user_id)
            return True
        except Exception as e:
            print(e)
        # remove operation
            return False