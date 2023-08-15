from flask import render_template
from flask_login import login_required, current_user
from . import main


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', name=current_user.name)
