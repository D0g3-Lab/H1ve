from CTFd.utils import user as current_user
from CTFd import utils
import random, string, os, uuid, datetime


def get_mode():
    mode = utils.get_config("user_mode")
    if mode == "teams":
        user_id = current_user.get_current_user().team_id
    else:
        user_id = current_user.get_current_user().id
    return user_id

def get_competition_time():
    start_time = utils.get_config("start") if utils.get_config("start") else datetime.datetime.utcnow()
    end_time = utils.get_config("end") if utils.get_config("end") else datetime.datetime.utcnow()
    return start_time, end_time

def teampasswd(key):
    pwd = uuid.uuid3(uuid.NAMESPACE_DNS, key)
    return str(pwd)

