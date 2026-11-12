"""
Student - Chat with Counselor Page
"""

import streamlit as st
from ai_counselor import ai_counselor
from database import db
from utils import get_student_by_id

st.set_page_config(page_title="Chat with Counselor", layout="wide")

def require_role(required_role):
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access this page")
        st.stop()
    if st.session_state.get("role") != required_role:
        st.error(f"Access denied. This page is only available to {required_role.title()} users.")
        st.stop()


def show_student_chat():
    """Student chat interface"""
    require_role("student")
    
    st.title("💬 Chat with Counselor")
    
    # Get current student
    student_id = st.session_state.user.get("student_id", "2310001")
    student = get_student_by_id(student_id)
    
    if not student:
        st.error("Student profile not found")
        return
    
    # Sidebar - Select Counselor or AI
    with st.sidebar:
        st.markdown("### 🎯 Counselor Selection")
        counselor_type = st.radio("Choose:", ["🤖 AI Counselor", "👨‍💼 Request Human Counselor"])
    
    if counselor_type == "🤖 AI Counselor":
        show_ai_counselor_chat(student)
    else:
        show_human_counselor_request(student)

def show_ai_counselor_chat(student):
    """Display AI counselor chat"""
    
    st.subheader("🤖 AI Counselor Chat")
    st.info("Chat with our AI-powered counselor for academic and personal guidance.")
    
    # Initialize conversation history
    if "ai_conversation" not in st.session_state:
        st.session_state.ai_conversation = []
        # Add initial message
        st.session_state.ai_conversation.append({
            "role": "assistant",
            "content": f"Hello {student['name']}! 👋 I'm your AI Counselor. I'm here to help you with academic guidance, career planning, and personal well-being. How can I assist you today?"
        })
    
    # Display conversation
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.ai_conversation:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])
    
    st.markdown("---")
    
    # User input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message
        st.session_state.ai_conversation.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        system_prompt = ai_counselor.get_counselor_system_prompt(
            "AI Counselor Bot",
            "General Academic & Personal Counseling",
            ["Time Management", "Study Skills", "Career Guidance", "Stress Management"],
            {
                'name': student['name'],
                'cgpa': student['cgpa'],
                'attendance': student['attendance'],
                'department': student['department'],
                'concerns': user_input
            }
        )
        
        with st.spinner("🤔 Thinking..."):
            response = ai_counselor.get_ai_response(
                user_input,
                st.session_state.ai_conversation,
                system_prompt
            )
        
        st.session_state.ai_conversation.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()

def show_human_counselor_request(student):
    """Show request form for human counselor"""
    
    st.subheader("👨‍💼 Request Human Counselor")
    
    with st.form("counselor_request"):
        st.markdown("### Schedule a Counseling Session")
        
        counselor_type = st.selectbox(
            "Type of Counseling Needed:",
            ["Academic Guidance", "Career Planning", "Mental Health & Wellness", "Personal Issues"]
        )
        
        preferred_time = st.select_slider(
            "Preferred Time:",
            options=["Morning (9-12)", "Afternoon (12-3)", "Evening (3-6)"]
        )
        
        message = st.text_area("Describe your concern (optional):")
        
        submit = st.form_submit_button("📤 Submit Request")
        
        if submit:
            # Save request to database
            db.add_message(
                student_id=student['student_id'],
                receiver_id="counselor_pool",
                message=f"Type: {counselor_type} | Time: {preferred_time} | Message: {message}",
                message_type="counselor_request"
            )
            
            st.success("✅ Your counseling request has been submitted! A counselor will contact you within 24 hours.")

if __name__ == "__main__":
    show_student_chat()
