from app.extensions import db


class League(db.Model):
    __tablename__ = 'leagues'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    league_id = db.Column(db.Integer)
    espn_s2 = db.Column(db.String(400))
    swid = db.Column(db.String(40))
    nickname = db.Column(db.String(25))

    def __repr__(self):
        return '<User %r>' % self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id)
