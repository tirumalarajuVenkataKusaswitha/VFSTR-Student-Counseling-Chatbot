"""
Counselor Dashboard Page
Advanced dashboard for counselor with AI assistance
"""

import streamlit as st
import pandas as pd
from utils import (
    get_high_priority_students,
    get_top_performers,
    get_student_by_id,
    search_students,
    create_marks_dataframe,
    display_health_indicator,
    get_department_stats,
    load_student_data
)
from ai_counselor import ai_counselor
from database import db

def require_role(required_role):
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access this page")
        st.stop()
    if st.session_state.get("role") != required_role:
        st.error(f"Access denied. This page is only available to {required_role.title()} users.")
        st.stop()


def show_counselor_dashboard(counselor_id):
    require_role("counselor")
    """Display counselor dashboard with AI support"""
    
    st.title("🎯 Counselor Dashboard")
    
    # Get counselor info
    counselor = db.get_user(counselor_id)
    st.write(f"### Welcome, {counselor.get('name', 'Counselor')}!")
    st.caption(f"Specialization: {counselor.get('specialization', 'General Counseling')}")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "⚠️ Priority Students",
        "🏆 Top Performers",
        "🤖 AI Chat",
        "📊 Analytics"
    ])
    
    # TAB 1: Overview
    with tab1:
        st.subheader("Dashboard Overview")
        
        students_data = load_student_data()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Students", len(students_data))
        
        with col2:
            priority_count = len([s for s in students_data if s.get("needs_counseling")])
            st.metric("Needing Support", priority_count)
        
        with col3:
            avg_cgpa = sum([s.get("cgpa", 0) for s in students_data]) / len(students_data)
            st.metric("Avg CGPA", f"{avg_cgpa:.2f}")
        
        with col4:
            low_attendance = len([s for s in students_data if s.get("attendance", 100) < 75])
            st.metric("Low Attendance", low_attendance)
        
        with col5:
            warnings_total = sum([s.get("warnings", 0) for s in students_data])
            st.metric("Total Warnings", warnings_total)
        
        # Quick Stats
        st.markdown("---")
        st.subheader("Quick Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Performance Distribution")
            cgpas = [s.get("cgpa", 0) for s in students_data]
            excellent = len([c for c in cgpas if c >= 7.5])
            good = len([c for c in cgpas if 6.5 <= c < 7.5])
            average = len([c for c in cgpas if 5.0 <= c < 6.5])
            poor = len([c for c in cgpas if c < 5.0])
            
            st.write(f"🟢 Excellent (≥7.5): {excellent}")
            st.write(f"🟡 Good (6.5-7.5): {good}")
            st.write(f"🟠 Average (5.0-6.5): {average}")
            st.write(f"🔴 Poor (<5.0): {poor}")
        
        with col2:
            st.markdown("#### Attendance Status")
            high_att = len([s for s in students_data if s.get("attendance", 0) >= 85])
            good_att = len([s for s in students_data if 80 <= s.get("attendance", 0) < 85])
            okay_att = len([s for s in students_data if 75 <= s.get("attendance", 0) < 80])
            low_att = len([s for s in students_data if s.get("attendance", 0) < 75])
            
            st.write(f"🟢 Excellent (≥85%): {high_att}")
            st.write(f"🟡 Good (80-85%): {good_att}")
            st.write(f"🟠 Fair (75-80%): {okay_att}")
            st.write(f"🔴 Poor (<75%): {low_att}")
    
    # TAB 2: Priority Students
    with tab2:
        st.subheader("⚠️ Students Needing Immediate Attention")
        
        priority_students = get_high_priority_students(limit=20)
        
        if priority_students:
            search_query = st.text_input("🔍 Search student in priority list:")
            
            if search_query:
                priority_students = [s for s in priority_students 
                                   if search_query.lower() in s["name"].lower() 
                                   or search_query.lower() in s["student_id"]]
            
            # Display as expandable cards
            for student in priority_students:
                with st.expander(f"📌 {student['name']} (ID: {student['student_id']}) - CGPA: {student['cgpa']:.2f}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("CGPA", f"{student['cgpa']:.2f}/10")
                    with col2:
                        st.metric("Attendance", f"{student['attendance']}%")
                    with col3:
                        st.metric("Warnings", student['warnings'])
                    
                    st.markdown("---")
                    
                    # Health indicator
                    display_health_indicator(student)
                    
                    st.markdown("---")
                    
                    # Subject performance
                    marks_df = create_marks_dataframe(student)
                    st.dataframe(marks_df[["Subject", "Total", "Percentage", "Grade"]], use_container_width=True)
                    
                    st.markdown("---")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"💬 Chat with {student['name']}", key=f"chat_{student['student_id']}"):
                            st.session_state.selected_student = student
                            st.session_state.show_ai_chat = True
                    
                    with col2:
                        if st.button(f"📝 Add Note for {student['name']}", key=f"note_{student['student_id']}"):
                            st.session_state.show_note_form = True
                            st.session_state.selected_student = student
                    
                    with col3:
                        if st.button(f"📞 Schedule Meeting", key=f"meeting_{student['student_id']}"):
                            st.success(f"Meeting scheduled with {student['name']}")
        else:
            st.success("✅ No students in priority list currently!")
    
    # TAB 3: Top Performers
    with tab3:
        st.subheader("🏆 Top Performing Students")
        
        top_students = get_top_performers(limit=15)
        
        top_df = pd.DataFrame([
            {
                "Name": s["name"],
                "ID": s["student_id"],
                "CGPA": f"{s['cgpa']:.2f}",
                "Attendance": f"{s['attendance']}%",
                "Department": s["department"]
            }
            for s in top_students
        ])
        
        st.dataframe(top_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Recognition & Feedback")
        
        for i, student in enumerate(top_students[:5], 1):
            st.success(f"#{i} {student['name']} - Excellent performance with CGPA {student['cgpa']:.2f}. Consider for awards/scholarships.")
    
    # TAB 4: AI Chat with Student
    with tab4:
        st.subheader("🤖 AI-Assisted Student Counseling")
        
        # Select student
        all_students = load_student_data()
        student_options = {f"{s['name']} ({s['student_id']})": s for s in all_students}
        
        selected_option = st.selectbox("Select student to counsel:", list(student_options.keys()))
        selected_student = student_options[selected_option]
        
        st.markdown("---")
        
        # Show student profile snapshot
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CGPA", f"{selected_student['cgpa']:.2f}")
        with col2:
            st.metric("Attendance", f"{selected_student['attendance']}%")
        with col3:
            st.metric("Warnings", selected_student['warnings'])
        with col4:
            st.metric("Department", selected_student['department'])
        
        st.markdown("---")
        
        # AI Chat Interface
        st.markdown("#### 💬 Chat with AI Counselor")
        
        # Initialize session state
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
        
        # Display conversation
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.conversation_history:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    st.chat_message("assistant").write(msg["content"])
        
        # User input
        user_input = st.chat_input("Ask counselor about the student...")
        
        if user_input:
            # Add to history
            st.session_state.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Get AI response
            system_prompt = ai_counselor.get_counselor_system_prompt(
                counselor.get('name'),
                counselor.get('specialization'),
                counselor.get('expertise', []),
                {
                    'name': selected_student['name'],
                    'cgpa': selected_student['cgpa'],
                    'attendance': selected_student['attendance'],
                    'department': selected_student['department'],
                    'concerns': user_input
                }
            )
            
            response = ai_counselor.get_ai_response(
                user_input,
                st.session_state.conversation_history,
                system_prompt
            )
            
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            st.rerun()
    
    # TAB 5: Analytics
    with tab5:
        st.subheader("📊 Department-wise Analytics")
        
        dept_stats = get_department_stats()
        
        dept_df = pd.DataFrame([
            {
                "Department": dept,
                "Students": stats["count"],
                "Avg CGPA": f"{stats['avg_cgpa']:.2f}",
                "Need Counseling": stats["need_counseling"]
            }
            for dept, stats in dept_stats.items()
        ])
        
        st.dataframe(dept_df, use_container_width=True)
        
        # Charts
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### CGPA Distribution by Department")
            dept_names = list(dept_stats.keys())
            avg_cgpas = [dept_stats[d]["avg_cgpa"] for d in dept_names]
            
            chart_data = pd.DataFrame({
                "Department": dept_names,
                "Avg CGPA": avg_cgpas
            })
            st.bar_chart(chart_data.set_index("Department"))
        
        with col2:
            st.markdown("#### Students Needing Support by Department")
            need_counseling = [dept_stats[d]["need_counseling"] for d in dept_names]
            
            chart_data = pd.DataFrame({
                "Department": dept_names,
                "Need Counseling": need_counseling
            })
            st.bar_chart(chart_data.set_index("Department"))

if __name__ == "__main__":
    show_counselor_dashboard("counselor_001")
