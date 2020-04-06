import os, uuid, subprocess, logging, time, subprocess
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
        try:
            configs = DBUtils.get_all_configs()
            basedir = os.path.dirname(__file__)
            challenge = DynamicCheckChallenge.query.filter_by(id=challenge_id).first_or_404()
            port = str(int(configs.get("frp_direct_port_minimum")) + int(user_id))
            flag = DockerUtils.gen_flag()
            socket = DockerUtils.get_socket()
            sname = os.path.join(basedir, "source/" + challenge.dirname)
            dirname = challenge.dirname.split("/")[1]
            name = "User{}_{}".format(user_id,dirname)
            dname = os.path.join(basedir, "source/run/" + name)
        except Exception as e:
            return e

        try:
            command = "cp -r {} {}".format(sname, dname)
            process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # sed port
            command = "cd {} && echo '{}' > flag && sed 's/9999/{}/g' docker-compose.yml > run.yml".format(dname, flag, port)
            process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # up docker-compose
            command = "cd " + dname + " && docker-compose -H={} -f run.yml up -d".format(socket)
            process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log(
                "owl",
                '[{date}] {name} {msg}',
                msg=name + " up."
            )
            docker_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, name)).replace("-", "")
            return docker_id, port, flag, challenge.redirect_type
        except subprocess.CalledProcessError as e:
            log("owl",
                'Stdout: {out}\nStderr: {err}',
                out=e.stdout.decode(),
                err=e.stderr.decode()
            )
            return e.stderr.decode()


    @staticmethod
    def down_docker_compose(user_id, challenge_id):
        try:
            basedir = os.path.dirname(__file__)
            socket = DockerUtils.get_socket()
            challenge = DynamicCheckChallenge.query.filter_by(id=challenge_id).first_or_404()
            dirname = challenge.dirname.split("/")[1]
            name = "User{}_{}".format(user_id, dirname)
            dname = os.path.join(basedir, "source/run/" + name)
        except Exception as e:
            return str(e)

        try:
            command = "cd {} && docker-compose -H={} -f run.yml down".format(dname, socket)
            process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            command = "rm -rf {}".format(dname)
            process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            msg = name + " down."
            log(
                "owl",
                "[{date}] {name} {msg}",
                msg=msg,
            )
            return True
        except subprocess.CalledProcessError as e:
            return str(e.stderr.decode())

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