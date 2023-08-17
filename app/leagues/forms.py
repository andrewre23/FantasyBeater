from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LeagueForm(FlaskForm):
    league_id = StringField('League ID', validators=[DataRequired()])
    espn_s2 = StringField('ESPN S2:', validators=[DataRequired()])
    swid = StringField('SWID (including brackets)', validators=[DataRequired()])
    nickname = StringField('League Nickname', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LeagueEditForm(FlaskForm):
    league_id = StringField('League ID')
    espn_s2 = StringField('ESPN S2:')
    swid = StringField('SWID (including brackets)')
    nickname = StringField('League Nickname')
    submit = SubmitField('Submit')
