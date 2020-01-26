from flask import render_template, jsonify, Blueprint, session, redirect, url_for, request
from CTFd import utils, scoreboard, challenges
from CTFd.plugins import override_template
from CTFd.models import db, Teams, Users, Solves, Awards, Challenges
from sqlalchemy.sql.expression import union_all
from CTFd.cache import cache
from CTFd.utils import get_config
from CTFd.utils.modes import get_model
from CTFd.utils.dates import unix_time_to_utc
from CTFd.utils.decorators.visibility import check_score_visibility
from sqlalchemy.sql import or_
from werkzeug.routing import Rule
import json, time
import itertools
import os


def load(app):

    matrix_blueprint = Blueprint(
        "matrix-scoreboard",
        __name__,
        template_folder="templates",
        static_folder='static',
        url_prefix='/matrix'
    )

    @matrix_blueprint.route("/")
    @check_score_visibility
    def matrix():
        standings = get_standings()
        return render_template('scoreboard-matrix.html', teams=standings,
            score_frozen=utils.config.is_scoreboard_frozen(), challenges=get_challenges())
    @matrix_blueprint.route("/scores")
    @check_score_visibility
    def scores():
        return jsonify(get_standings())
    def get_standings():
        standings = glowworm_get_standings()
        # TODO faster lookup here
        jstandings = []
        print(standings)
        for team in standings:
            mode = utils.get_config("user_mode")
            if mode == "teams":
                teamid = team[0]
                basic_solves = db.session.query(Solves.challenge_id.label('chalid'), Solves.date.label('date')).filter(
                    Solves.team_id == teamid)
            else:
                teamid = team[0]
                basic_solves = db.session.query(Solves.challenge_id.label('chalid'), Solves.date.label('date')).filter(
                    Solves.user_id == teamid)

            freeze = utils.get_config('freeze')
            if freeze:
                freeze = utils.unix_time_to_utc(freeze)
                if teamid != session.get('id'):
                    basic_solves = basic_solves.filter(Solves.date < freeze)
            basic_solves = basic_solves.all()

            jsolves = []
            score = 0 + team[3]
            # basic challenge
            # 1 first blood
            # 2 second blood
            # 3 third blood
            for solve in basic_solves:
                cvalue = Challenges.query.filter_by(id=solve.chalid).first().value
                top = Solves.query.filter_by(challenge_id=solve.chalid, type='correct').order_by(Solves.date.asc()).all()
                if(solve.date == top[0].date):
                    solve = str(solve.chalid) + "-1"
                    score = score + int(cvalue * 1.3)
                elif(solve.date == top[1].date):
                    solve = str(solve.chalid) + "-2"
                    score = score + int(cvalue * 1.2)
                elif(solve.date == top[2].date):
                    solve = str(solve.chalid) + "-3"
                    score = score + int(cvalue * 1.1)
                else:
                    solve = str(solve.chalid) + "-0"
                    score = score + int(cvalue * 1)
                jsolves.append(solve)
            # ada challenge
            # 4 safe
            # 5 hacked
            try:
                from CTFd.plugins.ctfd_glowworm.models import GlowwormAttacks, ADAChallenge
                from CTFd.plugins.ctfd_glowworm.extensions import get_round
                all_challenges = ADAChallenge.query.all()
                for challenge in all_challenges:
                    envname = challenge.dirname.split('/')[1]
                    log = GlowwormAttacks.query.filter_by(round=get_round(), victim_id=teamid, envname=envname).first()
                    if log == None:
                        solve = str(challenge.id) + "-4"
                        pass
                    elif envname == log.envname:
                        solve = str(challenge.id) + "-5"
                        pass
                    jsolves.append(solve)
            except Exception as e:
                print(e)

            if mode == "teams":
                jstandings.append({'userid':"", 'teamid':team[0], 'score':int(score), 'name':team[2],'solves':jsolves})
            else:
                jstandings.append({'userid':team[0], 'teamid':"", 'score':int(score), 'name':team[2],'solves':jsolves})
        # 重新按分数排序
        jstandings.sort(key=lambda x: x["score"], reverse=True)
        db.session.close()
        return jstandings


    def get_challenges():
        if not utils.user.is_admin():
            if not utils.dates.ctftime():
                if utils.dates.view_after_ctf():
                    pass
                else:
                    return []
        if utils.config.visibility.challenges_visible() and (utils.dates.ctf_started() or utils.user.is_admin()):
            chals = db.session.query(
                    Challenges.id,
                    Challenges.name,
                    Challenges.category,
                    Challenges.value
                ).filter(or_(Challenges.state != "hidden", Challenges.state == None)).all()
            jchals = []
            for x in chals:
                jchals.append({
                    'id':x.id,
                    'name':x.name,
                    'category':x.category,
                    'value' : x.value
                })

            # Sort into groups
            categories = set(map(lambda x:x['category'], jchals))
            # print(categories)
            jchals = [j for c in categories for j in jchals if j['category'] == c]

            return jchals
        return []




    @cache.memoize(timeout=60)
    def glowworm_get_standings(count=None, admin=False):
        """
        Get standings as a list of tuples containing account_id, name, and score e.g. [(account_id, team_name, score)].

        Ties are broken by who reached a given score first based on the solve ID. Two users can have the same score but one
        user will have a solve ID that is before the others. That user will be considered the tie-winner.

        Challenges & Awards with a value of zero are filtered out of the calculations to avoid incorrect tie breaks.
        """
        Model = get_model()

        basic_scores = (
            db.session.query(
                Solves.account_id.label("account_id"),
                db.func.sum(0).label("score"),
                db.func.max(Solves.id).label("id"),
                db.func.max(Solves.date).label("date"),
            )
                .join(Challenges)
                .filter(Challenges.value != 0)
                .group_by(Solves.account_id)
        )

        awards = (
            db.session.query(
                Awards.account_id.label("account_id"),
                db.func.sum(Awards.value).label("score"),
                db.func.max(Awards.id).label("id"),
                db.func.max(Awards.date).label("date"),
            )
                .filter(Awards.value != 0)
                .group_by(Awards.account_id)
        )

        try:
            from CTFd.plugins.ctfd_glowworm.models import GlowwormAttackLog, ADAChallenge

            attack_scores = (
                db.session.query(
                    GlowwormAttackLog.account_id.label("account_id"),
                    db.func.sum(Challenges.value).label("score"),
                    db.func.max(GlowwormAttackLog.id).label("id"),
                    db.func.max(GlowwormAttackLog.date).label("date"),
                )
                    .join(Challenges)
                    .filter(Challenges.value != 0)
                    .group_by(GlowwormAttackLog.account_id)
            )

            from CTFd.plugins.ctfd_glowworm.models import GlowwormCheckLog
            check_scores = (
                db.session.query(
                    GlowwormCheckLog.account_id.label("account_id"),
                    (0-db.func.sum(ADAChallenge.check_value)).label("score"),
                    db.func.max(GlowwormCheckLog.id).label("id"),
                    db.func.max(GlowwormCheckLog.date).label("date"),
                )
                    .join(ADAChallenge)
                    .filter(Challenges.value != 0)
                    .group_by(GlowwormCheckLog.account_id)
            )
            from CTFd.plugins.ctfd_glowworm.models import GlowwormInitLog
            init_scores = (
                db.session.query(
                    GlowwormInitLog.account_id.label("account_id"),
                    (0 - db.func.sum(ADAChallenge.check_value)).label("score"),
                    db.func.max(GlowwormInitLog.id).label("id"),
                    db.func.max(GlowwormInitLog.date).label("date"),
                )
                    .join(ADAChallenge)
                    .filter(Challenges.value != 0)
                    .group_by(GlowwormInitLog.account_id)
            )

            """
                Filter out solves and awards that are before a specific time point.
                """
            freeze = get_config("freeze")
            if not admin and freeze:
                basic_scores = basic_scores.filter(Solves.date < unix_time_to_utc(freeze))
                awards = awards.filter(Awards.date < unix_time_to_utc(freeze))
                attack_scores = attack_scores.filter(GlowwormAttackLog.date < unix_time_to_utc(freeze))
                check_scores = check_scores.filter(GlowwormCheckLog.date < unix_time_to_utc(freeze))
                init_scores = init_scores.filter(GlowwormInitLog.date < unix_time_to_utc(freeze))

            """
            Combine awards and solves with a union. They should have the same amount of columns
            """
            results = union_all(basic_scores, awards, attack_scores, check_scores, init_scores).alias("results")
        except Exception as e:
            print(e)
            results = union_all(basic_scores, awards).alias("results")

        """
        Sum each of the results by the team id to get their score.
        """
        sumscores = (
            db.session.query(
                results.columns.account_id,
                db.func.sum(results.columns.score).label("score"),
                db.func.max(results.columns.id).label("id"),
                db.func.max(results.columns.date).label("date"),
            )
                .group_by(results.columns.account_id)
                .subquery()
        )

        """
        Admins can see scores for all users but the public cannot see banned users.

        Filters out banned users.
        Properly resolves value ties by ID.

        Different databases treat time precision differently so resolve by the row ID instead.
        """
        if admin:
            standings_query = (
                db.session.query(
                    Model.id.label("account_id"),
                    Model.oauth_id.label("oauth_id"),
                    Model.name.label("name"),
                    Model.hidden,
                    Model.banned,
                    sumscores.columns.score,
                )
                    .join(sumscores, Model.id == sumscores.columns.account_id)
                    .order_by(sumscores.columns.score.desc(), sumscores.columns.id)
            )
        else:
            standings_query = (
                db.session.query(
                    Model.id.label("account_id"),
                    Model.oauth_id.label("oauth_id"),
                    Model.name.label("name"),
                    sumscores.columns.score,
                )
                    .join(sumscores, Model.id == sumscores.columns.account_id)
                    .filter(Model.banned == False, Model.hidden == False)
                    .order_by(sumscores.columns.score.desc(), sumscores.columns.id)
            )

        """
        Only select a certain amount of users if asked.
        """
        if count is None:
            standings = standings_query.all()
        else:
            standings = standings_query.limit(count).all()

        return standings

    app.register_blueprint(matrix_blueprint)