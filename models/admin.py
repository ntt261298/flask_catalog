from app import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    password_salt = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.username
