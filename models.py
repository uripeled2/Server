# database setup
from mange import db
import uuid


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), unique=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(256))
    is_login = db.Column(db.Boolean, default=True)


class Activity(db.Model):

    __tablename__ = "activity"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(400))
    spot = db.Column(db.String(100))
    policy_type = db.Column(db.Integer)  # 0 = no, 1 = modertet, 2 = strict
    penalty_price = db.Column(db.Integer)
    penalty_time = db.Column(db.Integer)
    days = db.Column(db.JSON)   # {"sunday": True, "monday": True, ...} or {"1": True, "2": True, ...}
    time_step = db.Column(db.JSON)  # {"start": hour, "end": hour} or {1: {"0": hour, "1": hour}, 2...}
    weekly = db.Column(db.Boolean)

    # relationship handle
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=user_id)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'description': self.description,
            'spot': self.spot,
            'policy_type': self.policy_type,
            'penalty_price': self.penalty_price,
            'penalty_time': self.penalty_time,
            'days': self.days,
            'time_step': self.time_step,
            'weekly': self.weekly
        }
