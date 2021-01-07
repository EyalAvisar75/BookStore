from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_reader(id):
    return Reader.query.get(int(id))


class Reader(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String)
    books = db.relationship(
        'Book',
        backref='readers',
        lazy=True
    )

    def __init__(self, role='reader'):
        self.role = role

    def __repr__(self):
        return f"reader: {self.name}, {self.email}"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    date_entered = db.Column(db.DateTime, default=datetime.utcnow)
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'))

    def __repr__(self):
        return f"book: {self.title}, {self.author}"
