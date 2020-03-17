import time

from CTFd.models import Challenges, Users
from .db_utils import DBUtils
from .ecs_utils import ECSUtils
from sqlalchemy.sql import and_
from flask import session

class ControlUtil:
    @staticmethod
    def new_instance(user_id, challenge_id):
        rq = ECSUtils.up_aliyun_ecs(user_id=user_id, challenge_id=challenge_id)
        if isinstance(rq, tuple):
            DBUtils.new_instance(user_id, challenge_id, flag=rq[2], ip=rq[1], instance_id=rq[0])
            return True
        else:
            return rq


    @staticmethod
    def destroy_instance(user_id):
        try:
            remove_result = ECSUtils.remove_current_aliyun_instance(user_id)
            # docker_result = ECSUtils.remove_current_aliyun_instance(user_id)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def expired_instance(user_id, challenge_id):
        DBUtils.renew_current_instance(user_id=user_id, challenge_id=challenge_id)

    @staticmethod
    def get_instance(user_id):
        return DBUtils.get_current_instances(user_id=user_id)

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
