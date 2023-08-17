import datetime as dt
import espn_api.football as fb

from espn_api.requests.espn_requests import ESPNInvalidLeague, ESPNAccessDenied, ESPNUnknownError
from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_required

from . import leagues
from .forms import LeagueForm, LeagueEditForm
from ..extensions import db
from ..models.leagues import League
from ..models.main import User

user = {'name': 'Andrew Edmonds'}


@leagues.route('/leagues')
@login_required
def my_leagues():
    usr = User.query.filter_by(name=user['name']).first()
    league_data = League.query.filter_by(user_id=usr.id).all()
    return render_template('leagues/my_leagues.html', user=user, league_data=league_data)


@leagues.route('/leagues/<league_id>')
@login_required
def view(league_id):
    league_data = League.query.filter_by(league_id=league_id).first()
    return render_template('leagues/view.html', league_data=league_data)


@leagues.route('/leagues/add', methods=['GET', 'POST'])
@login_required
def add():
    form = LeagueForm()
    if form.validate_on_submit():
        if _league_exists():
            flash('League already exists')
            return redirect(url_for('leagues.add'))

        if not _valid_league_params(
                league_id=int(request.form.get('league_id')),
                espn_s2=request.form.get('espn_s2'),
                swid=request.form.get('swid')
        ):
            flash('Invalid league parameters. Unable to load valid league using provided parameters')
            return redirect(url_for('leagues.add'))

        league = League(
            user_id=session['user_id'],
            league_id=int(request.form.get('league_id')),
            espn_s2=request.form.get('espn_s2'),
            swid=request.form.get('swid'),
            nickname=request.form.get('nickname'),
        )
        db.session.add(league)
        db.session.commit()
        flash('League added successfully!')
        return redirect(url_for('leagues.my_leagues'))
    return render_template('leagues/add.html', form=form)


@leagues.route('/leagues/edit/<league_id>', methods=['GET', 'POST'])
@login_required
def edit(league_id):
    form = LeagueEditForm()
    league = League.query.filter_by(league_id=league_id).first()
    if request.method == 'GET':
        form.league_id.data = league.league_id
        form.espn_s2.data = league.espn_s2
        form.swid.data = league.swid
        form.nickname.data = league.nickname

    if form.validate_on_submit():
        if not _valid_league_params(
                league_id=int(request.form.get('league_id', league.league_id, type=int)),
                espn_s2=request.form.get('espn_s2', league.espn_s2),
                swid=request.form.get('swid', league.swid)
        ):
            flash('Invalid league parameters. Unable to load valid league using provided parameters')
            return redirect(url_for('leagues.add'))

        league = League.query.filter_by(league_id=league_id).first()
        league.league_id = request.form.get('league_id') or league.league_id
        league.espn_s2 = request.form.get('espn_s2') or league.espn_s2
        league.swid = request.form.get('swid') or league.swid
        league.nickname = request.form.get('nickname') or league.nickname

        db.session.commit()
        flash('League updated updated')
        return redirect(url_for('leagues.my_leagues'))
    return render_template('leagues/edit.html', form=form)


@leagues.route('/leagues/delete/<league_id>')
@login_required
def delete(league_id):
    return render_template('leagues/delete.html', league_id=league_id)


@leagues.route('/leagues/delete/<league_id>/confirm')
@login_required
def delete_post(league_id):
    League.query.filter_by(league_id=league_id).delete()
    db.session.commit()
    flash('League successfully deleted!')
    return redirect(url_for('leagues.my_leagues'))


def _league_exists():
    league = League.query.filter_by(
        user_id=session['user_id'],
        league_id=int(request.form.get('league_id')),
        espn_s2=request.form.get('espn_s2'),
        swid=request.form.get('swid'),
    ).first()
    return None if not league else league


def _valid_league_params(league_id: int, espn_s2: str, swid: str):
    valid_params = False
    earliest_year = 2000

    for year in reversed(range(earliest_year, dt.date.today().year)):
        try:
            fb.League(
                league_id=league_id,
                year=year,
                espn_s2=espn_s2,
                swid=swid
            )
            valid_params = True
            break
        except (ESPNInvalidLeague, ESPNAccessDenied, ESPNUnknownError):
            continue
    return valid_params
