from CTFd.utils import user as current_user
from CTFd import utils

def get_mode():
    mode = utils.get_config("user_mode")
    if mode == "teams":
        user_id = current_user.get_current_user().team_id
    else:
        user_id = current_user.get_current_user().id
    return user_id