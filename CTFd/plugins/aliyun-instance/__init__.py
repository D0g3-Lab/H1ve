from __future__ import division  # Use floating point for math calculations

from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.flags import get_flag_class
from CTFd.utils.user import get_current_user
from CTFd import utils
from CTFd.models import (
    db,
    Solves,
    Fails,
    Flags,
    Challenges,
    ChallengeFiles,
    Tags,
    Hints,
    Users,
    Notifications
)
from flask import render_template, request, jsonify, Blueprint, current_app
from CTFd.utils.user import get_ip
from CTFd.utils.uploads import delete_file
from CTFd.utils.decorators import admins_only, authed_only
from CTFd.utils.modes import get_model
from CTFd.utils import user as current_user
from .models import AliyunInstanceChallenge, AliyunChallenge
from CTFd.plugins.challenges import CHALLENGE_CLASSES
from .db_utils import DBUtils
from .control_utils import ControlUtil
import datetime
import logging
import fcntl
from flask_apscheduler import APScheduler
import logging, os, sys
from .extensions import get_mode

def load(app):
    # upgrade()
    app.db.create_all()
    CHALLENGE_CLASSES["Aliyun_Instance_Challenge"] = AliyunInstanceChallenge
    register_plugin_assets_directory(
        app, base_path="/plugins/aliyun-instance/assets/"
    )
    ali_blueprint = Blueprint(
        "aliyun-instance",
        __name__,
        template_folder="templates",
        static_folder="assets",
        url_prefix="/plugins/aliyun-instance"
    )

    log_dir = app.config["LOG_FOLDER"]
    logger_ali = logging.getLogger("aliyun-instance")
    logger_ali.setLevel(logging.INFO)
    logs = {
        "aliyun-instance": os.path.join(log_dir, "aliyun-instance.log"),
    }
    try:
        for log in logs.values():
            if not os.path.exists(log):
                open(log, "a").close()
        container_log = logging.handlers.RotatingFileHandler(
            logs["aliyun-instance"], maxBytes=10000
        )
        logger_ali.addHandler(container_log)
    except IOError:
        pass

    stdout = logging.StreamHandler(stream=sys.stdout)
    logger_ali.addHandler(stdout)
    logger_ali.propagate = 0

    @ali_blueprint.route('/admin/settings', methods=['GET'])
    @admins_only
    # list plugin settings
    def admin_list_configs():
        configs = DBUtils.get_all_configs()
        return render_template('aliyun_configs.html', configs=configs)


    @ali_blueprint.route('/admin/settings', methods=['PATCH'])
    @admins_only
    # modify plugin settings
    def admin_save_configs():
        req = request.get_json()
        DBUtils.save_all_configs(req.items())
        return jsonify({'success': True})

    @ali_blueprint.route("/admin/containers", methods=['GET'])
    @admins_only
    # list alive containers
    def admin_list_containers():
        mode = utils.get_config("user_mode")
        configs = DBUtils.get_all_configs()
        page = abs(request.args.get("page", 1, type=int))
        results_per_page = 50
        page_start = results_per_page * (page - 1)
        page_end = results_per_page * (page - 1) + results_per_page

        count = DBUtils.get_all_alive_instance_count()
        containers = DBUtils.get_all_alive_instance_page(page_start, page_end)

        pages = int(count / results_per_page) + (count % results_per_page > 0)

        return render_template("aliyun_containers.html", containers=containers, pages=pages, curr_page=page,
                               curr_page_start=page_start, configs=configs, mode=mode)

    @ali_blueprint.route("/admin/containers", methods=['PATCH'])
    @admins_only
    def admin_expired_instance():
        user_id = request.args.get('user_id')
        challenge_id = request.args.get('challenge_id')
        ControlUtil.expired_instance(user_id=user_id, challenge_id=challenge_id)
        return jsonify({'success': True})

    @ali_blueprint.route("/admin/containers", methods=['DELETE'])
    @admins_only
    def admin_delete_container():
        user_id = request.args.get('user_id')
        ControlUtil.destroy_instance(user_id)
        return jsonify({'success': True})

    # instances
    @ali_blueprint.route('/container', methods=['GET'])
    @authed_only
    def list_container():
        try:
            user_id = get_mode()
            challenge_id = request.args.get('challenge_id')
            ControlUtil.check_challenge(challenge_id, user_id)
            data = ControlUtil.get_instance(user_id=user_id)
            if data is not None:
                if int(data.challenge_id) != int(challenge_id):
                    return jsonify({})

                dynamic_aliyun_challenge = AliyunChallenge.query \
                    .filter(AliyunChallenge.id == data.challenge_id) \
                    .first_or_404()

                return jsonify({'success': True, 'type': 'redirect', 'ip': data.ip,
                                    'remaining_time': 3600 - (datetime.datetime.utcnow() - data.start_time).seconds})
            else:
                return jsonify({'success': True})
        except Exception as e:
            logging.exception(e)
            return jsonify({'success': False, 'msg': str(e)})

    @ali_blueprint.route('/container', methods=['POST'])
    @authed_only
    def new_instance():
        try:
            user_id = get_mode()

            if ControlUtil.frequency_limit():
                return jsonify({'success': False, 'msg': 'Frequency limit, You should wait at least 1 min.'})
            # check whether exist container before
            existContainer = ControlUtil.get_instance(user_id)
            if existContainer:
                return jsonify({'success': False, 'msg': 'You have boot {} before.'.format(existContainer.challenge.name)})
            else:
                challenge_id = request.args.get('challenge_id')
                ControlUtil.check_challenge(challenge_id, user_id)
                configs = DBUtils.get_all_configs()
                current_count = DBUtils.get_all_alive_instance_count()
                if configs.get("aliyun_max_ECS_count") != "None":
                    if int(configs.get("aliyun_max_ECS_count")) <= int(current_count):
                        return jsonify({'success': False, 'msg': 'Max container count exceed.'})

                dynamic_aliyun_challenge = AliyunChallenge.query \
                    .filter(AliyunChallenge.id == challenge_id) \
                    .first_or_404()
                try:
                    result = ControlUtil.new_instance(user_id=user_id, challenge_id=challenge_id)
                    if isinstance(result, bool):
                        return jsonify({'success': True})
                    else:
                        return jsonify({'success': False, 'msg': str(result)})
                except Exception as e:
                    return jsonify({'success': True, 'msg':'Failed when launch instance, please contact with the admin.'+e})
        except Exception as e:
            return jsonify({'success': False, 'msg': str(e)})
            

    @ali_blueprint.route('/container', methods=['DELETE'])
    @authed_only
    def destroy_instance():
        user_id = get_mode()

        if ControlUtil.frequency_limit():
            return jsonify({'success': False, 'msg': 'Frequency limit, You should wait at least 1 min.'})

        if ControlUtil.destroy_instance(user_id):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'msg': 'Failed when destroy instance, please contact with the admin!'})

    @ali_blueprint.route('/container', methods=['PATCH'])
    @authed_only
    def renew_instance():
        user_id = get_mode()
        if ControlUtil.frequency_limit():
            return jsonify({'success': False, 'msg': 'Frequency limit, You should wait at least 1 min.'})

        configs = DBUtils.get_all_configs()
        challenge_id = request.args.get('challenge_id')
        ControlUtil.check_challenge(challenge_id, user_id)
        aliyun_max_renew_count = int(configs.get("aliyun_max_renew_count"))
        container = ControlUtil.get_instance(user_id)
        if container is None:
            return jsonify({'success': False, 'msg': 'Instance not found.'})
        if container.renew_count >= aliyun_max_renew_count:
            return jsonify({'success': False, 'msg': 'Max renewal times exceed.'})

        ControlUtil.expired_instance(user_id=user_id, challenge_id=challenge_id)

        return jsonify({'success': True})

    def auto_clean_container():
        # 每隔5分钟就好，第一次创建的时间为50分钟
        with app.app_context():
            results = DBUtils.get_all_expired_instance()
            for r in results:
                ControlUtil.destroy_instance(r.user_id)

            FrpUtils.update_frp_redirect()

    app.register_blueprint(ali_blueprint)

    try:
        lock_file = open("/tmp/aliyun-instance.lock", "w")
        lock_fd = lock_file.fileno()
        fcntl.lockf(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
        scheduler.add_job(id='aliyun-instance-auto-clean', func=auto_clean_container, trigger="interval", seconds=300)

        print("[CTFd Ali-ECS]Started successfully")
    except IOError:
        pass