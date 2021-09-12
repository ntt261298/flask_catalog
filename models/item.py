from app import db


class ItemModel(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.relationship('CategoryModel', backref=db.backref('items', lazy=True))

    def __repr__(self):
        return '<Item %r>' % self.title

    def json(self):
        return {'id': self.id, 'title': self.title, 'content': self.content}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
