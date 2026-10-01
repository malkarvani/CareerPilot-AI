from datetime import datetime

from models import db


class ActivityLog(db.Model):

    __tablename__ = "activity_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    action = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    endpoint = db.Column(
        db.String(200),
        nullable=True
    )

    method = db.Column(
        db.String(20),
        nullable=True
    )

    ip_address = db.Column(
        db.String(50),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "activity_logs",
            lazy=True
        )
    )

    def __repr__(self):
        return f"<ActivityLog {self.action} user={self.user_id}>"