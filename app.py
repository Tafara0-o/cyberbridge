from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import json
from ai_trainer import generate_training_module, get_fallback_content

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cyberbridge.db"
app.config["SECRET_KEY"] = "dev-key-change-this"

db = SQLAlchemy(app)

# ===== MODELS =====
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

# ===== ROUTES =====
@app.route("/")
def index():
    return render_template("risk-profile.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/training")
def training_page():
    return render_template("training.html")

@app.route("/api/user/register", methods=["POST"])
def register_user():
    data = request.json
    user = User(
        email=data["email"],
        organization=data.get("organization", "Demo Org"),
        industry=data.get("industry", "General"),
        role=data.get("role", "Employee"),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"user_id": user.id, "message": "User created"}), 201

# ===== DASHBOARD ENDPOINTS =====

@app.route("/api/dashboard/metrics/<int:user_id>", methods=["GET"])
def dashboard_metrics(user_id):
    """Return dashboard KPIs and training progress"""
    user = User.query.get_or_404(user_id)
    sessions = TrainingSession.query.filter_by(user_id=user_id).all()

    completed = sum(1 for s in sessions if s.completion_status == "completed")
    total = len(sessions) if len(sessions) > 0 else 4  # Default 4 modules
    avg_quiz = (
        sum((s.quiz_score or 0) for s in sessions) / completed 
        if completed > 0 else 0
    )

    timeline = [
        {"date": "Day 1", "completed": 0},
        {"date": "Day 2", "completed": 1},
        {"date": "Day 3", "completed": 2},
        {"date": "Day 4", "completed": completed},
    ]

    return jsonify(
        {
            "user": {
                "email": user.email,
                "organization": user.organization,
                "role": user.role,
                "industry": user.industry,
            },
            "kpis": {
                "training_completion": {
                    "completed": completed,
                    "total": total,
                    "percentage": (completed / total * 100) if total > 0 else 0,
                },
                "average_quiz_score": round(avg_quiz, 1),
                "risk_score": user.risk_score,
            },
            "completion_timeline": timeline,
            "modules": [
                {
                    "id": s.id,
                    "name": s.module_name,
                    "status": s.completion_status,
                    "score": s.quiz_score,
                }
                for s in sessions
            ],
        }
    )

@app.route("/api/dashboard/alerts", methods=["GET"])
def dashboard_alerts():
    """Return security alerts for dashboard"""
    return jsonify(
        {
            "alerts": [
                {
                    "type": "info",
                    "message": "📚 Complete Phishing Awareness module this week.",
                },
                {
                    "type": "warning",
                    "message": "⚠️ Password Security score is below 70%.",
                },
                {
                    "type": "success",
                    "message": "🎉 Great job completing 3 out of 4 modules!",
                },
            ]
        }
    )

# ===== TRAINING ENDPOINTS =====

TRAINING_MODULES = [
    "Phishing Awareness",
    "Password Security",
    "Ransomware Prevention",
    "Data Protection Basics",
]

@app.route("/api/training/modules", methods=["GET"])
def list_training_modules():
    """List available training modules"""
    return jsonify({"modules": TRAINING_MODULES})

@app.route("/api/training/start", methods=["POST"])
def start_training():
    """Start a training session with AI-generated content"""
    data = request.json
    user_id = data["user_id"]
    module_name = data["module_name"]

    # Get user info for personalization
    user = User.query.get_or_404(user_id)

    user_profile = {
        "role": user.role or "Employee",
        "industry": user.industry or "General",
        "tech_level": "beginner",
    }

    # Try to generate AI content
    print(f"\n📚 Starting training: {module_name} for {user.email}")
    content = generate_training_module(module_name, user_profile)

    # Use fallback if AI fails
    if content is None:
        print(f"⚠️ Using fallback content for {module_name}")
        content = get_fallback_content(module_name)

    # Create training session
    session = TrainingSession(
        user_id=user_id,
        module_name=module_name,
        content=json.dumps(content),
        completion_status="in_progress",
        started_at=datetime.utcnow(),
    )
    db.session.add(session)
    db.session.commit()

    print(f"✅ Training session created: {session.id}")

    return jsonify({
        "session_id": session.id,
        "content": content
    }), 201

@app.route("/api/training/complete", methods=["POST"])
def complete_training():
    """Mark training complete with quiz score"""
    data = request.json
    session_id = data["session_id"]
    quiz_score = data["quiz_score"]

    session = TrainingSession.query.get_or_404(session_id)
    session.completion_status = "completed"
    session.quiz_score = quiz_score
    session.completed_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "Training completed", "score": quiz_score})

# ===== DEMO/SEED ENDPOINT (FOR SYNCFLOW DEMO) =====

@app.route("/api/seed-syncflow-demo", methods=["POST"])
def seed_syncflow():
    """Populate SyncFlow demo data"""
    try:
        # Clear existing data
        TrainingSession.query.delete()
        User.query.delete()
        db.session.commit()

        # Create SyncFlow user (IT Manager)
        user = User(
            email="alice.smith@syncflowsolutions.com",
            organization="SyncFlow Solutions",
            industry="Professional Services",
            role="IT Manager",
            risk_score=45
        )
        db.session.add(user)
        db.session.commit()

        # Create training sessions with demo data
        modules_data = [
            ("Phishing Awareness", "completed", 88),
            ("Password Security", "completed", 85),
            ("Ransomware Prevention", "in_progress", None),
            ("Data Protection Basics", "not_started", None),
        ]

        for module_name, status, score in modules_data:
            session = TrainingSession(
                user_id=user.id,
                module_name=module_name,
                content=json.dumps({
                    "title": module_name,
                    "introduction": f"Training module on {module_name}",
                    "key_concepts": [],
                    "real_world_examples": [],
                    "best_practices": [],
                    "quiz": []
                }),
                completion_status=status,
                quiz_score=score,
                started_at=datetime.utcnow() if status != "not_started" else None,
                completed_at=datetime.utcnow() if status == "completed" else None
            )
            db.session.add(session)

        db.session.commit()

        return jsonify({
            "message": "SyncFlow demo data loaded",
            "user_id": user.id,
            "email": user.email
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error in seed_syncflow: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/risk-profile")
def risk_profile():
    """Risk profile setup page"""
    return render_template("risk-profile.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, port=5000)
