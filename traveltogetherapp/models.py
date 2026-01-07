from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    # Optional display alias shown across the site (e.g., "Alex", "Traveller123")
    alias = db.Column(db.String(50), nullable=True)
    # Role: 'user', 'editor', 'authority', or 'admin'
    role = db.Column(db.String(20), nullable=False, default='user')
    # RFID card ID for time logging via scanner
    rfid = db.Column(db.String(100), nullable=True)

    def is_editor(self):
        return (self.role or 'user') in ('editor', 'admin')

    def is_authority(self):
        return (self.role or 'user') in ('authority', 'admin')


class TimeEntry(db.Model):
    """Simple time tracking entries for project work.

    start_time: UTC datetime when timer was started
    end_time: UTC datetime when timer was stopped (nullable while running)
    duration_minutes: integer duration in minutes (computed on stop)
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)  # erstatter sekunder

    user = db.relationship("User", backref="time_entries", lazy=True)


# Ny modell for manuell dagsjustering (uten sekunder)
class DailyAdjustment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_minutes = db.Column(db.Integer, nullable=False)  # kun minutter
    edited_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='_user_date_uc'),)
