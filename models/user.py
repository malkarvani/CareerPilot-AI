from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_login import UserMixin

from models import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    education = db.Column(
        db.Text,
        nullable=True
    )

    skills = db.Column(
        db.Text,
        nullable=True
    )

    experience = db.Column(
        db.Text,
        nullable=True
    )

    interests = db.Column(
        db.Text,
        nullable=True
    )

    career_goal = db.Column(
        db.String(200),
        nullable=True
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    profile_image = db.Column(
        db.String(255),
        nullable=True
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )


    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )


    def __repr__(self):

        return f"<User {self.email}>"