"""
Enhanced Login System Module
Handles three-portal authentication and session management
"""

import streamlit as st
from datetime import datetime, timedelta
import json

class LoginManager:
    """Manage login sessions and authentication"""
    
    def __init__(self, db):
        self.db = db
        self.session_timeout = 3600  # 1 hour
    
    def initialize_session(self):
        """Initialize session state for login"""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.username = None
            st.session_state.login_time = None
            st.session_state.last_activity = None
    
    def login(self, username, password, role):
        """
        Authenticate user and create session
        
        Args:
            username: User's username
            password: User's password
            role: Expected role (student, parent, counselor)
        
        Returns:
            bool: True if login successful
        """
        user_info = self.db.authenticate(username, password)
        
        if user_info and user_info['role'] == role:
            st.session_state.authenticated = True
            st.session_state.user = user_info
            st.session_state.role = role
            st.session_state.username = username
            st.session_state.login_time = datetime.now()
            st.session_state.last_activity = datetime.now()
            return True
        
        return False
    
    def logout(self):
        """Clear session and logout user"""
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.login_time = None
        st.session_state.last_activity = None
    
    def check_session_timeout(self):
        """Check if session has timed out"""
        if st.session_state.authenticated and st.session_state.login_time:
            elapsed = datetime.now() - st.session_state.login_time
            if elapsed.total_seconds() > self.session_timeout:
                self.logout()
                st.warning("⏱️ Your session has expired. Please login again.")
                st.rerun()
    
    def update_activity(self):
        """Update last activity timestamp"""
        if st.session_state.authenticated:
            st.session_state.last_activity = datetime.now()
    
    def get_session_info(self):
        """Get current session information"""
        if not st.session_state.authenticated:
            return None
        
        login_time = st.session_state.login_time
        last_activity = st.session_state.last_activity
        elapsed = datetime.now() - login_time if login_time else None
        
        return {
            'user': st.session_state.user,
            'role': st.session_state.role,
            'login_time': login_time,
            'last_activity': last_activity,
            'elapsed_time': elapsed
        }

class RoleBasedAccess:
    """Handle role-based access control"""
    
    ROLES = {
        'student': {
            'pages': ['dashboard', 'counselor_chat', 'resources'],
            'features': ['view_own_data', 'request_counselor', 'message_counselor'],
            'permissions': {
                'view_own_data': True,
                'view_peers_data': False,
                'view_all_students': False,
                'manage_sessions': False,
                'manage_users': False
            }
        },
        'parent': {
            'pages': ['child_dashboard', 'messages', 'alerts'],
            'features': ['view_child_data', 'request_meeting', 'message_counselor'],
            'permissions': {
                'view_own_data': True,
                'view_child_data': True,
                'view_all_students': False,
                'manage_sessions': False,
                'manage_users': False
            }
        },
        'counselor': {
            'pages': ['dashboard', 'student_management', 'notes', 'analytics'],
            'features': ['view_all_students', 'manage_sessions', 'create_notes', 'generate_reports'],
            'permissions': {
                'view_own_data': True,
                'view_all_students': True,
                'manage_sessions': True,
                'manage_users': False,
                'generate_reports': True
            }
        }
    }
    
    @classmethod
    def check_permission(cls, role, permission):
        """Check if role has permission"""
        if role not in cls.ROLES:
            return False
        return cls.ROLES[role]['permissions'].get(permission, False)
    
    @classmethod
    def get_accessible_pages(cls, role):
        """Get list of accessible pages for role"""
        if role not in cls.ROLES:
            return []
        return cls.ROLES[role]['pages']
    
    @classmethod
    def get_features(cls, role):
        """Get available features for role"""
        if role not in cls.ROLES:
            return []
        return cls.ROLES[role]['features']
    
    @classmethod
    def can_access(cls, role, resource_type):
        """Check if role can access resource"""
        return cls.check_permission(role, resource_type)

# Usage example:
# from login_system import LoginManager, RoleBasedAccess
# from database import db
# 
# login_manager = LoginManager(db)
# login_manager.initialize_session()
# 
# if login_manager.login("student_001", "student123", "student"):
#     st.success("Login successful!")
#     role = st.session_state.role
#     if RoleBasedAccess.check_permission(role, 'view_own_data'):
#         st.write("Access granted to view your data")
