"""
Utility Functions for Dashboards
Common functions used across all role dashboards
"""

import json
import streamlit as st
import pandas as pd
from datetime import datetime

def load_student_data():
    """Load student data from JSON"""
    try:
        with open("student_data.json", "r") as f:
            return json.load(f)
    except:
        return []

def get_student_by_id(student_id):
    """Get single student data"""
    students = load_student_data()
    if student_id is None:
        return None
    lookup = str(student_id).strip()
    for student in students:
        if str(student.get("student_id", "")).strip() == lookup:
            return student
    return None

def get_student_by_name(name):
    """Get student by name"""
    students = load_student_data()
    for student in students:
        if student["name"].lower() == name.lower():
            return student
    return None

def search_students(query):
    """Search students by name or ID"""
    students = load_student_data()
    results = []
    query_lower = query.lower()
    for student in students:
        if query_lower in student["name"].lower() or query_lower in student["student_id"]:
            results.append(student)
    return results

def get_high_priority_students(limit=10):
    """Get students who need counseling (low CGPA or attendance)"""
    students = load_student_data()
    priority = [s for s in students if s.get("needs_counseling", False)]
    return sorted(priority, key=lambda x: x.get("cgpa", 0))[:limit]

def get_top_performers(limit=10):
    """Get top performing students"""
    students = load_student_data()
    return sorted(students, key=lambda x: x.get("cgpa", 0), reverse=True)[:limit]

def create_marks_dataframe(student_data):
    """Create DataFrame from student marks"""
    marks_data = []
    for subject, marks in student_data.get("marks", {}).items():
        marks_data.append({
            "Subject": subject,
            "T1": marks.get("T1"),
            "T2": marks.get("T2"),
            "T3": marks.get("T3"),
            "T4": marks.get("T4"),
            "M1_A1": marks.get("M1_A1"),
            "M1_A2": marks.get("M1_A2"),
            "M2_A1": marks.get("M2_A1"),
            "M2_A2": marks.get("M2_A2"),
            "Total": marks.get("Total"),
            "Percentage": marks.get("Percentage"),
            "Grade": marks.get("Grade")
        })
    return pd.DataFrame(marks_data)

def display_performance_card(student_data):
    """Display student performance summary card"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CGPA", f"{student_data['cgpa']:.2f}/10", 
                 delta=None, label_visibility="visible")
    
    with col2:
        st.metric("Attendance", f"{student_data['attendance']}%", 
                 delta=None, label_visibility="visible")
    
    with col3:
        avg_percentage = sum([m.get("Percentage", 0) for m in student_data.get("marks", {}).values()]) / len(student_data.get("marks", {}))
        st.metric("Avg %", f"{avg_percentage:.1f}%", 
                 delta=None, label_visibility="visible")
    
    with col4:
        warnings = student_data.get("warnings", 0)
        st.metric("Warnings", warnings, 
                 delta=None, label_visibility="visible")

def get_grade_color(grade):
    """Get color for grade"""
    grade_colors = {
        "A+": "🟢",
        "A": "🟢",
        "B+": "🟡",
        "B": "🟡",
        "C": "🟠",
        "F": "🔴"
    }
    return grade_colors.get(grade, "⚪")

def display_marks_table(marks_df):
    """Display marks in formatted table"""
    st.dataframe(
        marks_df.style.background_gradient(cmap="RdYlGn", subset=["Percentage"]),
        use_container_width=True
    )

def get_department_stats():
    """Get statistics by department"""
    students = load_student_data()
    depts = {}
    
    for student in students:
        dept = student.get("department")
        if dept not in depts:
            depts[dept] = {"count": 0, "total_cgpa": 0, "need_counseling": 0}
        
        depts[dept]["count"] += 1
        depts[dept]["total_cgpa"] += student.get("cgpa", 0)
        if student.get("needs_counseling"):
            depts[dept]["need_counseling"] += 1
    
    # Calculate averages
    for dept in depts:
        depts[dept]["avg_cgpa"] = depts[dept]["total_cgpa"] / depts[dept]["count"]
    
    return depts

def display_health_indicator(student_data):
    """Display overall health/status of student"""
    cgpa = student_data.get("cgpa", 0)
    attendance = student_data.get("attendance", 0)
    warnings = student_data.get("warnings", 0)
    
    # Calculate health score (0-100)
    health_score = 0
    health_score += (cgpa / 10) * 40  # 40% weight to CGPA
    health_score += (attendance / 100) * 40  # 40% weight to attendance
    health_score += max(0, (100 - warnings * 20)) * 0.2  # 20% weight to warnings
    
    health_score = max(0, min(100, health_score))
    
    if health_score >= 80:
        status = "🟢 Excellent"
        color = "#00CC00"
    elif health_score >= 60:
        status = "🟡 Good"
        color = "#FFAA00"
    elif health_score >= 40:
        status = "🟠 Fair"
        color = "#FF6600"
    else:
        status = "🔴 Critical"
        color = "#CC0000"
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(health_score / 100, text=f"Overall Health: {health_score:.0f}/100")
    with col2:
        st.metric("Status", status)

def get_subject_performance_summary(student_data):
    """Get summary of subject performance"""
    marks = student_data.get("marks", {})
    summary = {
        "excellent": [],
        "good": [],
        "average": [],
        "needs_improvement": []
    }
    
    for subject, marks_data in marks.items():
        percentage = marks_data.get("Percentage", 0)
        if percentage >= 80:
            summary["excellent"].append((subject, percentage))
        elif percentage >= 70:
            summary["good"].append((subject, percentage))
        elif percentage >= 60:
            summary["average"].append((subject, percentage))
        else:
            summary["needs_improvement"].append((subject, percentage))
    
    return summary
