"""
Database Management & Authentication
Handles user credentials and role-based access
"""

import json
import hashlib
import os
from datetime import datetime

class Database:
    def __init__(self, db_file="app_database.json"):
        self.db_file = db_file
        self.load_or_create_db()
    
    def load_or_create_db(self):
        """Load existing database or create new one"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.db = json.load(f)
        else:
            self.db = {
                "users": {},
                "sessions": {},
                "counseling_notes": [],
                "messages": []
            }
            self.initialize_default_users()
            self.save_db()
    
    def initialize_default_users(self):
        """Create default users for demo"""
        default_users = {
            # 3 Sample Students
            "student_001": {
                "role": "student",
                "password": self.hash_password("student123"),
                "name": "Arjun Sharma",
                "email": "arjun@vignan.ac.in",
                "student_id": "2310001",
                "created_at": datetime.now().isoformat()
            },
            "student_002": {
                "role": "student",
                "password": self.hash_password("student123"),
                "name": "Priya Singh",
                "email": "priya@vignan.ac.in",
                "student_id": "2310002",
                "created_at": datetime.now().isoformat()
            },
            "student_003": {
                "role": "student",
                "password": self.hash_password("student123"),
                "name": "Karan Patel",
                "email": "karan@vignan.ac.in",
                "student_id": "2310003",
                "created_at": datetime.now().isoformat()
            },
            # 2 Sample Parents
            "parent_001": {
                "role": "parent",
                "password": self.hash_password("parent123"),
                "name": "Rajesh Sharma",
                "email": "rajesh.parent@email.com",
                "child_student_id": "2310001",
                "phone": "9876543210",
                "created_at": datetime.now().isoformat()
            },
            "parent_002": {
                "role": "parent",
                "password": self.hash_password("parent123"),
                "name": "Sunita Singh",
                "email": "sunita.parent@email.com",
                "child_student_id": "2310002",
                "phone": "9876543211",
                "created_at": datetime.now().isoformat()
            },
            # 3 Sample Counselors
            "counselor_001": {
                "role": "counselor",
                "password": self.hash_password("counselor123"),
                "name": "Dr. Ananya Verma",
                "email": "ananya@vignan.ac.in",
                "specialization": "Academic Guidance",
                "expertise": ["Time Management", "Study Skills", "Career Guidance"],
                "created_at": datetime.now().isoformat()
            },
            "counselor_002": {
                "role": "counselor",
                "password": self.hash_password("counselor123"),
                "name": "Prof. Rajesh Kumar",
                "email": "rajesh@vignan.ac.in",
                "specialization": "Mental Health & Wellness",
                "expertise": ["Stress Management", "Anxiety", "Depression", "Work-Life Balance"],
                "created_at": datetime.now().isoformat()
            },
            "counselor_003": {
                "role": "counselor",
                "password": self.hash_password("counselor123"),
                "name": "Ms. Shreya Nair",
                "email": "shreya@vignan.ac.in",
                "specialization": "Career & Placement",
                "expertise": ["Job Preparation", "Interview Skills", "Internships"],
                "created_at": datetime.now().isoformat()
            }
        }
        self.db["users"] = default_users
    
    @staticmethod
    def hash_password(password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def save_db(self):
        """Save database to file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.db, f, indent=2)
    
    def authenticate(self, username, password):
        """Authenticate user"""
        if username not in self.db["users"]:
            return None
        
        user = self.db["users"][username]
        if user["password"] == self.hash_password(password):
            return {
                "username": username,
                "role": user["role"],
                "name": user["name"],
                "email": user["email"],
                "authenticated": True
            }
        return None
    
    def get_user(self, username):
        """Get user details"""
        return self.db["users"].get(username)
    
    def add_counseling_note(self, counselor_id, student_id, note, note_type="general"):
        """Add counseling note"""
        note_entry = {
            "id": len(self.db["counseling_notes"]) + 1,
            "counselor_id": counselor_id,
            "student_id": student_id,
            "note": note,
            "note_type": note_type,  # general, academic, mental_health, career
            "timestamp": datetime.now().isoformat(),
            "follow_up_date": None
        }
        self.db["counseling_notes"].append(note_entry)
        self.save_db()
        return note_entry
    
    def add_message(self, sender_id, receiver_id, message, message_type="text"):
        """Add message (chat history)"""
        msg_entry = {
            "id": len(self.db["messages"]) + 1,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "message_type": message_type,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        self.db["messages"].append(msg_entry)
        self.save_db()
        return msg_entry
    
    def get_counseling_notes(self, student_id):
        """Get counseling notes for student"""
        return [n for n in self.db["counseling_notes"] if n["student_id"] == student_id]
    
    def get_messages(self, user_id, role):
        """Get messages for user"""
        if role == "student":
            return [m for m in self.db["messages"] if m["receiver_id"] == user_id or m["sender_id"] == user_id]
        elif role == "counselor":
            return [m for m in self.db["messages"] if m["receiver_id"] == user_id or m["sender_id"] == user_id]
        return []

# Initialize database
db = Database()
