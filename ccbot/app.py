"""
Enhanced Vignan AI Counselor Bot - Three-Login System
Enterprise-grade student counseling system with Role-Based Access and Premium UI
"""

import streamlit as st
from database import db
from pages.student_dashboard import show_student_dashboard
from pages.parent_dashboard import show_parent_dashboard
from pages.counselor_dashboard import show_counselor_dashboard

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="CampusCare AI Counselor",
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
    st.session_state.name = None
    st.session_state.student_id = None
    st.session_state.child_student_id = None
    st.session_state.login_tab = "student"

# ============================================================
# GLOBAL STYLE INJECTION
# ============================================================

def inject_global_styles():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            .stApp {
                background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.18), transparent 35%),
                            linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
                color: #0f172a;
            }

            .login-card,
            .feature-card,
            .sidebar-card {
                background: rgba(255, 255, 255, 0.92);
                border-radius: 24px;
                padding: 24px;
                box-shadow: 0 24px 70px rgba(15, 23, 42, 0.08);
            }

            .feature-card {
                border: 1px solid rgba(148, 163, 184, 0.16);
                transition: transform 0.18s ease, box-shadow 0.18s ease;
            }
            .feature-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 26px 80px rgba(15, 23, 42, 0.12);
            }

            .sidebar .stButton button,
            .stButton button {
                border-radius: 999px !important;
            }

            .stTextInput > div > div > input,
            .stSelectbox > div > div > div {
                border-radius: 16px !important;
                border: 1px solid rgba(148, 163, 184, 0.3) !important;
                padding: 14px 16px !important;
                background-color: #ffffff !important;
                transition: border-color 0.2s ease !important;
                font-size: 1rem !important;
                color: #0f172a !important;
            }
            .stTextInput > div > div > input:focus,
            .stSelectbox > div > div > div:focus {
                border-color: #38bdf8 !important;
                box-shadow: none !important;
            }

            .forgot-link {
                text-align: center;
                margin-top: 18px;
            }
            .forgot-link a {
                color: #0ea5e9;
                text-decoration: none;
                font-size: 0.95rem;
            }
            .forgot-link a:hover {
                text-decoration: underline;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_global_styles()

# ============================================================
# UNIFIED LOGIN PAGE
# ============================================================
def show_unified_login():
    """Display unified login form for all roles."""
    st.markdown(
        """
        <div style='border-radius: 30px; padding: 24px 30px; background: rgba(255,255,255,0.95); box-shadow: 0 28px 80px rgba(15,23,42,0.08); margin-bottom: 24px;'>
            <h1 style='margin:0; font-size:2.4rem; color:#111827;'>CampusCare AI</h1>
            <p style='margin:8px 0 0 0; color:#475569; font-size:1.05rem;'>Secure login for students, parents, and counselors with analytics, alerts, and AI-driven support.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    login_col, info_col = st.columns([1.4, 1], gap="large")

    with login_col:
        with st.form("login_form"):
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            st.subheader("Login to your role-based workspace")
            username = st.text_input("Username", placeholder="Enter your username")
            role = st.selectbox("Select role", options=["Select User", "Student", "Parent", "Counselor"])
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_btn = st.form_submit_button("🚀 Sign in")
            st.markdown("</div>", unsafe_allow_html=True)

        if login_btn:
            if role == "Select User":
                st.warning("Please select your role before continuing.")
            elif not username or not password:
                st.warning("Please enter both username and password.")
            else:
                user_info = db.authenticate(username.strip(), password)
                expected_role = role.lower()
                if user_info and user_info["role"] == expected_role:
                    st.session_state.authenticated = True
                    st.session_state.user = user_info
                    st.session_state.role = expected_role
                    st.session_state.username = username.strip()
                    st.session_state.name = user_info.get("name")
                    if expected_role == "student":
                        st.session_state.student_id = user_info.get("student_id")
                    elif expected_role == "parent":
                        st.session_state.child_student_id = user_info.get("child_student_id")
                    st.success(f"Welcome back, {user_info['name']}! Redirecting to your dashboard...")
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials or role mismatch. Please try again.")

        st.markdown(
            """
            <div class='forgot-link'>
                <a href='#'>Forgot password?</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("\n")

    with info_col:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.subheader("Why CampusCare AI?")
        st.write("• Personalized student dashboards for performance, attendance, and health monitoring.")
        st.write("• Role-based analytics for students, parents, and counselors.")
        st.write("• Built-in AI counselor support for instant academic and well-being guidance.")
        st.write("• Secure access with sample demo credentials for quick evaluation.")
        st.markdown("---")
        st.subheader("Sample credentials")
        st.markdown("**Student:** `student_001` / `student123`")
        st.markdown("**Parent:** `parent_001` / `parent123`")
        st.markdown("**Counselor:** `counselor_001` / `counselor123`")
        st.markdown("</div>", unsafe_allow_html=True)

# ROLE-SPECIFIC SERVICE PANEL
# ============================================================
def show_role_services():
    """Display role-specific service cards."""
    st.markdown(
        "<h2 style='text-align:center; color:#111827; margin-top:2rem;'>🌟 Quick actions for your workspace</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; color:#475569; max-width:760px; margin:0 auto 1.5rem auto;'>Explore the most important tools available for your role and get started quickly.</p>",
        unsafe_allow_html=True,
    )

    if st.session_state.role == "student":
        services = [
            {"icon": "📊", "title": "My Progress", "desc": "Review grades, attendance trends, and subject strengths."},
            {"icon": "💬", "title": "AI Counselor", "desc": "Ask academic and wellbeing questions and get instant advice."},
            {"icon": "📚", "title": "Study Resources", "desc": "Browse curated learning resources and recommended materials."},
        ]
    elif st.session_state.role == "parent":
        services = [
            {"icon": "📈", "title": "Child Progress", "desc": "Monitor your child's academic performance and attendance."},
            {"icon": "🔔", "title": "Alerts", "desc": "Receive alerts when performance or attendance require attention."},
            {"icon": "📝", "title": "Messages", "desc": "Stay connected with counselors through secure communication."},
        ]
    else:
        services = [
            {"icon": "🎯", "title": "Counselor Dashboard", "desc": "Review student analytics and identify top cases."},
            {"icon": "⚠️", "title": "Priority Cases", "desc": "Track students who need immediate support."},
            {"icon": "🤖", "title": "AI Support", "desc": "Use the AI counselor to generate tailored guidance."},
        ]

    cols = st.columns(len(services), gap="medium")
    for col, service in zip(cols, services):
        col.markdown(
            f"""
            <div class='feature-card'>
                <h3 style='margin-bottom:0.75rem;'>{service['icon']} {service['title']}</h3>
                <p style='color:#475569; line-height:1.7;'>{service['desc']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# ADVANCED SIDEBAR
# ============================================================
def show_advanced_sidebar():
    """Display advanced sidebar with user info and navigation."""
    with st.sidebar:
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        user_name = st.session_state.get("name", "User")
        role_label = st.session_state.get("role", "").title()
        avatar_emoji = "👤" if role_label == "Student" else "👨‍👩‍👧" if role_label == "Parent" else "🎯"

        st.markdown(
            f"<div style='text-align:center; font-size:2.5rem; margin-bottom:12px;'>{avatar_emoji}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h3 style='margin:0; text-align:center; color:#111827;'>{user_name}</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='margin:6px 0 0 0; text-align:center; color:#475569;'>Role: <strong>{role_label}</strong></p>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<h4 style='color:#111827;'>📍 Navigation</h4>", unsafe_allow_html=True)

        if st.session_state.role == "student":
            st.page_link("pages/student_dashboard.py", label="📊 My Dashboard")
            st.page_link("pages/student_counselor_chat.py", label="🤖 AI Counselor")
            st.page_link("pages/student_resources.py", label="📚 Resources")
        elif st.session_state.role == "parent":
            st.page_link("pages/parent_dashboard.py", label="📈 Child's Progress")
            st.page_link("pages/parent_messages.py", label="💬 Messages")
            st.page_link("pages/parent_alerts.py", label="🔔 Alerts")
        else:
            st.page_link("pages/counselor_dashboard.py", label="🎯 Main Dashboard")
            st.page_link("pages/counselor_students.py", label="👥 Student Roster")
            st.page_link("pages/counselor_notes.py", label="📝 Session Notes")

        st.markdown("---")
        st.markdown("<div style='border-radius: 18px; padding: 18px; background: #f8fafc;'>", unsafe_allow_html=True)
        st.markdown("<strong>Need support?</strong>", unsafe_allow_html=True)
        st.markdown(
            "<p style='margin:0.5rem 0 0 0; color:#475569;'>Contact support@campuscare.ai for onboarding or troubleshooting.</p>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.username = None
            st.session_state.name = None
            st.session_state.student_id = None
            st.session_state.child_student_id = None
            st.success("✅ Successfully logged out!")
            st.experimental_rerun()

# ============================================================
# DASHBOARD DISPLAY
# ============================================================
def show_dashboard():
    """Show appropriate dashboard based on role."""
    show_advanced_sidebar()

    st.markdown(
        "<div style='padding: 24px; border-radius: 24px; background: rgba(255,255,255,0.95); box-shadow: 0 24px 70px rgba(15,23,42,0.06); margin-bottom: 24px;'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<h2 style='margin:0 0 8px 0; color:#111827;'>Welcome back, {st.session_state.get('name', 'Valued User')}!</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='margin:0; color:#475569;'>You are signed in as a <strong>{st.session_state.get('role', '').title()}</strong>. Use the quick access panel to navigate to your dashboard, alerts, or counselor tools.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    show_role_services()
    st.markdown("<hr style='border:none; border-top:1px solid rgba(0,0,0,0.12); margin: 30px 0;'>", unsafe_allow_html=True)

    if st.session_state.role == "student":
        show_student_dashboard(st.session_state.student_id)
    elif st.session_state.role == "parent":
        show_parent_dashboard(st.session_state.child_student_id)
    elif st.session_state.role == "counselor":
        show_counselor_dashboard(st.session_state.username)

# ============================================================
# MAIN ENTRY POINT
# ============================================================
def main():
    if not st.session_state.authenticated:
        show_unified_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
