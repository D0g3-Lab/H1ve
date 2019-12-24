from flask_apscheduler import APScheduler
from apscheduler.jobstores.redis import RedisJobStore

class Config(object):
    SCHEDULER_JOBSTORES = {
        'default': RedisJobStore(host="cache", port=6379, password="", db=15)
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_API_ENABLED = True

scheduler = APScheduler()