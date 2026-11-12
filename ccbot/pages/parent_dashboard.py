"""
Parent Dashboard Page - Enhanced with Power BI/Tableau Integration
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
    search_students
)
from dashboard_utils import (
    create_parent_analytics_dashboard,
    create_alert_card,
    get_health_status,
    get_recommendations,
    embed_powerbi_dashboard,
    embed_tableau_dashboard
)

def require_role(required_role):
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access this page")
        st.stop()
    if st.session_state.get("role") != required_role:
        st.error(f"Access denied. This page is only available to {required_role.title()} users.")
        st.stop()


def show_parent_dashboard(child_student_id):
    """Display enhanced parent dashboard for child's progress"""
    require_role("parent")
    
    st.title("👨‍👩‍👧 Parent Dashboard - Enhanced Analytics")
    
    # Get student data
    student = get_student_by_id(child_student_id)
    if not student:
        st.warning("Child's profile not found. Use the search below to locate your child.")

        query = st.text_input("Search child by name or ID", key="parent_search_query")
        if st.button("Search", key="parent_search_button"):
            results = search_students(query)
            if not results:
                st.info("No students matched your query.")
            elif len(results) == 1:
                student = results[0]
                child_student_id = student['student_id']
                st.session_state.user = st.session_state.get('user', {}) or {}
                st.session_state.user['child_student_id'] = child_student_id
                st.success(f"Loaded {student['name']} ({child_student_id})")
                st.rerun()
            else:
                options = [f"{s['name']} ({s['student_id']})" for s in results]
                choice = st.selectbox("Multiple matches found - select student", options, key="parent_search_select")
                if st.button("Load selected student", key="parent_search_load"):
                    idx = options.index(choice)
                    student = results[idx]
                    child_student_id = student['student_id']
                    st.session_state.user = st.session_state.get('user', {}) or {}
                    st.session_state.user['child_student_id'] = child_student_id
                    st.success(f"Loaded {student['name']} ({child_student_id})")
                    st.rerun()
        return
    
    # Welcome section
    st.write(f"### Monitoring {student['name']}'s Academic Progress")
    st.caption(f"Student ID: {student['student_id']} | Semester: {student['semester']} | Department: {student['department']}")
    
    # Display health status
    health_status, health_color = get_health_status(student)
    st.markdown(f"**Overall Status:** {health_status}")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics Dashboard", "📈 Performance Trends", "🔔 Alerts", "💡 Recommendations"])
    
    with tab1:
        st.subheader("📊 Interactive Analytics Dashboard")
        create_parent_analytics_dashboard(student)
        st.markdown("---")
        st.subheader("📌 BI Dashboard Previews")
        st.info("Customize these embedded dashboards with your Power BI report and Tableau dashboard URLs.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Tableau Dashboard")
            embed_tableau_dashboard(
                "https://public.tableau.com/views/RegionalSampleWorkbook/Storms",
                height=400
            )

        with col2:
            st.markdown("#### Power BI Dashboard")
            embed_powerbi_dashboard(
                embed_url="https://app.powerbi.com/view?r=eyJrIjoiZmFrZS1yZXBvcnQifQ%3D%3D",
                height=400
            )
    
    with tab2:
        st.markdown("---")
        st.subheader("📈 Performance Trends & Analysis")
        
        col1, col2 = st.columns(4)
        
        with col1:
            color = "🟢" if student['cgpa'] >= 6.5 else "🟡" if student['cgpa'] >= 5.0 else "🔴"
            st.metric(f"{color} CGPA", f"{student['cgpa']:.2f}/10")
        
        with col2:
            color = "🟢" if student['attendance'] >= 80 else "🟡" if student['attendance'] >= 75 else "🔴"
            st.metric(f"{color} Attendance", f"{student['attendance']}%")
        
        with col3:
            avg_percentage = sum([m.get("Percentage", 0) for m in student.get("marks", {}).values()]) / len(student.get("marks", {})) if student.get("marks") else 0
            color = "🟢" if avg_percentage >= 70 else "🟡" if avg_percentage >= 60 else "🔴"
            st.metric(f"{color} Avg Score", f"{avg_percentage:.1f}%")
        
        with col4:
            color = "🟢" if student['warnings'] == 0 else "🟠" if student['warnings'] == 1 else "🔴"
            st.metric(f"{color} Warnings", student['warnings'])
        
        # Subject Performance
        st.markdown("---")
        st.subheader("📖 Subject-wise Performance")
        
        marks_df = create_marks_dataframe(student)
        st.dataframe(
            marks_df.style.background_gradient(cmap="RdYlGn", subset=["Percentage"]),
            use_container_width=True
        )
        
        # Performance Analysis
        st.markdown("---")
        st.subheader("📈 Performance Summary")
        
        subject_summary = get_subject_performance_summary(student)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"**Strong Subjects**: {len(subject_summary['excellent']) + len(subject_summary['good'])} subjects")
            if subject_summary['excellent']:
                for subject, pct in subject_summary['excellent'][:3]:
                    st.write(f"  • {subject}: {pct}% ⭐")
            if subject_summary['good']:
                for subject, pct in subject_summary['good'][:2]:
                    st.write(f"  • {subject}: {pct}% ✅")
        
        with col2:
            st.warning(f"**Areas of Concern**: {len(subject_summary['average']) + len(subject_summary['needs_improvement'])} subjects")
            if subject_summary['needs_improvement']:
                for subject, pct in subject_summary['needs_improvement']:
                    st.error(f"  • {subject}: {pct}% ❌")
            if subject_summary['average']:
                for subject, pct in subject_summary['average'][:2]:
                    st.warning(f"  • {subject}: {pct}% ⚠️")
    
    with tab3:
        st.subheader("🔔 Real-time Alerts")
        
        alerts = []
        
        if student['cgpa'] < 5.0:
            alerts.append({
                'type': 'Low CGPA Alert',
                'name': student['name'],
                'message': f"CGPA has dropped below 5.0. Current: {student['cgpa']:.2f}. Please contact the academic counselor.",
                'severity': 'danger'
            })
        
        if student['attendance'] < 75:
            alerts.append({
                'type': 'Attendance Alert',
                'name': student['name'],
                'message': f"Attendance is below required threshold. Current: {student['attendance']}%. Attendance below 75% may affect grades.",
                'severity': 'danger'
            })
        
        if student['warnings'] > 0:
            alerts.append({
                'type': 'Academic Warning',
                'name': student['name'],
                'message': f"Your child has received {student['warnings']} academic warning(s). Immediate action recommended.",
                'severity': 'warning'
            })
        
        if not alerts:
            st.success("✅ No active alerts. Your child is performing well!")
        else:
            for alert in alerts:
                create_alert_card(
                    alert_type=alert['type'],
                    student_name=alert['name'],
                    message=alert['message'],
                    severity=alert['severity']
                )
    
    with tab4:
        st.subheader("💡 Personalized Recommendations")
        
        recommendations = get_recommendations(student)
        
        for rec in recommendations:
            if rec['type'] == 'danger':
                st.error(f"**{rec['title']}**\n{rec['message']}")
            elif rec['type'] == 'warning':
                st.warning(f"**{rec['title']}**\n{rec['message']}")
            else:
                st.success(f"**{rec['title']}**\n{rec['message']}")
    
    # Attendance Status
    st.markdown("---")
    st.subheader("📅 Attendance Status")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.progress(student['attendance'] / 100)
    
    with col2:
        if student['attendance'] < 75:
            st.error("Below Required")
        elif student['attendance'] < 80:
            st.warning("Acceptable")
        else:
            st.success("Excellent")
    
    st.info(f"⚠️ Minimum required attendance: 75% | Current: {student['attendance']}%")
    
    # Contact Counselor
    st.markdown("---")
    st.subheader("📞 Contact & Support")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 Request Counselor Meeting", use_container_width=True):
            st.success("Meeting request sent to counselor. You'll receive confirmation within 24 hours.")
    
    with col2:
        if st.button("📝 View Counselor Notes", use_container_width=True):
            st.info("No counselor notes available yet. Your child may grant permission to view.")
    
    with col3:
        if st.button("💬 Send Message", use_container_width=True):
            st.success("Redirecting to messages section...")

    
    # Student Contact Info
    st.markdown("---")
    st.subheader("👤 Student Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name**: {student['name']}")
        st.write(f"**Student ID**: {student['student_id']}")
        st.write(f"**Email**: {student['email']}")
    
    with col2:
        st.write(f"**Phone**: {student['phone']}")
        st.write(f"**Admission Year**: {student['admission_year']}")
        st.write(f"**Address**: {student['address']}")

if __name__ == "__main__":
    # This would be called from main app
    show_parent_dashboard("2310001")
