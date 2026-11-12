"""
Counselor - My Students Page
List and manage counseling sessions with students
"""

import streamlit as st
import pandas as pd
from utils import (
    get_high_priority_students,
    search_students,
    get_student_by_id,
    create_marks_dataframe,
    display_health_indicator
)
from database import db

st.set_page_config(page_title="My Students", layout="wide")

def require_role(required_role):
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access this page")
        st.stop()
    if st.session_state.get("role") != required_role:
        st.error(f"Access denied. This page is only available to {required_role.title()} users.")
        st.stop()

require_role("counselor")

st.title("👥 My Students")

# Filter options
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    filter_priority = st.selectbox(
        "Filter by Priority:",
        ["All Students", "High Priority", "Moderate", "Low Risk", "Top Performers"]
    )

with col2:
    search_query = st.text_input("🔍 Search student:")

with col3:
    sort_by = st.selectbox(
        "Sort by:",
        ["CGPA (Low to High)", "CGPA (High to Low)", "Attendance", "Name"]
    )

st.markdown("---")

# Get students based on filters
if filter_priority == "High Priority":
    students = get_high_priority_students(limit=50)
else:
    from utils import load_student_data
    students = load_student_data()
    
    if filter_priority == "Moderate":
        students = [s for s in students if 5.0 <= s.get("cgpa", 0) < 6.5]
    elif filter_priority == "Low Risk":
        students = [s for s in students if s.get("cgpa", 0) >= 6.5]
    elif filter_priority == "Top Performers":
        students = sorted(students, key=lambda x: x.get("cgpa", 0), reverse=True)[:20]

# Search filter
if search_query:
    students = search_students(search_query)

# Sort
if sort_by == "CGPA (High to Low)":
    students = sorted(students, key=lambda x: x.get("cgpa", 0), reverse=True)
elif sort_by == "CGPA (Low to High)":
    students = sorted(students, key=lambda x: x.get("cgpa", 0))
elif sort_by == "Attendance":
    students = sorted(students, key=lambda x: x.get("attendance", 0))
else:
    students = sorted(students, key=lambda x: x.get("name", ""))

st.subheader(f"Showing {len(students)} students")

# Display students
for student in students:
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
    
    with col1:
        if st.button(f"📋 {student['name']}", key=f"expand_{student['student_id']}"):
            st.session_state.selected_student_detail = student['student_id']
    
    with col2:
        st.metric("CGPA", f"{student['cgpa']:.2f}", label_visibility="collapsed")
    
    with col3:
        st.metric("Attendance", f"{student['attendance']}%", label_visibility="collapsed")
    
    with col4:
        status = "🔴 Critical" if student.get("needs_counseling") else "🟢 Good"
        st.write(status)
    
    with col5:
        if st.button("💬 Chat", key=f"chat_{student['student_id']}"):
            st.session_state.selected_student = student
    
    # Expanded view
    if st.session_state.get("selected_student_detail") == student['student_id']:
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            ### {student['name']}
            **ID**: {student['student_id']}  
            **Email**: {student['email']}  
            **Phone**: {student['phone']}  
            **Department**: {student['department']}  
            **Semester**: {student['semester']}  
            **Parent**: {student['parent_name']} ({student['parent_phone']})
            """)
            
            st.markdown("#### Academic Performance")
            display_health_indicator(student)
            
            marks_df = create_marks_dataframe(student)
            st.dataframe(marks_df[["Subject", "Percentage", "Grade"]], use_container_width=True)
        
        with col2:
            st.markdown("#### Quick Actions")
            
            if st.button("📝 Add Note", key=f"note_{student['student_id']}"):
                st.session_state.show_note_form = True
                st.session_state.selected_student = student
            
            if st.button("📞 Schedule Meeting", key=f"meet_{student['student_id']}"):
                st.success("Meeting scheduled!")
            
            if st.button("📧 Send Message", key=f"msg_{student['student_id']}"):
                st.session_state.show_message_form = True
                st.session_state.selected_student = student
        
        st.markdown("---")
