import os, uuid, subprocess, logging, time, subprocess
from .db_utils import DBUtils
from .models import AliyunChallenge, AliyunECS
from CTFd.utils.logging import log

class ECSUtils:
    @staticmethod
    def gen_flag():
        configs = DBUtils.get_all_configs()
        prefix = configs.get("aliyun_flag_prefix")
        flag = "{" + str(uuid.uuid4()) + "}"
        flag = prefix + flag.replace("-","")
        while AliyunECS.query.filter_by(flag=flag).first() != None:
            flag = prefix + "{" + str(uuid.uuid4()) + "}"
        return flag

    @staticmethod
    def up_aliyun_ecs(user_id, challenge_id):
        try:
            configs = DBUtils.get_all_configs()
            basedir = os.path.dirname(__file__)
            challenge = AliyunChallenge.query.filter_by(id=challenge_id).first_or_404()
            flag = ECSUtils.gen_flag()
            exedir = os.path.join(basedir, "vulscript/")
            scriptName = challenge.scriptName
        except Exception as e:
            return e

        try:
            command = "cd {} && python {}.py run {}".format(exedir,scriptName,flag)
            process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = str(process.stdout, encoding="utf-8")
            if '\r\n' in data:
                lines = data.split('\r\n')
            else:
                lines = data.split('\n')

            if len(lines) == 4 and lines[2] == 'right':
                instance_id = lines[0]
                ip = lines[1]
            
            log(
                "aliyun-instance",
                '[{date}] {name} {msg}',
                msg=scriptName + " up."
            )

            return instance_id, ip, flag
        except subprocess.CalledProcessError as e:
            log("aliyun-instance",
                'Stdout: {out}\nStderr: {err}',
                out=e.stdout.decode(),
                err=e.stderr.decode()
            )
            return e.stderr.decode()



    @staticmethod
    def down_aliyun_ecs(user_id, challenge_id):
        try:
            configs = DBUtils.get_all_configs()
            basedir = os.path.dirname(__file__)
            challenge = AliyunChallenge.query.filter_by(id=challenge_id).first_or_404()
            flag = ECSUtils.gen_flag()
            exedir = os.path.join(basedir, "vulscript/")
            scriptName = challenge.scriptName

            aliyunECS = AliyunECS.query.filter_by(challenge_id=challenge_id,user_id=user_id).first_or_404()
            instance_id = aliyunECS.instance_id
        except Exception as e:
            return str(e)

        try:
            command = "cd {} && python {}.py down {}".format(exedir, scriptName, instance_id)
            # print(command)
            # print(instance_id)
            # instance_id为<AliyunECS 1>
            process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # log(
            #     "aliyun-instance",
            #     "[{date}] {name} {msg}",
            #     msg=msg,
            # )
            return True
        except subprocess.CalledProcessError as e:
            return str(e.stderr.decode())

    @staticmethod
    def remove_current_aliyun_instance(user_id, is_retry=False):
        configs = DBUtils.get_all_configs()
        instance = DBUtils.get_current_instances(user_id=user_id)

        if instance is None:
            return False
        try:
            ECSUtils.down_aliyun_ecs(user_id,challenge_id=instance.challenge_id)
            DBUtils.remove_current_instance(user_id)
            return True
        except Exception as e:
            logging.exception(e)
            print(e)
        # remove operation
            return False