"""
Student Dashboard Page
"""

import streamlit as st
import pandas as pd
from utils import (
    get_student_by_id, 
    create_marks_dataframe,
    display_performance_card,
    display_marks_table,
    display_health_indicator,
    get_subject_performance_summary,
    load_student_data,
    search_students
)

def require_role(required_role):
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access this page")
        st.stop()
    if st.session_state.get("role") != required_role:
        st.error(f"Access denied. This page is only available to {required_role.title()} users.")
        st.stop()


def show_student_dashboard(student_id):
    """Display student dashboard"""
    require_role("student")
    
    # Get student data
    student = get_student_by_id(student_id)
    if not student:
        st.warning("❌ Student not found. Search by name or ID below to locate the student.")
        query = st.text_input("Search student by name or ID", key="student_search_query")
        if st.button("Search", key="student_search_button"):
            results = search_students(query)
            if not results:
                st.info("No students matched your query.")
            elif len(results) == 1:
                student = results[0]
                st.success(f"Loaded {student['name']} ({student['student_id']})")
                st.experimental_rerun()
            else:
                options = [f"{s['name']} ({s['student_id']})" for s in results]
                choice = st.selectbox("Multiple matches found - select student", options, key="student_search_select")
                if st.button("Load selected student", key="student_search_load"):
                    idx = options.index(choice)
                    student = results[idx]
                    st.success(f"Loaded {student['name']} ({student['student_id']})")
                    st.experimental_rerun()
        return
    
    # Advanced Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px;">
        <h1 style="margin: 0 0 15px 0;">📚 Student Academic Dashboard</h1>
        <p style="margin: 0; font-size: 1.1em; opacity: 0.9;">Welcome back, <strong>""" + student['name'] + """</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome section with advanced info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <p style="margin: 0; color: #999; font-size: 0.9em;">Student ID</p>
            <h3 style="margin: 5px 0 0 0; color: #667eea;">{student['student_id']}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <p style="margin: 0; color: #999; font-size: 0.9em;">Department</p>
            <h3 style="margin: 5px 0 0 0; color: #667eea;">{student['department']}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <p style="margin: 0; color: #999; font-size: 0.9em;">Semester</p>
            <h3 style="margin: 5px 0 0 0; color: #667eea;">{student['semester']}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        status = "🟢 Active" if student['attendance'] >= 75 else "🟡 Alert"
        st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <p style="margin: 0; color: #999; font-size: 0.9em;">Status</p>
            <h3 style="margin: 5px 0 0 0; color: #667eea;">{status}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance Summary
    st.markdown("---")
    st.subheader("📊 Performance Summary")
    display_performance_card(student)
    
    # Health Indicator
    st.markdown("---")
    st.subheader("💚 Overall Health Status")
    display_health_indicator(student)
    
    # Detailed Marks
    st.markdown("---")
    st.subheader("📖 Detailed Subject Performance")
    
    marks_df = create_marks_dataframe(student)
    display_marks_table(marks_df)
    
    # Subject Performance Summary
    st.markdown("---")
    st.subheader("🎯 Subject Analysis")
    
    subject_summary = get_subject_performance_summary(student)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(f"**Excellent**\n{len(subject_summary['excellent'])} Subjects\n≥ 80%", icon="⭐")
    
    with col2:
        st.success(f"**Good**\n{len(subject_summary['good'])} Subjects\n70-79%", icon="✅")
    
    with col3:
        st.warning(f"**Average**\n{len(subject_summary['average'])} Subjects\n60-69%", icon="⚠️")
    
    with col4:
        st.error(f"**Needs Improvement**\n{len(subject_summary['needs_improvement'])} Subjects\n< 60%", icon="❌")
    
    # Subject Details
    if subject_summary['excellent']:
        st.markdown("##### ⭐ Excellent Performance")
        for subject, pct in subject_summary['excellent']:
            st.success(f"{subject}: {pct}%")
    
    if subject_summary['needs_improvement']:
        st.markdown("##### ❌ Subjects Needing Improvement")
        for subject, pct in subject_summary['needs_improvement']:
            st.error(f"{subject}: {pct}% - Consider seeking help!")
    
    # Attendance
    st.markdown("---")
    st.subheader("📅 Attendance")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Attendance", f"{student['attendance']}%")
    
    with col2:
        if student['attendance'] < 75:
            st.error("⚠️ Below Required (75%)")
        else:
            st.success("✅ Above Required")
    
    with col3:
        classes_attended = int((student['attendance'] / 100) * 120)  # Assuming 120 total classes
        st.info(f"Classes Attended: ~{classes_attended}/120")
    
    # Achievements
    if student['achievements']:
        st.markdown("---")
        st.subheader("🏆 Achievements & Recognitions")
        for achievement in student['achievements']:
            st.success(f"✅ {achievement}")
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Recommendations")
    
    recommendations = []
    
    if student['cgpa'] < 5.0:
        recommendations.append("📌 **Focus on Core Subjects**: Your CGPA needs improvement. Focus on understanding fundamental concepts.")
    
    if student['attendance'] < 75:
        recommendations.append("📌 **Improve Attendance**: Regular attendance is crucial. Attend all classes and track your progress.")
    
    if student['warnings'] > 0:
        recommendations.append("📌 **Academic Warning**: You have academic warnings. Meet with your counselor for support.")
    
    if subject_summary['needs_improvement']:
        recommendations.append(f"📌 **Subject Support**: Seek help for {subject_summary['needs_improvement'][0][0]} - consider tutoring or counseling.")
    
    if not recommendations:
        st.success("✅ Keep up the excellent work! Continue your current trajectory.")
    else:
        for rec in recommendations:
            st.info(rec)
    
    # Quick Actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Request Counseling Session"):
            st.success("Counseling request submitted! You'll receive a confirmation email.")
    
    with col2:
        if st.button("📧 Send Message to Counselor"):
            st.session_state.show_message_form = True
    
    with col3:
        if st.button("📋 View Counseling Notes"):
            st.info("No counseling notes available yet.")
    
    # Parent Contact Info (optional)
    if student.get('parent_name'):
        st.markdown("---")
        st.subheader("👨‍👩‍👧 Parent Contact")
        st.write(f"**Name**: {student['parent_name']}")
        st.write(f"**Phone**: {student['parent_phone']}")
        st.write(f"**Email**: {student['parent_email']}")

if __name__ == "__main__":
    # This would be called from main app with student_id from session
    show_student_dashboard("2310001")
