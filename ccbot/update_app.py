import sys
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 1. Update CSS
new_css = '''st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap');

    * {
        font-family: 'Open Sans', sans-serif !important;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main Background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Login Form Container */
    .login-container {
        max-width: 500px;
        margin: 50px auto;
        padding: 40px;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 40px;
        color: #333333;
    }
    
    .login-header h1 {
        font-size: 2.5em;
        font-weight: 300;
        color: #777777;
    }
    
    .login-header h1 strong {
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        border-radius: 2px !important;
        border: 1px solid #cccccc !important;
        padding: 12px 15px !important;
        background-color: #ffffff !important;
        transition: border-color 0.3s ease;
        font-size: 1em !important;
        color: #333333 !important;
    }
    .stTextInput > div > div > input:focus, .stSelectbox > div > div > div:focus {
        border-color: #2196F3 !important;
        box-shadow: none !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #2196F3 !important;
        color: white !important;
        border-radius: 2px !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 12px 0 !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: none !important;
        transition: background-color 0.3s ease !important;
        font-size: 1.1em !important;
    }
    
    .stButton > button:hover {
        background-color: #1976D2 !important;
    }
    
    /* Forgot password link */
    .forgot-link {
        text-align: center;
        margin-top: 20px;
    }
    
    .forgot-link a {
        color: #2196F3;
        text-decoration: none;
        font-size: 1em;
    }
    
    .forgot-link a:hover {
        text-decoration: underline;
    }
    
    /* Retain original service card css for dashboard */
    .service-card {
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.8);
        border-radius: 15px;
        padding: 25px;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        background: rgba(255,255,255,0.8);
    }
    
    .service-card h3 {
        color: #2b2d42;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)'''

content = re.sub(r'st\.markdown\("""\n<style>.*?</style>\n""", unsafe_allow_html=True\)', new_css, content, flags=re.DOTALL)

# 2. Replace show_three_portal_login with show_unified_login
old_login_start = '# THREE-PORTAL LOGIN PAGE'
old_login_end = '# ROLE-SPECIFIC SERVICE PANEL'

new_login = '''# UNIFIED LOGIN PAGE
# ============================================================
def show_unified_login():
    """Display unified login form matching the reference image"""
    
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <h1><strong>SignIn To</strong> Your Account</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("unified_login_form"):
            # Add some spacing to mimic the form in the reference image
            st.markdown("<style>.stTextInput, .stSelectbox { margin-bottom: 15px; }</style>", unsafe_allow_html=True)
            
            username = st.text_input(
                "Registerno or Empcode",
                placeholder="Registerno or Empcode",
                label_visibility="collapsed"
            )
            
            role = st.selectbox(
                "Select User",
                options=["Select User", "Student", "Parent", "Counselor"],
                label_visibility="collapsed"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Password",
                label_visibility="collapsed"
            )
            
            login_btn = st.form_submit_button("SIGNIN", use_container_width=True)
            
            if login_btn:
                if role == "Select User":
                    st.warning("⚠️ Please select a user role.")
                elif username and password:
                    user_info = db.authenticate(username, password)
                    expected_role = role.lower()
                    if user_info and user_info['role'] == expected_role:
                        st.session_state.authenticated = True
                        st.session_state.user = user_info
                        st.session_state.role = expected_role
                        st.session_state.username = username
                        if expected_role == 'student':
                            st.session_state.student_id = user_info.get("student_id", "2310001")
                        elif expected_role == 'parent':
                            st.session_state.child_student_id = user_info.get("child_student_id", "2310001")
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error(f"❌ Invalid {expected_role} credentials!")
                else:
                    st.warning("⚠️ Please enter credentials")
                    
        st.markdown("""
        <div class="forgot-link">
            <a href="#">Forgottten or Set password?</a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <br><br>
        <div style="font-size: 0.8em; color: gray; text-align: center;">
            Demo Credentials:<br>
            Student: student_001 / student123<br>
            Parent: parent_001 / parent123<br>
            Counselor: counselor_001 / counselor123
        </div>
        """, unsafe_allow_html=True)

'''

pattern = r'# THREE-PORTAL LOGIN PAGE.*?# ============================================================\n(?=# ROLE-SPECIFIC SERVICE PANEL)'
content = re.sub(pattern, new_login, content, flags=re.DOTALL)

# 3. Update main()
content = content.replace('show_three_portal_login()', 'show_unified_login()')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('app.py updated successfully!')
