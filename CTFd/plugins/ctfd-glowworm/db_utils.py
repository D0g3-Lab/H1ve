import datetime
import uuid
from CTFd import utils
from .models import GlowwormConfigs, GlowwormContainers, ADAChallenge, GlowwormAttacks
from CTFd.models import Users, Teams
from .extensions import get_competition_time
from CTFd.models import (
    db
)

class DBUtils:
    @staticmethod
    def get_all_configs():
        configs = GlowwormConfigs.query.all()
        result = {}

        for c in configs:
            result[str(c.key)] = str(c.value)

        return result

    @staticmethod
    def save_all_configs(configs):
        for c in configs:
            q = db.session.query(GlowwormConfigs)
            q = q.filter(GlowwormConfigs.key == c[0])
            record = q.one_or_none()
            if record:
                record.value = c[1]
                db.session.commit()
            else:
                config = GlowwormConfigs(key=c[0], value=c[1])
                db.session.add(config)
                db.session.commit()
        db.session.close()

    @staticmethod
    def build_env(challenge_id):
        try:
            ADAChallenge.query.filter_by(id=challenge_id).first_or_404().env_build_status = True
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_current_containers(challenge_id, user_id):
        container = GlowwormContainers.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
        if container:
            return container
        else:
            return None

    @staticmethod
    def get_all_container():
        q = db.session.query(GlowwormContainers)
        return q.all()

    @staticmethod
    def get_all_alive_container_page(page_start, page_end):
        q = db.session.query(GlowwormContainers)
        q = q.slice(page_start, page_end)
        return q.all()

    @staticmethod
    def get_all_alive_container_count():
        q = db.session.query(GlowwormContainers)
        return q.count()

    @staticmethod
    def get_all_alive_participators(mode=""):
        if mode == "users":
            q = db.session.query(Users)
        else:
            q = db.session.query(Teams)
        return q.all()

    @staticmethod
    def get_alive_participator(mode, user_id):
        if mode == "users":
            q = Users.query.filter_by(id=user_id).first()
        else:
            qq = Users.query.filter_by(id=user_id).first().team_id
            q = Teams.query.filter_by(id=qq).first()
        return q

    @staticmethod
    def get_all_alive_environment_page(page_start, page_end):
        q = db.session.query(ADAChallenge)
        q = q.slice(page_start, page_end)
        return q.all()

    @staticmethod
    def get_all_alive_environment_count():
        q = db.session.query(ADAChallenge)
        return q.count()

    @staticmethod
    def update_flag(docker_id, flag):
        try:
            GlowwormContainers.query.filter_by(docker_id=docker_id).first().flag = flag
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_attack_log(attack_id, victim_id, docker_id, flag):
        competition_time = get_competition_time()
        print(competition_time)
        round = 1
        try:
            if victim_id != "0":
                attack = GlowwormAttacks(
                    attack_id = attack_id,
                    victim_id = victim_id,
                    docker_id = docker_id,
                    envname = docker_id.split("_")[1],
                    flag = flag,
                    round =round
                )
                print(attack)
            else:
                attack = GlowwormAttacks(
                    flag="New Round {}".format(round),
                    round=round
                )
                print(attack)

            db.session.add(attack)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            print(e)
            return False