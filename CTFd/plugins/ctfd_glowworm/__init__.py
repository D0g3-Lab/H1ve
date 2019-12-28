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
from CTFd.utils.decorators import admins_only, authed_only, during_ctf_time_only
from CTFd.utils.modes import get_model
from CTFd.utils import user as current_user
from .models import GlowwormChallenge, ADAChallenge, GlowwormContainers, GlowwormAttacks
from CTFd.plugins.challenges import CHALLENGE_CLASSES
from .db_utils import DBUtils
from .control_utils import ControlUtil
import datetime, fcntl
import logging, os, sys, uuid
from .extensions import get_mode

def load(app):
    # upgrade()
    app.db.create_all()
    CHALLENGE_CLASSES["ada_challenge"] = GlowwormChallenge
    register_plugin_assets_directory(
        app, base_path="/plugins/ctfd_glowworm/assets/"
    )
    glowworm_blueprint = Blueprint(
        "ctfd-glowworm",
        __name__,
        template_folder="templates",
        static_folder="assets",
        url_prefix="/plugins/ctfd-glowworm"
    )

    log_dir = app.config["LOG_FOLDER"]
    logger_glowworm = logging.getLogger("glowworm")
    logger_glowworm.setLevel(logging.INFO)
    logs = {
        "glowworm": os.path.join(log_dir, "glowworm.log"),
    }
    try:
        for log in logs.values():
            if not os.path.exists(log):
                open(log, "a").close()
        container_log = logging.handlers.RotatingFileHandler(
            logs["glowworm"], maxBytes=10000
        )
        logger_glowworm.addHandler(container_log)
    except IOError:
        pass

    stdout = logging.StreamHandler(stream=sys.stdout)
    logger_glowworm.addHandler(stdout)
    logger_glowworm.propagate = 0

    @glowworm_blueprint.route("/flag", methods=['POST'])
    # TODO: fix differfent time bug
    # @during_ctf_time_only
    def update_flag():
        try:
            req = request.get_json()
            print(req)
            key = GlowwormContainers.query.filter_by(docker_id=req['name']).first().key
            if req['key'] != key:
                return jsonify({'success': False})
            else:
                flag = uuid.uuid3(uuid.UUID(req['uuid']), req['name'] + req['time'] + key)

                if DBUtils.update_flag(req['name'], 'flag{' + str(flag) + '}'):
                    return jsonify({'success': True})
                else:
                    return jsonify({'success': False})
        except Exception as e:
            print(e)
            return jsonify({'success': False})

    @glowworm_blueprint.route("/challenge/<challenge_id>", methods=['GET'])
    def get_targets(challenge_id):
        try:
            datas = {'success': True, 'data':[]}
            containers = GlowwormContainers.query.filter_by(challenge_id=challenge_id).all()
            print(challenge_id,containers)
            for container in containers:
                datas['data'].append({"target":"{}:{}".format(container.ip, container.service_port)})
            datas['length'] = len(datas['data'])
            return jsonify(datas)
        except Exception as e:
            print(e)
            return jsonify({'success': False})

    @glowworm_blueprint.route('/admin/settings', methods=['GET'])
    @admins_only
    # list plugin settings
    def admin_list_configs():
        configs = DBUtils.get_all_configs()
        return render_template('glowworm_configs.html', configs=configs)

    @glowworm_blueprint.route('/admin/settings', methods=['PATCH'])
    @admins_only
    # modify plugin settings
    def admin_save_configs():
        req = request.get_json()
        DBUtils.save_all_configs(req.items())
        return jsonify({'success': True})

    @glowworm_blueprint.route("/admin/containers", methods=['GET'])
    @admins_only
    # list alive containers
    def admin_list_containers():
        configs = DBUtils.get_all_configs()
        page = abs(request.args.get("page", 1, type=int))
        results_per_page = 50
        page_start = results_per_page * (page - 1)
        page_end = results_per_page * (page - 1) + results_per_page

        count = DBUtils.get_all_alive_container_count()
        containers = DBUtils.get_all_alive_container_page(page_start, page_end)

        pages = int(count / results_per_page) + (count % results_per_page > 0)
        return render_template("glowworm_containers.html", containers=containers, pages=pages, curr_page=page,
                               curr_page_start=page_start, configs=configs)

    @glowworm_blueprint.route('/admin/containers', methods=['PATCH'])
    @admins_only
    def renew_admin_container():
        user_id = request.args.get('user_id')
        challenge_id = request.args.get('challenge_id')
        if ControlUtil.frequency_limit():
            return jsonify({'success': False, 'msg': 'Frequency limit, You should wait at least 1 min.'})
        try:
            ControlUtil.renew_container(user_id, challenge_id)
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            return jsonify({'success': False})

    @glowworm_blueprint.route("/admin/environments", methods=['GET'])
    @admins_only
    # list alive containers
    def admin_list_environments():
        configs = DBUtils.get_all_configs()
        page = abs(request.args.get("page", 1, type=int))
        results_per_page = 50
        page_start = results_per_page * (page - 1)
        page_end = results_per_page * (page - 1) + results_per_page

        count = DBUtils.get_all_alive_environment_count()
        environments = DBUtils.get_all_alive_environment_page(page_start, page_end)

        pages = int(count / results_per_page) + (count % results_per_page > 0)
        return render_template("glowworm_environments.html", environments=environments, pages=pages, curr_page=page,
                               curr_page_start=page_start)


    @glowworm_blueprint.route("/admin/init", methods=['PATCH'])
    @admins_only
    def admin_init_competitions():
        try:
            from .schedule import scheduler
            start_time = int(utils.get_config("start"))
            interval = DBUtils.get_all_configs().get("per_round")
            interval = str(int(int(interval) / 60))
            if ControlUtil.init_competition():
                job = scheduler.add_job(id='time_base', func=ControlUtil.check_env, args=["init"], trigger='cron', minute="*/{}".format(interval))
                # job = scheduler.add_job(id='time_base', func=ControlUtil.check_env, args=["init"], trigger='interval', seconds=5)
                print(job)
                return jsonify({'success': True})
            else:
                return jsonify({'success': False})
        except Exception as e:
            return jsonify({'success': False, 'msg': str(e)})

    @glowworm_blueprint.route("/admin/remove", methods=['PATCH'])
    @admins_only
    def admin_remove_competitions():
        if ControlUtil.remove_competition():
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})

    @glowworm_blueprint.route("/live/attacks", methods=['GET', 'POST'])
    @admins_only
    def attacks():
        if request.method == "GET":
            attacks = GlowwormAttacks.query.order_by(GlowwormAttacks.time.desc()).all()
            print(attacks)
            return jsonify({'success': True})
        elif request.method == "POST":
            req = request.get_json()
            print(req)

            return jsonify({'success': True})

            return jsonify({'success': False})

    @glowworm_blueprint.route("/admin/env", methods=['PATCH'])
    @admins_only
    def admin_env():
        req = request.get_json()
        print(req)
        if req["type"] == "init":
            result = ControlUtil.check_env()
        elif req["type"] == "check":
            result = ControlUtil.check_env(req['type'], req['challenge_id'])
        elif req["type"] == "build":
            result = ControlUtil.build_env(req['challenge_id'])
        elif req["type"] == "run":
            result = ControlUtil.start_env(req['challenge_id'])
        elif req["type"] == "remove":
            result = ControlUtil.remove_env(req['challenge_id'])

        if result:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'msg': result})

    @glowworm_blueprint.route('/container', methods=['GET'])
    @authed_only
    def container_info():
        user_id = get_mode()
        challenge_id = request.args.get('challenge_id')
        ControlUtil.check_challenge(challenge_id, user_id)
        data = ControlUtil.get_container(user_id=user_id, challenge_id=challenge_id)
        configs = DBUtils.get_all_configs()
        if data is not None:
            if int(data.challenge_id) != int(challenge_id):
                return jsonify({})
            else:
                return jsonify({'success': True, 'type': 'direct', 'ip': configs.get('direct_address', ""),
                    'service_port' : data.service_port, 'ssh_port' : data.ssh_port, 'ssh_key' : data.ssh_key
                })
        else:
            return jsonify({'success': True})

    @glowworm_blueprint.route('/container', methods=['PATCH'])
    @authed_only
    def renew_container():
        user_id = get_mode()
        challenge_id = request.args.get('challenge_id')
        if ControlUtil.frequency_limit():
            return jsonify({'success': False, 'msg': 'Frequency limit, You should wait at least 1 min.'})
        try:
            ControlUtil.renew_container(user_id, challenge_id)
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            return jsonify({'success': False})

    @glowworm_blueprint.route("/attacks", methods=['GET'])
    def list_attacks():
        page = abs(request.args.get("page", 1, type=int))
        results_per_page = 50
        page_start = results_per_page * (page - 1)
        page_end = results_per_page * (page - 1) + results_per_page

        count = GlowwormAttacks.query.count()
        attacks = (
            GlowwormAttacks.query.order_by(GlowwormAttacks.time.desc())
                .slice(page_start, page_end)
                .all()
        )

        pages = int(count / results_per_page) + (count % results_per_page > 0)
        return render_template("glowworm_attacks.html", attacks=attacks, pages=pages, curr_page=page)

    app.register_blueprint(glowworm_blueprint)

    try:

        lock_file = open("/tmp/ctfd_glowworm.lock", "w")
        lock_fd = lock_file.fileno()
        fcntl.lockf(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

        from .schedule import scheduler, Config
        app.config.from_object(Config())
        scheduler.init_app(app)
        scheduler.start()
    except IOError:
        pass