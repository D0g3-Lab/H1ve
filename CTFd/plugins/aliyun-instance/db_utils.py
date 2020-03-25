import datetime
import uuid

from .models import AliyunInstanceConfigs, AliyunECS

from CTFd.models import (
    db
)

class DBUtils:
    @staticmethod
    def get_all_configs():
        configs = AliyunInstanceConfigs.query.all()
        result = {}

        for c in configs:
            result[str(c.key)] = str(c.value)

        return result

    @staticmethod
    def save_all_configs(configs):
        for c in configs:
            q = db.session.query(AliyunInstanceConfigs)
            q = q.filter(AliyunInstanceConfigs.key == c[0])
            record = q.one_or_none()

            if record:
                record.value = c[1]
                db.session.commit()
            else:
                config = AliyunInstanceConfigs(key=c[0], value=c[1])
                db.session.add(config)
                db.session.commit()
        db.session.close()

    @staticmethod
    def new_instance(user_id, challenge_id, flag, instance_id, port=0, ip=""):
        instance = AliyunECS(user_id=user_id, challenge_id=challenge_id, flag=flag, instance_id=instance_id, ip=ip)
        db.session.add(instance)
        db.session.commit()
        db.session.close()
        return str(instance_id)

    @staticmethod
    def get_current_instances(user_id):
        q = db.session.query(AliyunECS)
        q = q.filter(AliyunECS.user_id == user_id)
        # print(AliyunECS.user_id+'aaa')
        # print(user_id)
        records = q.all()
        if len(records) == 0:
            return None

        return records[0]

    @staticmethod
    def get_instance_by_port(port):
        q = db.session.query(AliyunECS)
        q = q.filter(AliyunECS.port == port)
        records = q.all()
        if len(records) == 0:
            return None

        return records[0]

    @staticmethod
    def remove_current_instance(user_id):
        q = db.session.query(AliyunECS)
        q = q.filter(AliyunECS.user_id == user_id)
        # records = q.all()
        # for r in records:
        #     pass

        q.delete()
        db.session.commit()
        db.session.close()

    @staticmethod
    def renew_current_instance(user_id, challenge_id):
        q = db.session.query(AliyunECS)
        q = q.filter(AliyunECS.user_id == user_id)
        q = q.filter(AliyunECS.challenge_id == challenge_id)
        records = q.all()
        if len(records) == 0:
            return

        r = records[0]
        r.start_time = r.start_time + datetime.timedelta(seconds=3600)

        if r.start_time > datetime.datetime.utcnow():
            r.start_time = datetime.datetime.utcnow()

        r.renew_count += 1
        db.session.commit()
        db.session.close()

    @staticmethod
    def get_all_expired_instance():
        q = db.session.query(AliyunECS)
        q = q.filter(AliyunECS.start_time < datetime.datetime.utcnow() - datetime.timedelta(seconds=3600))
        return q.all()

    @staticmethod
    def get_all_alive_instance():
        q = db.session.query(AliyunECS)
        q = q.filter(AliyunECS.start_time >= datetime.datetime.utcnow() - datetime.timedelta(seconds=3600))
        return q.all()

    @staticmethod
    def get_all_instance():
        q = db.session.query(AliyunECS)
        return q.all()

    @staticmethod
    def get_all_alive_instance_page(page_start, page_end):
        q = db.session.query(AliyunECS)
        q = q.filter(AliyunECS.start_time >= datetime.datetime.utcnow() - datetime.timedelta(seconds=3600))
        q = q.slice(page_start, page_end)
        return q.all()

    @staticmethod
    def get_all_alive_instance_count():
        q = db.session.query(AliyunECS)
        q = q.filter(AliyunECS.start_time >= datetime.datetime.utcnow() - datetime.timedelta(seconds=3600))
        return q.count()
