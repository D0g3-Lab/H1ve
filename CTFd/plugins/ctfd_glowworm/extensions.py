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

def get_round():
    from .models import GlowwormConfigs
    configs = GlowwormConfigs.query.all()
    result = {}
    for c in configs:
        result[str(c.key)] = str(c.value)

    interval = int(result.get("per_round"))
    start_time = int(utils.get_config("start"))

    start_time = datetime.datetime.utcfromtimestamp(start_time)
    round = int(int((datetime.datetime.utcnow() - start_time).seconds / interval))
    return round

def teampasswd(key):
    pwd = uuid.uuid3(uuid.NAMESPACE_DNS, key)
    return str(pwd)

