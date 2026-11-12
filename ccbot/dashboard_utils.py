"""
Dashboard Utilities with Power BI and Tableau Integration
Provides visualization helpers for enhanced dashboards
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ============================================================
# TABLEAU EMBEDDED DASHBOARD INTEGRATION
# ============================================================

def embed_tableau_dashboard(dashboard_url, height=800):
    """
    Embed a Tableau dashboard
    
    Args:
        dashboard_url: URL to the Tableau dashboard
        height: Height of the embedded dashboard
    """
    st.components.v1.iframe(
        src=dashboard_url,
        height=height,
        scrolling=True
    )

# ============================================================
# POWER BI EMBEDDED DASHBOARD INTEGRATION
# ============================================================

def embed_powerbi_dashboard(embed_url=None, report_id=None, access_token=None, height=800):
    """
    Embed a Power BI report
    
    Args:
        embed_url: Full Power BI embed URL (preferred)
        report_id: Power BI report ID (optional)
        access_token: Power BI access token (optional)
        height: Height of the embedded report
    """
    if embed_url:
        src = embed_url
    elif report_id:
        src = f"https://app.powerbi.com/reportEmbed?reportId={report_id}&autoAuth=true&ctid=common"
    else:
        st.warning("Power BI dashboard URL or report ID is required for embedding.")
        return

    html_string = f"""
    <iframe 
        width="100%" 
        height="{height}" 
        src="{src}" 
        frameborder="0" 
        allowFullScreen="true">
    </iframe>
    """
    st.components.v1.html(html_string, height=height)

# ============================================================
# INTERACTIVE STUDENT PERFORMANCE DASHBOARD
# ============================================================

def create_student_performance_dashboard(student_data):
    """Create an interactive student performance dashboard"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 CGPA",
            f"{student_data['cgpa']:.2f}",
            f"{student_data['cgpa'] - 6.0:.2f}",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "✅ Attendance",
            f"{student_data['attendance']}%",
            f"{student_data['attendance'] - 75}%",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            "📚 Subjects",
            len(student_data.get('subjects', [])),
            "0"
        )
    
    with col4:
        st.metric(
            "⭐ Performance",
            "Excellent" if student_data['cgpa'] >= 8 else "Good" if student_data['cgpa'] >= 6 else "Average",
            ""
        )
    
    st.markdown("---")
    
    # Performance over time chart
    col1, col2 = st.columns(2)
    
    with col1:
        # CGPA Trend Chart
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        cgpa_values = [random.uniform(5.5, 8.5) for _ in range(12)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=cgpa_values,
            mode='lines+markers',
            name='CGPA Trend',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="📈 CGPA Trend (12 Months)",
            xaxis_title="Month",
            yaxis_title="CGPA",
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Attendance Pie Chart
        attendance_data = {
            'Present': student_data['attendance'],
            'Absent': 100 - student_data['attendance']
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(attendance_data.keys()),
            values=list(attendance_data.values()),
            marker=dict(colors=['#4CAF50', '#f44336']),
            hoverinfo='label+percent+value'
        )])
        
        fig.update_layout(
            title="📊 Attendance Distribution",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PARENT DASHBOARD WITH ANALYTICS
# ============================================================

def create_parent_analytics_dashboard(student_data):
    """Create parent-focused analytics dashboard"""
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    performance_status = "🟢 Excellent" if student_data['cgpa'] >= 8 else "🟡 Good" if student_data['cgpa'] >= 6 else "🔴 Needs Attention"
    
    with col1:
        st.metric("Academic Status", performance_status)
    
    with col2:
        st.metric("Current CGPA", f"{student_data['cgpa']:.2f}/10")
    
    with col3:
        st.metric("Attendance", f"{student_data['attendance']}%")
    
    with col4:
        days_since_update = random.randint(1, 7)
        st.metric("Last Updated", f"{days_since_update} days ago")
    
    st.markdown("---")
    
    # Subject-wise performance
    st.subheader("📚 Subject-wise Performance")
    
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'Programming', 'Database']
    marks = [random.randint(65, 95) for _ in subjects]
    
    fig = go.Figure(data=[
        go.Bar(
            x=subjects,
            y=marks,
            marker_color=['#667eea' if m >= 75 else '#ffa500' if m >= 60 else '#ff6b6b' for m in marks],
            text=marks,
            textposition='outside',
        )
    ])
    
    fig.update_layout(
        title="Subject-wise Marks",
        xaxis_title="Subject",
        yaxis_title="Marks (%)",
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Performance comparison with class average
    st.subheader("📊 Class Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart for comparison
        categories = ['CGPA', 'Attendance', 'Participation', 'Assignments', 'Exam Performance']
        student_values = [
            student_data['cgpa'] / 10 * 100,
            student_data['attendance'],
            random.randint(60, 95),
            random.randint(70, 95),
            random.randint(65, 90)
        ]
        class_avg = [75, 80, 70, 75, 72]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=student_values,
            theta=categories,
            fill='toself',
            name='Your Child',
            line=dict(color='#667eea')
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=class_avg,
            theta=categories,
            fill='toself',
            name='Class Average',
            line=dict(color='#ffa500')
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Counseling sessions chart
        sessions_data = {
            'Academic': random.randint(2, 8),
            'Personal': random.randint(1, 5),
            'Career': random.randint(1, 4),
            'Mental Health': random.randint(0, 3)
        }
        
        fig = go.Figure(data=[go.Bar(
            x=list(sessions_data.keys()),
            y=list(sessions_data.values()),
            marker_color=['#667eea', '#764ba2', '#4CAF50', '#ff9800'],
            text=list(sessions_data.values()),
            textposition='outside'
        )])
        
        fig.update_layout(
            title="Counseling Sessions by Type",
            xaxis_title="Session Type",
            yaxis_title="Number of Sessions",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# COUNSELOR ANALYTICS DASHBOARD
# ============================================================

def create_counselor_analytics_dashboard(counselor_id, students_data):
    """Create counselor analytics dashboard"""
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Students Assigned", len(students_data))
    
    with col2:
        avg_cgpa = sum([s['cgpa'] for s in students_data]) / len(students_data) if students_data else 0
        st.metric("📊 Avg CGPA", f"{avg_cgpa:.2f}")
    
    with col3:
        risk_students = len([s for s in students_data if s['cgpa'] < 5.5])
        st.metric("🔴 At-Risk Students", risk_students)
    
    with col4:
        excellent_students = len([s for s in students_data if s['cgpa'] >= 8])
        st.metric("⭐ Excellent Students", excellent_students)
    
    st.markdown("---")
    
    # Students distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        # CGPA Distribution
        cgpas = [s['cgpa'] for s in students_data]
        
        fig = go.Figure(data=[go.Histogram(
            x=cgpas,
            nbinsx=10,
            name='CGPA Distribution',
            marker_color='#667eea'
        )])
        
        fig.update_layout(
            title="CGPA Distribution",
            xaxis_title="CGPA",
            yaxis_title="Number of Students",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Performance breakdown
        performance_categories = {
            'Excellent (8+)': len([s for s in students_data if s['cgpa'] >= 8]),
            'Good (6-8)': len([s for s in students_data if 6 <= s['cgpa'] < 8]),
            'Average (5-6)': len([s for s in students_data if 5 <= s['cgpa'] < 6]),
            'Below Avg (<5)': len([s for s in students_data if s['cgpa'] < 5])
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(performance_categories.keys()),
            values=list(performance_categories.values()),
            marker=dict(colors=['#4CAF50', '#2196F3', '#ff9800', '#f44336']),
            hoverinfo='label+percent+value'
        )])
        
        fig.update_layout(
            title="Student Performance Breakdown",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ALERT SYSTEM FOR PARENTS
# ============================================================

def create_alert_card(alert_type, student_name, message, severity="info"):
    """Create an alert card for parent notifications"""
    
    color_map = {
        "success": "#4CAF50",
        "warning": "#ff9800",
        "danger": "#f44336",
        "info": "#2196F3"
    }
    
    icon_map = {
        "success": "✅",
        "warning": "⚠️",
        "danger": "🚨",
        "info": "ℹ️"
    }
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color_map.get(severity, '#2196F3')} 0%, 
        {color_map.get(severity, '#2196F3')}dd 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid white;
    ">
        <div style="font-weight: 600; font-size: 1.1em;">
            {icon_map.get(severity, '❓')} {alert_type}
        </div>
        <div style="opacity: 0.95; margin-top: 5px;">
            <strong>{student_name}</strong><br>
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PERFORMANCE HEALTH CHECK
# ============================================================

def get_health_status(student_data):
    """Determine student health status based on metrics"""
    
    cgpa = student_data['cgpa']
    attendance = student_data['attendance']
    
    if cgpa >= 7.5 and attendance >= 85:
        return "🟢 Excellent", "#4CAF50"
    elif cgpa >= 6.0 and attendance >= 75:
        return "🟡 Good", "#ff9800"
    elif cgpa >= 5.0 and attendance >= 70:
        return "🟠 Fair", "#ff6b6b"
    else:
        return "🔴 At Risk", "#f44336"

# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def get_recommendations(student_data):
    """Generate personalized recommendations for student"""
    
    recommendations = []
    
    if student_data['cgpa'] < 5.5:
        recommendations.append({
            'title': 'Academic Support',
            'message': 'Your CGPA is below the passing threshold. Please connect with your counselor for academic support.',
            'type': 'danger'
        })
    elif student_data['cgpa'] < 6.5:
        recommendations.append({
            'title': 'Improve Performance',
            'message': 'Focus on improving your marks. Consider attending tutoring sessions.',
            'type': 'warning'
        })
    
    if student_data['attendance'] < 75:
        recommendations.append({
            'title': 'Attendance Alert',
            'message': 'Your attendance is below 75%. Ensure regular class participation.',
            'type': 'danger'
        })
    elif student_data['attendance'] < 80:
        recommendations.append({
            'title': 'Maintain Attendance',
            'message': 'Try to improve your attendance. Aim for 85% or above.',
            'type': 'warning'
        })
    
    if not recommendations:
        recommendations.append({
            'title': 'Keep Up the Good Work!',
            'message': 'You are performing well. Continue to maintain your focus and dedication.',
            'type': 'success'
        })
    
    return recommendations
