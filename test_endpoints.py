#!/usr/bin/env python
"""Test script for CyberBridge API endpoints"""

from app import app, db, User, TrainingSession
from datetime import datetime
import json

# Create app context
with app.app_context():
    # Initialize database
    db.create_all()
    
    # Seed demo data
    TrainingSession.query.delete()
    User.query.delete()
    db.session.commit()
    
    user = User(
        email="alice.smith@syncflowsolutions.com",
        organization="SyncFlow Solutions",
        industry="Professional Services",
        role="IT Manager",
        risk_score=45
    )
    db.session.add(user)
    db.session.commit()
    
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
    
    print("✅ Demo data seeded successfully!")
    print(f"   User ID: {user.id}")
    print(f"   Email: {user.email}")
    print(f"   Organization: {user.organization}")
    
    # Test endpoints with test client
    client = app.test_client()
    
    print("\n" + "="*50)
    print("TEST 1: Dashboard Metrics")
    print("="*50)
    response = client.get(f'/api/dashboard/metrics/{user.id}')
    metrics = response.get_json()
    print(json.dumps(metrics, indent=2, default=str))
    
    print("\n" + "="*50)
    print("TEST 2: Dashboard Alerts")
    print("="*50)
    response = client.get('/api/dashboard/alerts')
    alerts = response.get_json()
    print(json.dumps(alerts, indent=2, default=str))
    
    print("\n" + "="*50)
    print("TEST 3: Training Modules")
    print("="*50)
    response = client.get('/api/training/modules')
    modules = response.get_json()
    print(json.dumps(modules, indent=2, default=str))
    
    print("\n✅ All tests completed successfully!")
