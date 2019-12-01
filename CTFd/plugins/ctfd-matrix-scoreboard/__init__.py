from flask import render_template, jsonify, Blueprint, session, redirect, url_for, request
from CTFd import utils, scoreboard, challenges
from CTFd.plugins import override_template
from CTFd.models import db, Teams, Users, Solves, Awards, Challenges
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
        standings = scoreboard.get_standings()
        # TODO faster lookup here
        jstandings = []
        # print(standings)
        for team in standings:
            print(team)
            teamid = team[0]
            # To do 区分模式
            solves = db.session.query(Solves.challenge_id.label('chalid'), Solves.date.label('date')).filter(Solves.team_id==teamid)

            freeze = utils.get_config('freeze')
            if freeze:
                freeze = utils.unix_time_to_utc(freeze)
                if teamid != session.get('id'):
                    solves = solves.filter(Solves.date < freeze)
            solves = solves.all()

            jsolves = []
            score = 0
            for solve in solves:
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

            mode = utils.get_config("user_mode")
            if mode == "teams":
                jstandings.append({'userid':"", 'teamid':team[0], 'score':score, 'name':team[2],'solves':jsolves})
            else:
                jstandings.append({'userid':team[0], 'teamid':"", 'score':score, 'name':team[2],'solves':jsolves})
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


    def scoreboard_view():
        if utils.get_config('view_scoreboard_if_authed') and not utils.authed():
            return redirect(url_for('auth.login', next=request.path))
        if utils.hide_scores():
            return render_template('scoreboard.html',
                    errors=['Scores are currently hidden'])
        standings = get_standings()
        return render_template('scoreboard.html', teams=standings,
            score_frozen=utils.is_scoreboard_frozen(), challenges=get_challenges())

    def scores():
        json = {'standings': []}
        if utils.get_config('view_scoreboard_if_authed') and not utils.authed():
            return redirect(url_for('auth.login', next=request.path))
        if utils.hide_scores():
            return jsonify(json)

        standings = get_standings()

        for i, x in enumerate(standings):
            json['standings'].append({'pos': i + 1, 'id': x['name'], 'team': x['name'],
                'score': int(x['score']), 'solves':x['solves']})
        return jsonify(json)

    app.register_blueprint(matrix_blueprint)