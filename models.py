from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    organization = db.Column(db.String(200))
    industry = db.Column(db.String(100))
    role = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    risk_score = db.Column(db.Float, default=0.0)

class TrainingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    module_name = db.Column(db.String(200))
    content = db.Column(db.Text)  # JSON string
    completion_status = db.Column(db.String(50), default="not_started")
    quiz_score = db.Column(db.Float)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
