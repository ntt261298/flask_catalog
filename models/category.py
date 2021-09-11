from app import db


class CategoryModel(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

    def json(self):
        return {'id': self.id, 'name': self.name}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
