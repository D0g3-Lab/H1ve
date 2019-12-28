import time, os, json, requests, re, datetime
from CTFd.models import Challenges, Users, Submissions
from CTFd import utils
from .db_utils import DBUtils
from .models import ADAChallenge, GlowwormAttacks
from .docker_utils import DockerUtils
from sqlalchemy.sql import and_
from flask import session
from CTFd.models import db

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
    def remove_competition():
        mode = utils.get_config("user_mode")
        from .schedule import scheduler
        try:
            scheduler.remove_job('time_base')
        except Exception as e:
            pass
        challenges = ADAChallenge.query.all()
        # 清除运行的容器
        for challenge in challenges:
            ControlUtil.remove_env(challenge.id)
        # 清空相关数据库记录
        try:
            num_rows_deleted = db.session.query(GlowwormAttacks).delete()
            print(num_rows_deleted)
            num_rows_deleted = db.session.query(Submissions).filter(Submissions.type == "check").delete()
            print(num_rows_deleted)
            num_rows_deleted = db.session.query(Submissions).filter(Submissions.type == "attack").delete()
            print(num_rows_deleted)
            num_rows_deleted = db.session.query(Submissions).filter(Submissions.type == "init").delete()
            print(num_rows_deleted)
            db.session.commit()
        except:
            db.session.rollback()
        return True

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
            DBUtils.update_attack_log()
            return True
        else:
            from .schedule import scheduler
            interval = DBUtils.get_all_configs().get("per_round")
            interval = str(int(int(interval) / 60))
            status = ADAChallenge.query.filter_by(id=challenge_id).first()
            if status.env_check_status:
                try:
                    job = scheduler.remove_job("glowworm_check_{}".format(challenge_id))
                except Exception as e:
                    print(e)
                status.env_check_status = False
            else:
                job = scheduler.add_job(id="glowworm_check_{}".format(challenge_id), func=DockerUtils.check_env, args=[challenge_id], trigger='cron', minute = "*/{}".format(interval))
                status.env_check_status = True
                print(job)
            db.session.commit()
            db.session.close()
            return True

    @staticmethod
    def renew_container(user_id, challenge_id):
        mode = utils.get_config("user_mode")
        counts = [DBUtils.get_alive_participator(mode, user_id)]
        try:
            ControlUtil.remove_env(challenge_id, counts)
            ControlUtil.start_env(challenge_id, counts)
            DBUtils.update_attack_log(victim_id=counts[0].id, victim_name=counts[0].name, challenge_id=challenge_id, flag=None)
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

        if int(time.time()) - session["limit"] < 60:
            return True

        session["limit"] = int(time.time())
        return False
