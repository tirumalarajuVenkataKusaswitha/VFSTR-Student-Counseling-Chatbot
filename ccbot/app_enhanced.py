"""
Enhanced Vignan AI Counselor Bot - Three-Login System
Enterprise-grade student counseling system with Role-Based Access
"""

import streamlit as st
import os
from datetime import datetime
from database import db
from pages.student_dashboard import show_student_dashboard
from pages.parent_dashboard import show_parent_dashboard
from pages.counselor_dashboard import show_counselor_dashboard

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Vignan AI Counselor | Three-Portal System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.login_tab = "student"

# ============================================================
# ADVANCED CSS STYLING
# ============================================================
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 50px 20px;
        text-align: center;
        color: white;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .header-title {
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.1em;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Tab Styling */
    .tab-container {
        display: flex;
        gap: 10px;
        margin-bottom: 30px;
        justify-content: center;
    }
    
    .tab-button {
        padding: 12px 25px;
        border: 2px solid #ddd;
        background: white;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        font-size: 1em;
    }
    
    .tab-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .tab-button.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
    
    /* Login Card Styling */
    .login-card {
        max-width: 450px;
        margin: 30px auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    
    .login-form-title {
        text-align: center;
        color: #667eea;
        font-size: 1.8em;
        margin-bottom: 25px;
        font-weight: 700;
    }
    
    .role-icon {
        font-size: 3em;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .role-description {
        text-align: center;
        color: #666;
        font-size: 0.95em;
        margin-bottom: 25px;
        line-height: 1.5;
    }
    
    /* Credential Card */
    .credential-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .credential-label {
        font-weight: 600;
        font-size: 0.95em;
        opacity: 0.9;
        margin-bottom: 8px;
    }
    
    .credential-code {
        background: rgba(255,255,255,0.15);
        padding: 12px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        border-left: 3px solid white;
    }
    
    /* Sidebar Styling */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    .user-info-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin-bottom: 15px;
    }
    
    /* Button Styling */
    .btn-login {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 14px;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.1em;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .btn-login:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(102,126,234,0.4);
    }
    
    .btn-logout {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .btn-logout:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255,107,107,0.3);
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    .feature-icon {
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    
    /* Input Styling */
    .input-field {
        width: 100%;
        padding: 12px 15px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 1em;
        transition: all 0.3s ease;
        margin-bottom: 15px;
    }
    
    .input-field:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102,126,234,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# THREE-PORTAL LOGIN PAGE
# ============================================================
def show_three_portal_login():
    """Display three separate login portals for different roles"""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🎓 Vignan AI Counselor Platform</div>
        <div class="header-subtitle">Advanced Student Counseling, Academic Support & Parent Engagement System</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for the three login portals
    student_col, parent_col, counselor_col = st.columns(3, gap="large")
    
    # ============================================================
    # STUDENT LOGIN PORTAL
    # ============================================================
    with student_col:
        st.markdown("""
        <div class="login-card">
            <div class="role-icon">👤</div>
            <div class="login-form-title">Student Login</div>
            <div class="role-description">
                Access your personal dashboard, track academic progress, and connect with counselors
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("student_login_form"):
            st.markdown("**Student Portal**")
            student_username = st.text_input(
                "Username",
                placeholder="e.g., student_001",
                key="student_username"
            )
            student_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="student_password"
            )
            
            student_login_btn = st.form_submit_button(
                "🚀 Login as Student",
                use_container_width=True,
                type="primary"
            )
            
            if student_login_btn:
                if student_username and student_password:
                    user_info = db.authenticate(student_username, student_password)
                    if user_info and user_info['role'] == 'student':
                        st.session_state.authenticated = True
                        st.session_state.user = user_info
                        st.session_state.role = 'student'
                        st.session_state.username = student_username
                        st.session_state.student_id = user_info.get("student_id", "2310001")
                        st.success("✅ Login successful!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid student credentials!")
                else:
                    st.warning("⚠️ Please enter username and password")
        
        # Demo credentials
        st.markdown("""
        <div class="credential-card">
            <div class="credential-label">📋 Demo Credentials</div>
            <div class="credential-code">
                👤 Username: student_001<br>
                🔑 Password: student123
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Features
        st.markdown("**✨ Student Features:**")
        st.markdown("- 📊 Personal Dashboard\n- 🤖 AI Counselor Chat\n- 📈 Performance Tracking\n- 📚 Study Resources")
    
    # ============================================================
    # PARENT LOGIN PORTAL
    # ============================================================
    with parent_col:
        st.markdown("""
        <div class="login-card">
            <div class="role-icon">👨‍👩‍👧</div>
            <div class="login-form-title">Parent Login</div>
            <div class="role-description">
                Monitor your child's academic progress and stay updated with real-time alerts
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("parent_login_form"):
            st.markdown("**Parent Portal**")
            parent_username = st.text_input(
                "Username",
                placeholder="e.g., parent_001",
                key="parent_username"
            )
            parent_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="parent_password"
            )
            
            parent_login_btn = st.form_submit_button(
                "👨‍👩‍👧 Login as Parent",
                use_container_width=True,
                type="primary"
            )
            
            if parent_login_btn:
                if parent_username and parent_password:
                    user_info = db.authenticate(parent_username, parent_password)
                    if user_info and user_info['role'] == 'parent':
                        st.session_state.authenticated = True
                        st.session_state.user = user_info
                        st.session_state.role = 'parent'
                        st.session_state.username = parent_username
                        st.session_state.child_student_id = user_info.get("child_student_id", "2310001")
                        st.success("✅ Login successful!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid parent credentials!")
                else:
                    st.warning("⚠️ Please enter username and password")
        
        # Demo credentials
        st.markdown("""
        <div class="credential-card">
            <div class="credential-label">📋 Demo Credentials</div>
            <div class="credential-code">
                👨‍👩‍👧 Username: parent_001<br>
                🔑 Password: parent123
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Features
        st.markdown("**✨ Parent Features:**")
        st.markdown("- 📊 Child's Dashboard\n- 📈 Performance Analytics\n- 🔔 Real-time Alerts\n- 💬 Counselor Chat")
    
    # ============================================================
    # COUNSELOR LOGIN PORTAL
    # ============================================================
    with counselor_col:
        st.markdown("""
        <div class="login-card">
            <div class="role-icon">🎯</div>
            <div class="login-form-title">Counselor Login</div>
            <div class="role-description">
                Manage student counseling sessions and access comprehensive analytics
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("counselor_login_form"):
            st.markdown("**Counselor Portal**")
            counselor_username = st.text_input(
                "Username",
                placeholder="e.g., counselor_001",
                key="counselor_username"
            )
            counselor_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="counselor_password"
            )
            
            counselor_login_btn = st.form_submit_button(
                "🎯 Login as Counselor",
                use_container_width=True,
                type="primary"
            )
            
            if counselor_login_btn:
                if counselor_username and counselor_password:
                    user_info = db.authenticate(counselor_username, counselor_password)
                    if user_info and user_info['role'] == 'counselor':
                        st.session_state.authenticated = True
                        st.session_state.user = user_info
                        st.session_state.role = 'counselor'
                        st.session_state.username = counselor_username
                        st.success("✅ Login successful!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid counselor credentials!")
                else:
                    st.warning("⚠️ Please enter username and password")
        
        # Demo credentials
        st.markdown("""
        <div class="credential-card">
            <div class="credential-label">📋 Demo Credentials</div>
            <div class="credential-code">
                🎯 Username: counselor_001<br>
                🔑 Password: counselor123
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Features
        st.markdown("**✨ Counselor Features:**")
        st.markdown("- 👥 Student Management\n- 📊 Analytics Dashboard\n- 📝 Session Records\n- 🤖 AI Assistance")
    
    # ============================================================
    # INFORMATION SECTION
    # ============================================================
    st.markdown("---")
    
    st.markdown("## 📋 Platform Information")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.markdown("""
        **🎯 For Students**
        
        Manage your academic journey with:
        - Personal performance dashboards
        - AI-powered counseling sessions
        - Real-time academic guidance
        - Resource library access
        """)
    
    with info_col2:
        st.markdown("""
        **👨‍👩‍👧 For Parents**
        
        Stay informed about your child's progress:
        - Comprehensive performance analytics
        - Power BI dashboards
        - Real-time notifications
        - Direct counselor communication
        """)
    
    with info_col3:
        st.markdown("""
        **🎯 For Counselors**
        
        Professional counseling management:
        - Student caseload management
        - Advanced analytics reports
        - Tableau dashboards
        - Session documentation
        """)

# ============================================================
# ADVANCED SIDEBAR WITH LOGOUT
# ============================================================
def show_advanced_sidebar():
    """Display advanced sidebar with user info and navigation"""
    
    with st.sidebar:
        # User Profile Card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
            <h3 style="margin: 0 0 15px 0;">👤 User Profile</h3>
            <p style="margin: 5px 0;"><strong>Name:</strong> {st.session_state.user['name']}</p>
            <p style="margin: 5px 0;"><strong>Email:</strong> {st.session_state.user['email']}</p>
            <p style="margin: 5px 0; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.3);">
                <strong>Role:</strong> <span style="background: rgba(255,255,255,0.2); padding: 3px 10px; 
                border-radius: 20px; font-size: 0.9em;">{st.session_state.role.upper()}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Section
        st.markdown("### 📍 Navigation")
        
        if st.session_state.role == "student":
            st.page_link("pages/student_dashboard.py", label="📊 My Dashboard")
            st.page_link("pages/student_counselor_chat.py", label="🤖 AI Counselor")
            st.page_link("pages/student_resources.py", label="📚 Resources")
        elif st.session_state.role == "parent":
            st.page_link("pages/parent_dashboard.py", label="📊 Child's Dashboard")
            st.page_link("pages/parent_messages.py", label="💬 Messages")
            st.page_link("pages/parent_alerts.py", label="🔔 Alerts")
        else:  # counselor
            st.page_link("pages/counselor_dashboard.py", label="🎯 Dashboard")
            st.page_link("pages/counselor_students.py", label="👥 My Students")
            st.page_link("pages/counselor_notes.py", label="📝 Notes")
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        
        theme = st.radio(
            "🌓 Theme:",
            ["Light Mode", "Dark Mode"],
            label_visibility="collapsed"
        )
        
        notifications = st.checkbox("🔔 Enable Notifications", value=True)
        
        st.markdown("---")
        
        # Logout
        st.markdown("### 🚪 Account")
        
        if st.button("🚪 LOGOUT", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.username = None
            st.success("✅ Successfully logged out!")
            st.rerun()
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <p style="text-align: center; color: #999; font-size: 0.9em; margin-top: 20px;">
            <strong>Vignan AI Counselor</strong><br>
            Advanced Educational Platform<br>
            v2.0 | © 2026
        </p>
        """, unsafe_allow_html=True)

# ============================================================
# ROLE-SPECIFIC SERVICE PANEL
# ============================================================
def show_role_services():
    """Display role-specific service cards and quick links"""
    st.markdown("## 🔧 Available Services")

    if st.session_state.role == "student":
        services = [
            {"icon": "📊", "title": "My Dashboard", "desc": "View academic progress, grades, and attendance."},
            {"icon": "🤖", "title": "AI Counselor", "desc": "Ask personalized study and career guidance questions."},
            {"icon": "📚", "title": "Resources", "desc": "Browse study resources and recommended learning paths."}
        ]
    elif st.session_state.role == "parent":
        services = [
            {"icon": "📊", "title": "Child's Dashboard", "desc": "Monitor your child's performance and attendance."},
            {"icon": "🔔", "title": "Alerts", "desc": "Receive real-time notifications for key issues."},
            {"icon": "💬", "title": "Messages", "desc": "Communicate with counselors about your child."}
        ]
    else:
        services = [
            {"icon": "🎯", "title": "Counselor Dashboard", "desc": "Review student analytics and manage counseling tasks."},
            {"icon": "👥", "title": "My Students", "desc": "Track high-priority students and academic concerns."},
            {"icon": "📝", "title": "Counsel Notes", "desc": "Log session notes and follow-ups for each student."}
        ]

    cols = st.columns(len(services))
    for col, service in zip(cols, services):
        col.markdown(f"""
        <div style=\"background: #f7f8fc; border-radius: 14px; padding: 18px; height: 100%; box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);\">
            <h3 style=\"margin: 0 0 10px;\">{service['icon']} {service['title']}</h3>
            <p style=\"margin: 0; color: #555; line-height: 1.5;\">{service['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# DASHBOARD DISPLAY
# ============================================================
def show_dashboard():
    """Show appropriate dashboard based on role"""
    
    show_advanced_sidebar()
    show_role_services()
    
    if st.session_state.role == "student":
        show_student_dashboard(st.session_state.student_id)
    elif st.session_state.role == "parent":
        show_parent_dashboard(st.session_state.child_student_id)
    elif st.session_state.role == "counselor":
        show_counselor_dashboard(st.session_state.username)

# ============================================================
# MAIN APPLICATION
# ============================================================
def main():
    """Main application entry point"""
    
    if not st.session_state.authenticated:
        show_three_portal_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
