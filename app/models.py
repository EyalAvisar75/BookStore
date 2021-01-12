from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_reader(id):
    return Reader.query.get(int(id))


carts = db.Table('carts',
                 db.Column('reader_id', db.Integer, db.ForeignKey('reader.id')),
                 db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
                 )


class Reader(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String)
    books = db.relationship(
        'Book',
        backref='readers',
        secondary=carts,
        lazy='dynamic'
    )

    def get_reset_token(self, expires_seconds=1800):
        from run import app
        from flask import flash
        flash(self.id)
        s = Serializer(app.secret_key, expires_seconds)
        return s.dump({'id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        from run import app
        s = Serializer(app.secret_key)
        try:
            reader_id = s.load(token)['id']
        except:
            return None

        return Reader.query.get(reader_id)

    def __init__(self, role='reader'):
        self.role = role

    def __repr__(self):
        return f"reader: {self.name}, {self.email}"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer)
    date_entered = db.Column(db.DateTime, default=datetime.utcnow)
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'))

    def __repr__(self):
        return f"book: {self.title}, {self.author}"

    def as_dict(self):
        return {'title': self.title}