"""
Student - Resources Page
Study materials, tips, and guidance resources
"""

import streamlit as st

st.set_page_config(page_title="Student Resources", layout="wide")

def require_role(required_role):
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access this page")
        st.stop()
    if st.session_state.get("role") != required_role:
        st.error(f"Access denied. This page is only available to {required_role.title()} users.")
        st.stop()

require_role("student")

st.title("📚 Academic Resources & Guidance")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Study Tips",
    "⏰ Time Management",
    "💼 Career Guidance",
    "🧠 Mental Wellness",
    "📞 Contact Support"
])

with tab1:
    st.subheader("📖 Effective Study Tips")
    
    st.markdown("""
    ### 1. **Active Learning Techniques**
    - **Spaced Repetition**: Review material at increasing intervals
    - **Feynman Technique**: Explain concepts in simple terms
    - **Practice Problems**: Solve varied questions regularly
    - **Summary Writing**: Create concise notes of key concepts
    
    ### 2. **Study Environment**
    - Choose a quiet, well-lit space
    - Minimize distractions (phone, social media)
    - Keep study materials organized
    - Take short breaks every 30-45 minutes
    
    ### 3. **Subject-Specific Strategies**
    - **Mathematics**: Practice problems daily, understand theory first
    - **Programming**: Code regularly, build small projects
    - **Data Structures**: Visualize algorithms, trace execution
    - **Databases**: Practice SQL queries, understand normalization
    
    ### 4. **Exam Preparation**
    - Start revision 2-3 weeks before exams
    - Create revision timetables
    - Solve previous year question papers
    - Group study for peer learning
    - Get adequate sleep before exams
    """)

with tab2:
    st.subheader("⏰ Time Management Strategies")
    
    st.markdown("""
    ### Daily Schedule Template
    """)
    
    schedule = {
        "7:00 - 8:00": "Morning Routine & Breakfast",
        "8:30 - 12:30": "Classes (4 hours)",
        "12:30 - 1:30": "Lunch Break",
        "1:30 - 5:30": "Classes/Labs (4 hours)",
        "5:30 - 6:30": "Physical Activity/Break",
        "6:30 - 8:30": "Study/Assignments (2 hours)",
        "8:30 - 9:30": "Dinner",
        "9:30 - 10:30": "Personal Time/Relaxation",
        "10:30": "Sleep"
    }
    
    for time, activity in schedule.items():
        st.write(f"**{time}**: {activity}")
    
    st.markdown("""
    ### Weekly Planning Tips
    
    1. **Monday**: Review weekly goals, plan major tasks
    2. **Tuesday-Thursday**: Focus on challenging subjects
    3. **Friday**: Complete pending assignments
    4. **Saturday**: Revision and practice tests
    5. **Sunday**: Rest and plan for next week
    
    ### Priority Management (ABC Method)
    - **A-Priority**: Must do today (exams, deadlines)
    - **B-Priority**: Should do this week (regular coursework)
    - **C-Priority**: Nice to do (extra reading, projects)
    """)

with tab3:
    st.subheader("💼 Career Guidance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Career Path Options
        
        **Software Development**
        - Web Development
        - Mobile App Development
        - Cloud Computing
        - DevOps
        
        **Data Science**
        - Data Analysis
        - Machine Learning
        - Business Intelligence
        
        **Systems & Infrastructure**
        - Network Administration
        - System Engineering
        - Cybersecurity
        """)
    
    with col2:
        st.markdown("""
        ### Building Your Career
        
        **Skills to Develop**
        - Technical skills (programming, tools)
        - Soft skills (communication, teamwork)
        - Problem-solving abilities
        - Leadership qualities
        
        **Internship Tips**
        - Apply early (6 months ahead)
        - Build a strong resume
        - Practice interviews
        - Network with seniors
        """)

with tab4:
    st.subheader("🧠 Mental Wellness & Work-Life Balance")
    
    st.markdown("""
    ### Stress Management Techniques
    
    1. **Physical Activity**
       - Exercise for 30 minutes daily
       - Yoga or meditation for relaxation
       - Sports and outdoor activities
    
    2. **Sleep Hygiene**
       - Sleep 7-8 hours daily
       - Maintain consistent sleep schedule
       - Avoid screens before bed
    
    3. **Mindfulness Practices**
       - Meditation (start with 5 minutes)
       - Deep breathing exercises
       - Journaling thoughts and feelings
    
    4. **Social Connection**
       - Spend time with friends
       - Family interactions
       - Join clubs and societies
    
    ### When to Seek Help
    - Persistent anxiety or depression
    - Difficulty concentrating
    - Sleep disturbances
    - Overwhelming stress
    - Thoughts of self-harm
    
    **Our counselors are here to help!** Don't hesitate to reach out.
    """)

with tab5:
    st.subheader("📞 Support & Contact Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Counseling Services
        
        🎯 **Academic Counselor**
        - Dr. Ananya Verma
        - Email: ananya@vignan.ac.in
        - Specialization: Academic Guidance
        - Availability: Monday-Friday, 2-5 PM
        
        🧠 **Mental Health Counselor**
        - Prof. Rajesh Kumar
        - Email: rajesh@vignan.ac.in
        - Specialization: Mental Health
        - Availability: Tuesday, Thursday, 3-6 PM
        """)
    
    with col2:
        st.markdown("""
        ### Emergency Support
        
        🆘 **Crisis Helplines**
        - AAMI Helpline: +91-22-2754-6669
        - iCall: +91-9152-987-821
        - Vandrevala Foundation: +91-9999-666-555
        
        📋 **Quick Links**
        - Book Counseling Session (Chat tab)
        - Request Meeting (Dashboard)
        - View Counselor Notes
        """)
    
    st.markdown("---")
    
    # Quick booking
    if st.button("📅 Book a Counseling Session"):
        st.info("Click on 'Chat with Counselor' to request a session!")
