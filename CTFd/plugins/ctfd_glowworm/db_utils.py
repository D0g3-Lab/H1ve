import datetime, random, uuid
from CTFd import utils
from .models import GlowwormConfigs, GlowwormContainers, ADAChallenge, GlowwormAttacks, GlowwormInitLog
from CTFd.models import Users, Teams
from .extensions import get_round
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
            return str(e)

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
            # Todo: 重新封装模式判断
            # qq = Users.query.filter_by(id=user_id).first().team_id
            q = Teams.query.filter_by(id=user_id).first()
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
    def get_alive_ports():
        configs = DBUtils.get_all_configs()
        min = int(configs.get("port_minimum") )if configs.get("port_minimum") else 40000
        max = int(configs.get("port_maximum")) if configs.get("port_maximum") else 50000

        while 1:
            service_port = random.randint(min, max)
            if GlowwormContainers.query.filter_by(service_port=service_port).first() == None:
                break
            else:
                service_port = random.randint(min, max)
        while 1:
            ssh_port = random.randint(min, max)
            if GlowwormContainers.query.filter_by(ssh_port=ssh_port).first() == None:
                break
            else:
                ssh_port = random.randint(min, max)
        return service_port, ssh_port

    @staticmethod
    def update_attack_log(attack_id=None, attack_name=None, victim_id=None, victim_name=None, challenge_id=None, flag=None):
        from .schedule import scheduler
        with scheduler.app.app_context():
            round = get_round()
            try:
                if challenge_id != None:
                    container = GlowwormContainers.query.filter_by(challenge_id=challenge_id,user_id=victim_id).first()
                    docker_id = container.docker_id
                    attack = GlowwormAttacks(
                        attack_id = attack_id,
                        attack_name = attack_name,
                        victim_id = victim_id,
                        victim_name = victim_name,
                        docker_id = docker_id,
                        envname = docker_id.split("_")[1],
                        flag = flag,
                        round =round
                    )
                    mode = utils.get_config("user_mode")
                    if mode == "users":
                        user_id = victim_id
                        team_id = None
                    else:
                        user_id = None
                        team_id = victim_id
                    init = GlowwormInitLog(
                        user_id=victim_id,
                        team_id=victim_name,
                        victim_user_id=victim_id,
                        victim_team_id=victim_name,
                        challenge_id=challenge_id,
                        ip="127.0.0.1",
                        provided="Init",
                    )
                    db.session.add(init)

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