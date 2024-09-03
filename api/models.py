from flask_sqlalchemy import SQLAlchemy
from .modules import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, username, name, password_hash):
        self.username = username
        self.name = name
        self.password_hash = password_hash

    def __repr__(self):
        return f'<User {self.username}>'
