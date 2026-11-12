"""
Parent - Alerts Page
Important notifications and warnings about child's progress
"""

import streamlit as st
from utils import get_student_by_id, search_students

st.set_page_config(page_title="Alerts", layout="wide")

def require_role(required_role):
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access this page")
        st.stop()
    if st.session_state.get("role") != required_role:
        st.error(f"Access denied. This page is only available to {required_role.title()} users.")
        st.stop()

require_role("parent")

st.title("🔔 Alerts & Notifications")

# Get child's student ID
child_student_id = None
if st.session_state.get('user'):
    child_student_id = st.session_state.user.get("child_student_id")
student = get_student_by_id(child_student_id) if child_student_id else None

if not student:
    st.warning("Child's profile not found. Search below to locate your child.")
    query = st.text_input("Search child by name or ID", key="alerts_parent_search")
    if st.button("Search", key="alerts_parent_search_btn"):
        results = search_students(query)
        if not results:
            st.info("No students matched your query.")
        elif len(results) == 1:
            student = results[0]
            st.session_state.user = st.session_state.get('user', {}) or {}
            st.session_state.user['child_student_id'] = student['student_id']
            st.success(f"Loaded {student['name']} ({student['student_id']})")
            st.experimental_rerun()
        else:
            options = [f"{s['name']} ({s['student_id']})" for s in results]
            choice = st.selectbox("Multiple matches found - select student", options, key="alerts_parent_select")
            if st.button("Load selected student", key="alerts_parent_load"):
                idx = options.index(choice)
                student = results[idx]
                st.session_state.user = st.session_state.get('user', {}) or {}
                st.session_state.user['child_student_id'] = student['student_id']
                st.success(f"Loaded {student['name']} ({student['student_id']})")
                st.experimental_rerun()
    else:
        st.info("No child selected. Please set your child in your profile or use search.")
    st.stop()

# Generate alerts based on student data
alerts = []

# CGPA alert
if student['cgpa'] < 5.0:
    alerts.append({
        "type": "critical",
        "title": "Low CGPA Alert",
        "message": f"Your child's CGPA is {student['cgpa']:.2f}. Immediate academic intervention recommended.",
        "action": "Schedule counselor meeting"
    })
elif student['cgpa'] < 6.0:
    alerts.append({
        "type": "warning",
        "title": "CGPA Below Target",
        "message": f"Current CGPA: {student['cgpa']:.2f}. Encourage better study habits.",
        "action": "Check performance details"
    })

# Attendance alert
if student['attendance'] < 75:
    alerts.append({
        "type": "critical",
        "title": "Attendance Critical",
        "message": f"Attendance is {student['attendance']}% - Below minimum 75%. Risk of deregistration!",
        "action": "Contact counselor immediately"
    })
elif student['attendance'] < 80:
    alerts.append({
        "type": "warning",
        "title": "Low Attendance",
        "message": f"Current attendance: {student['attendance']}%. Encourage regular class attendance.",
        "action": "Monitor attendance"
    })

# Academic warning alert
if student['warnings'] > 0:
    alerts.append({
        "type": "critical",
        "title": f"Academic Warning(s) - {student['warnings']}",
        "message": "Your child has received academic warning(s). Immediate action needed.",
        "action": "Meet with academic advisor"
    })

# Failing subjects alert
failing_subjects = []
for subject, marks in student.get("marks", {}).items():
    if marks.get("Percentage", 0) < 50:
        failing_subjects.append(subject)

if failing_subjects:
    alerts.append({
        "type": "critical",
        "title": "Failing Subjects",
        "message": f"Failing in: {', '.join(failing_subjects)}. Immediate tutoring recommended.",
        "action": "Arrange remedial classes"
    })

# Display alerts
if alerts:
    st.markdown(f"### 🚨 {len(alerts)} Active Alert(s)")
    st.markdown("---")
    for alert in alerts:
        if alert["type"] == "critical":
            with st.container():
                st.error(f"**🔴 {alert['title']}**")
                st.write(alert['message'])
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button(f"✓ {alert['action']}", key=f"action_{alerts.index(alert)}"):
                        st.success(f"Action initiated: {alert['action']}")
                st.divider()
        elif alert["type"] == "warning":
            with st.container():
                st.warning(f"**🟡 {alert['title']}**")
                st.write(alert['message'])
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button(f"✓ {alert['action']}", key=f"action_{alerts.index(alert)}"):
                        st.success(f"Action initiated: {alert['action']}")
                st.divider()
else:
    st.success("✅ No active alerts! Your child is performing well.")

st.markdown("---")

# Historical Alerts
st.subheader("📋 Recent Activity Log")

activities = [
    {"date": "2024-05-15", "event": "Marks uploaded for this semester"},
    {"date": "2024-05-12", "event": "Attendance updated"},
    {"date": "2024-05-10", "event": "Counseling session completed"},
    {"date": "2024-05-05", "event": "Assignment submitted"},
]

for activity in activities:
    st.write(f"📅 {activity['date']}: {activity['event']}")

st.markdown("---")

# Notification Settings
st.subheader("⚙️ Notification Preferences")

col1, col2 = st.columns(2)

with col1:
    st.toggle("Email notifications", value=True)
    st.toggle("SMS alerts for critical issues", value=True)

with col2:
    st.toggle("Weekly performance summary", value=True)
    st.toggle("Monthly counselor report", value=True)
