from CTFd.plugins.challenges import BaseChallenge
from CTFd.plugins.flags import get_flag_class
from CTFd.utils.user import get_current_user, get_ip
from flask import Blueprint, current_app
from CTFd.utils.modes import get_model
from CTFd.utils.user import get_current_user
from CTFd.utils import user as current_user
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
    Teams,
    Notifications,
)
import math, datetime
from CTFd.utils.uploads import delete_file
from .extensions import get_mode

class GlowwormChallenge(BaseChallenge):
    id = "ada_challenge"  # Unique identifier used to register challenges
    name = "ada_challenge"  # Name of a challenge type
    templates = {  # Handlebars templates used for each aspect of challenge editing & viewing
        "create": "/plugins/ctfd-glowworm/assets/create.html",
        "update": "/plugins/ctfd-glowworm/assets/update.html",
        "view": "/plugins/ctfd-glowworm/assets/view.html",
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        "create": "/plugins/ctfd-glowworm/assets/create.js",
        "update": "/plugins/ctfd-glowworm/assets/update.js",
        "view": "/plugins/ctfd-glowworm/assets/view.js",
    }
    # Route at which files are accessible. This must be registered using register_plugin_assets_directory()
    route = "/plugins/ctfd-glowworm/assets/"
    # Blueprint used to access the static_folder directory.
    blueprint = Blueprint(
        "ctfd-glowworm-challenge",
        __name__,
        template_folder="templates",
        static_folder="assets",
        url_prefix="/plugins/ctfd-glowworm"
    )

    @staticmethod
    def create(request):
        """
        This method is used to process the challenge creation request.

        :param request:
        :return:
        """
        data = request.form or request.get_json()
        challenge = ADAChallenge(**data)

        db.session.add(challenge)
        db.session.commit()

        return challenge

    @staticmethod
    def read(challenge):
        """
        This method is in used to access the data of a challenge in a format processable by the front end.

        :param challenge:
        :return: Challenge object, data dictionary to be returned to the user
        """
        challenge = ADAChallenge.query.filter_by(id=challenge.id).first()
        data = {
            "id": challenge.id,
            "name": challenge.name,
            "value": challenge.value,
            "check_value": challenge.check_value,
            "description": challenge.description,
            "category": challenge.category,
            "state": challenge.state,
            "max_attempts": challenge.max_attempts,
            "type": challenge.type,
            "type_data": {
                "id": GlowwormChallenge.id,
                "name": GlowwormChallenge.name,
                "templates": GlowwormChallenge.templates,
                "scripts": GlowwormChallenge.scripts,
            },
        }
        return data

    @staticmethod
    def update(challenge, request):
        """
        This method is used to update the information associated with a challenge. This should be kept strictly to the
        Challenges table and any child tables.

        :param challenge:
        :param request:
        :return:
        """

        data = request.form or request.get_json()
        for attr, value in data.items():
            # We need to set these to floats so that the next operations don't operate on strings
            if attr in ("initial", "minimum", "decay"):
                value = float(value)
            setattr(challenge, attr, value)

        Model = get_model()

        solve_count = (
            Solves.query.join(Model, Solves.account_id == Model.id)
                .filter(
                Solves.challenge_id == challenge.id,
                Model.hidden == False,
                Model.banned == False,
            )
                .count()
        )

        # It is important that this calculation takes into account floats.
        # Hence this file uses from __future__ import division
        value = (
                        ((challenge.minimum - challenge.initial) / (challenge.decay ** 2))
                        * (solve_count ** 2)
                ) + challenge.initial

        value = math.ceil(value)

        if value < challenge.minimum:
            value = challenge.minimum

        challenge.value = value

        db.session.commit()
        return challenge

    @staticmethod
    def delete(challenge):
        """
        This method is used to delete the resources used by a challenge.

        :param challenge:
        :return:
        """
        Fails.query.filter_by(challenge_id=challenge.id).delete()
        Solves.query.filter_by(challenge_id=challenge.id).delete()
        Flags.query.filter_by(challenge_id=challenge.id).delete()
        GlowwormContainers.query.filter_by(id=challenge.id).delete()
        files = ChallengeFiles.query.filter_by(challenge_id=challenge.id).all()
        for f in files:
            delete_file(f.id)
        ChallengeFiles.query.filter_by(challenge_id=challenge.id).delete()
        Tags.query.filter_by(challenge_id=challenge.id).delete()
        Hints.query.filter_by(challenge_id=challenge.id).delete()
        ADAChallenge.query.filter_by(id=challenge.id).delete()
        Challenges.query.filter_by(id=challenge.id).delete()
        db.session.commit()

    @staticmethod
    def attempt(challenge, request):
        """
        This method is used to check whether a given input is right or wrong. It does not make any changes and should
        return a boolean for correctness and a string to be shown to the user. It is also in charge of parsing the
        user's input from the request itself.

        :param challenge: The Challenge object from the database
        :param request: The request the user submitted
        :return: (boolean, string)
        """
        data = request.form or request.get_json()
        submission = data["submission"].strip()
        # flags = Flags.query.filter_by(challenge_id=challenge.id).all()
        # Todo: change this to another way
        user_id = get_mode()

        flag = GlowwormContainers.query.filter_by(user_id=user_id, challenge_id=challenge.id).first()
        print(flag)


        if get_flag_class(flag.type).compare(flag, submission):
            return True, "Correct"
        else:
            return False, "Incorrect"

    @staticmethod
    def solve(user, team, challenge, request):
        """
        This method is used to insert Solves into the database in order to mark a challenge as solved.

        :param team: The Team object from the database
        :param chal: The Challenge object from the database
        :param request: The request the user submitted
        :return:
        """
        chal = ADAChallenge.query.filter_by(id=challenge.id).first()
        data = request.form or request.get_json()
        submission = data["submission"].strip()

        Model = get_model()

        solve = Solves(
            user_id=user.id,
            team_id=team.id if team else None,
            challenge_id=challenge.id,
            ip=get_ip(req=request),
            provided=submission,
        )
        db.session.add(solve)

        solve_count = (
            Solves.query.join(Model, Solves.account_id == Model.id)
                .filter(
                Solves.challenge_id == challenge.id,
                Model.hidden == False,
                Model.banned == False,
            )
                .count()
        )

        # We subtract -1 to allow the first solver to get max point value
        solve_count -= 1


        # It is important that this calculation takes into account floats.
        # Hence this file uses from __future__ import division
        value = (
                        ((chal.minimum - chal.initial) / (chal.decay ** 2)) * (solve_count ** 2)
                ) + chal.initial

        value = math.ceil(value)

        if value < chal.minimum:
            value = chal.minimum

        chal.value = value

        db.session.commit()
        db.session.close()

    @staticmethod
    def fail(user, team, challenge, request):
        """
        This method is used to insert Fails into the database in order to mark an answer incorrect.

        :param team: The Team object from the database
        :param challenge: The Challenge object from the database
        :param request: The request the user submitted
        :return:
        """
        data = request.form or request.get_json()
        submission = data["submission"].strip()
        wrong = Fails(
            user_id=user.id,
            team_id=team.id if team else None,
            challenge_id=challenge.id,
            ip=get_ip(request),
            provided=submission,
        )
        db.session.add(wrong)
        db.session.commit()
        db.session.close()


