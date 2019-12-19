import time, os, json, requests, re
from CTFd.models import Challenges, Users
from CTFd import utils
from .db_utils import DBUtils
from .docker_utils import DockerUtils
from sqlalchemy.sql import and_
from flask import session

class ControlUtil:
    @staticmethod
    def init_competition():
        mode = utils.get_config("user_mode")
        counts = DBUtils.get_all_alive_participators(mode)
        if DockerUtils.init_teams(counts):
            return True
        else:
            return False

    @staticmethod
    def build_env(challenge_id):
        if DockerUtils.build_env(challenge_id):
            if DBUtils.build_env(challenge_id):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def start_env(challenge_id, counts=None):
        mode = utils.get_config("user_mode")
        if counts == None:
            counts = DBUtils.get_all_alive_participators(mode)
        if DockerUtils.run_env(counts, challenge_id):
            return True
        else:
            return False

    @staticmethod
    def remove_env(challenge_id, counts=None):
        mode = utils.get_config("user_mode")
        if counts == None:
            counts = DBUtils.get_all_alive_participators(mode)
        if DockerUtils.delete_env(counts, challenge_id):
            return True
        else:
            return False

    @staticmethod
    def check_env(type="init", challenge_id=""):
        if type == "init":
            print("timebase")
            rq = requests.session()
            get = "http://localhost:4000"
            url = "http://localhost:4000/plugins/ctfd-glowworm/admin/init"
            result = rq.get(get)
            token = "".join(re.findall("var csrf_nonce = \"(.*)\"", result.text))
            print(token)
            data = {
                'attack_id': "0",
                'victim_id': "0",
                'docker_id': "",
                'flag': ""
            }
            headers = {"CSRF-Token": token, "Content-Type": "application/json"}
            print(rq.post(url, data=json.dumps(data), headers=headers))
            return True
        else:
            # Todo: Add Time-Base Check here
            if DockerUtils.check_env(challenge_id):
                return True
            else:
                return False

    @staticmethod
    def renew_container(user_id, challenge_id):
        mode = utils.get_config("user_mode")
        counts = [DBUtils.get_alive_participator(mode, user_id)]
        try:
            ControlUtil.remove_env(challenge_id, counts)
            ControlUtil.start_env(challenge_id, counts)
            return True
        except Exception as e:
            print(e)
            return False



    @staticmethod
    def get_container(challenge_id, user_id):
        return DBUtils.get_current_containers(challenge_id, user_id)

    @staticmethod
    def check_challenge(challenge_id, user_id):
        user = Users.query.filter_by(id=user_id).first()

        if user.type == "admin":
            Challenges.query.filter(
                Challenges.id == challenge_id
            ).first_or_404()
        else:
            Challenges.query.filter(
                Challenges.id == challenge_id,
                and_(Challenges.state != "hidden", Challenges.state != "locked"),
            ).first_or_404()

    @staticmethod
    def frequency_limit():
        if "limit" not in session:
            session["limit"] = int(time.time())
            return False

        if int(time.time()) - session["limit"] < 1:
            return True

        session["limit"] = int(time.time())
        return False
