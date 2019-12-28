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
from .models import DynamicCheckValueChallenge, DynamicCheckChallenge
from CTFd.plugins.challenges import CHALLENGE_CLASSES
from .db_utils import DBUtils
from .control_utils import ControlUtil
from .frp_utils import FrpUtils
import datetime, fcntl
from flask_apscheduler import APScheduler
import logging, os, sys
from .extensions import get_mode

def load(app):
    # upgrade()
    app.db.create_all()
    CHALLENGE_CLASSES["dynamic_check_docker"] = DynamicCheckValueChallenge
    register_plugin_assets_directory(
        app, base_path="/plugins/ctfd-owl/assets/"
    )
    owl_blueprint = Blueprint(
        "ctfd-owl",
        __name__,
        template_folder="templates",
        static_folder="assets",
        url_prefix="/plugins/ctfd-owl"
    )

    log_dir = app.config["LOG_FOLDER"]
    logger_owl = logging.getLogger("owl")
    logger_owl.setLevel(logging.INFO)
    logs = {
        "owl": os.path.join(log_dir, "owl.log"),
    }
    try:
        for log in logs.values():
            if not os.path.exists(log):
                open(log, "a").close()
        container_log = logging.handlers.RotatingFileHandler(
            logs["owl"], maxBytes=10000
        )
        logger_owl.addHandler(container_log)
    except IOError:
        pass

    stdout = logging.StreamHandler(stream=sys.stdout)
    logger_owl.addHandler(stdout)
    logger_owl.propagate = 0

    @owl_blueprint.route('/admin/settings', methods=['GET'])
    @admins_only
    # list plugin settings
    def admin_list_configs():
        configs = DBUtils.get_all_configs()
        return render_template('configs.html', configs=configs)


    @owl_blueprint.route('/admin/settings', methods=['PATCH'])
    @admins_only
    # modify plugin settings
    def admin_save_configs():
        req = request.get_json()
        DBUtils.save_all_configs(req.items())
        return jsonify({'success': True})

    @owl_blueprint.route("/admin/containers", methods=['GET'])
    @admins_only
    # list alive containers
    def admin_list_containers():
        mode = utils.get_config("user_mode")
        configs = DBUtils.get_all_configs()
        page = abs(request.args.get("page", 1, type=int))
        results_per_page = 50
        page_start = results_per_page * (page - 1)
        page_end = results_per_page * (page - 1) + results_per_page

        count = DBUtils.get_all_alive_container_count()
        containers = DBUtils.get_all_alive_container_page(page_start, page_end)

        pages = int(count / results_per_page) + (count % results_per_page > 0)
        return render_template("containers.html", containers=containers, pages=pages, curr_page=page,
                               curr_page_start=page_start, configs=configs, mode=mode)

    @owl_blueprint.route("/admin/containers", methods=['PATCH'])
    @admins_only
    def admin_expired_container():
        user_id = request.args.get('user_id')
        challenge_id = request.args.get('challenge_id')
        ControlUtil.expired_container(user_id=user_id, challenge_id=challenge_id)
        return jsonify({'success': True})

    @owl_blueprint.route("/admin/containers", methods=['DELETE'])
    @admins_only
    def admin_delete_container():
        user_id = request.args.get('user_id')
        ControlUtil.destroy_container(user_id)
        return jsonify({'success': True})

    # instances
    @owl_blueprint.route('/container', methods=['GET'])
    @authed_only
    def list_container():
        try:
            user_id = get_mode()
            challenge_id = request.args.get('challenge_id')
            ControlUtil.check_challenge(challenge_id, user_id)
            data = ControlUtil.get_container(user_id=user_id)
            configs = DBUtils.get_all_configs()
            domain = configs.get('frp_http_domain_suffix', "")
            if data is not None:
                if int(data.challenge_id) != int(challenge_id):
                    return jsonify({})
                dynamic_docker_challenge = DynamicCheckChallenge.query \
                    .filter(DynamicCheckChallenge.id == data.challenge_id) \
                    .first_or_404()
                lan_domain = str(user_id) + "-" + data.docker_id

                if dynamic_docker_challenge.deployment == "single":
                    return jsonify({'success': True, 'type': 'redirect', 'ip': configs.get('frp_direct_ip_address', ""),
                                    'port': data.port,
                                    'remaining_time': 3600 - (datetime.datetime.utcnow() - data.start_time).seconds,
                                    'lan_domain': lan_domain})
                else:
                    if dynamic_docker_challenge.redirect_type == "http":
                        if int(configs.get('frp_http_port', "80")) == 80:
                            return jsonify({'success': True, 'type': 'http', 'domain': data.docker_id + "." + domain,
                                               'remaining_time': 3600 - (datetime.datetime.utcnow() - data.start_time).seconds,
                                               'lan_domain': lan_domain})
                        else:
                            return jsonify({'success': True, 'type': 'http',
                                               'domain': data.docker_id + "." + domain + ":" + configs.get('frp_http_port', "80"),
                                               'remaining_time': 3600 - (datetime.datetime.utcnow() - data.start_time).seconds,
                                               'lan_domain': lan_domain})
                    else:
                        return jsonify({'success': True, 'type': 'redirect', 'ip': configs.get('frp_direct_ip_address', ""),
                                           'port': data.port,
                                           'remaining_time': 3600 - (datetime.datetime.utcnow() - data.start_time).seconds,
                                           'lan_domain': lan_domain})
            else:
                return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'msg': str(e)})

    @owl_blueprint.route('/container', methods=['POST'])
    @authed_only
    def new_container():
        try:
            user_id = get_mode()

            if ControlUtil.frequency_limit():
                return jsonify({'success': False, 'msg': 'Frequency limit, You should wait at least 1 min.'})
            # check whether exist container before
            existContainer = ControlUtil.get_container(user_id)
            if existContainer:
                return jsonify({'success': False, 'msg': 'You have boot {} before.'.format(existContainer.challenge.name)})
            else:
                challenge_id = request.args.get('challenge_id')
                ControlUtil.check_challenge(challenge_id, user_id)
                configs = DBUtils.get_all_configs()
                current_count = DBUtils.get_all_alive_container_count()
                # print(configs.get("docker_max_container_count"))
                if configs.get("docker_max_container_count") != "None":
                    if int(configs.get("docker_max_container_count")) <= int(current_count):
                        return jsonify({'success': False, 'msg': 'Max container count exceed.'})

                dynamic_docker_challenge = DynamicCheckChallenge.query \
                    .filter(DynamicCheckChallenge.id == challenge_id) \
                    .first_or_404()
                try:
                    result = ControlUtil.new_container(user_id=user_id, challenge_id=challenge_id)
                    if isinstance(result, bool):
                        return jsonify({'success': True})
                    else:
                        return jsonify({'success': False, 'msg': str(result)})
                except Exception as e:
                    return jsonify({'success': True, 'msg':'Failed when launch instance, please contact with the admin.'})
        except Exception as e:
            return jsonify({'success': False, 'msg': str(e)})

    @owl_blueprint.route('/container', methods=['DELETE'])
    @authed_only
    def destroy_container():
        user_id = get_mode()

        if ControlUtil.frequency_limit():
            return jsonify({'success': False, 'msg': 'Frequency limit, You should wait at least 1 min.'})

        if ControlUtil.destroy_container(user_id):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'msg': 'Failed when destroy instance, please contact with the admin!'})

    @owl_blueprint.route('/container', methods=['PATCH'])
    @authed_only
    def renew_container():
        user_id = get_mode()
        if ControlUtil.frequency_limit():
            return jsonify({'success': False, 'msg': 'Frequency limit, You should wait at least 1 min.'})

        configs = DBUtils.get_all_configs()
        challenge_id = request.args.get('challenge_id')
        ControlUtil.check_challenge(challenge_id, user_id)
        docker_max_renew_count = int(configs.get("docker_max_renew_count"))
        container = ControlUtil.get_container(user_id)
        if container is None:
            return jsonify({'success': False, 'msg': 'Instance not found.'})
        if container.renew_count >= docker_max_renew_count:
            return jsonify({'success': False, 'msg': 'Max renewal times exceed.'})

        ControlUtil.expired_container(user_id=user_id, challenge_id=challenge_id)

        return jsonify({'success': True})

    def auto_clean_container():
        with app.app_context():
            results = DBUtils.get_all_expired_container()
            for r in results:
                ControlUtil.destroy_container(r.user_id)

            FrpUtils.update_frp_redirect()

    app.register_blueprint(owl_blueprint)

    try:
        lock_file = open("/tmp/ctfd_owl.lock", "w")
        lock_fd = lock_file.fileno()
        fcntl.lockf(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
        scheduler.add_job(id='owl-auto-clean', func=auto_clean_container, trigger="interval", seconds=5)

        print("[CTFd Owl]Started successfully")
    except IOError:
        pass