from enum import unique
from app import db


class AuthData(db.Model):
    __tablename__ = "auth_data"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(12), nullable=False, unique=True)
    code = db.Column(db.String(6), nullable=False)