class ADAChallenge(Challenges):
    __mapper_args__ = {"polymorphic_identity": "ada_challenge"}
    id = db.Column(None, db.ForeignKey("challenges.id"), primary_key=True)

    dirname = db.Column(db.String(80))
    check_value = db.Column(db.Integer, default=0)

    cpu_limit = db.Column(db.String(5))
    memory_limit = db.Column(db.String(10))

    env_type = db.Column(db.String(10))
    env_language = db.Column(db.String(10))
    env_status = db.Column(db.Boolean, default=False)
    env_build_status = db.Column(db.Boolean, default=False)
    env_check_status = db.Column(db.Boolean, default=False)
    env_port = db.Column(db.String(10))

    def __init__(self, *args, **kwargs):
        super(ADAChallenge, self).__init__(**kwargs)
        self.initial = kwargs["value"]

class GlowwormConfigs(db.Model):
    key = db.Column(db.String(length=128), primary_key=True)
    value = db.Column(db.Text)

    def __init__(self, key, value):
        self.key = key
        self.value = value

class GlowwormContainers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"))
    docker_id = db.Column(db.String(32), unique=True)
    ip = db.Column(db.String(32))
    service_port = db.Column(db.Integer)
    ssh_port = db.Column(db.Integer)
    ssh_key = db.Column(db.String(32))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    flag = db.Column(db.String(128), nullable=True)
    key = db.Column(db.String(32))

    # Todo 数据库预留可视化信息

    # Relationships
    challenge = db.relationship(
        "Challenges", foreign_keys="GlowwormContainers.challenge_id", lazy="select"
    )

    def __init__(self, *args, **kwargs):
        super(GlowwormContainers, self).__init__(**kwargs)

class GlowwormAttacks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attack_id = db.Column(db.Integer)
    victim_id = db.Column(db.Integer)
    docker_id = db.Column(db.Integer, db.ForeignKey('glowworm_containers.docker_id'))

    envname = db.Column(db.String(72), db.ForeignKey('challenges.name'))
    flag = db.Column(db.String(128))
    round = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    # Todo 数据库预留可视化信息

    def __init__(self, *args, **kwargs):
        super(GlowwormAttacks, self).__init__(**kwargs)
