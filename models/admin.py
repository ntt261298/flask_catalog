from app import db


class AdminModel(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.username
