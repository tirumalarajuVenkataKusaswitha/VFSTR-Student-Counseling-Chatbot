"""
Parent - Messages Page
Communication with counselors and school
"""

import streamlit as st
from datetime import datetime
from database import db

st.set_page_config(page_title="Messages", layout="wide")

def require_role(required_role):
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access this page")
        st.stop()
    if st.session_state.get("role") != required_role:
        st.error(f"Access denied. This page is only available to {required_role.title()} users.")
        st.stop()

require_role("parent")

st.title("💬 Messages & Communication")

tabs = st.tabs(["📧 Inbox", "✍️ Compose", "📤 Sent"])

with tabs[0]:
    st.subheader("📧 Inbox")
    
    # Get messages for parent
    user_messages = db.get_messages(st.session_state.username, st.session_state.role)
    incoming = [m for m in user_messages if m["receiver_id"] == st.session_state.username]
    
    if incoming:
        for msg in sorted(incoming, key=lambda x: x["timestamp"], reverse=True):
            with st.expander(f"From: {msg['sender_id']} - {msg['timestamp'][:10]}"):
                st.write(msg["message"])
                if st.button(f"Reply", key=f"reply_{msg['id']}"):
                    st.session_state.reply_to = msg["sender_id"]
                    st.rerun()
    else:
        st.info("No messages in inbox")

with tabs[1]:
    st.subheader("✍️ Compose Message")
    
    with st.form("compose_message"):
        recipient = st.selectbox(
            "Send to:",
            ["Counselor Pool", "Principal", "Class Advisor"]
        )
        
        subject = st.text_input("Subject:")
        message = st.text_area("Message:")
        
        if st.form_submit_button("📤 Send"):
            if subject and message:
                db.add_message(
                    st.session_state.username,
                    recipient.lower(),
                    f"Subject: {subject}\n\n{message}"
                )
                st.success("✅ Message sent!")
            else:
                st.error("Please fill all fields")

with tabs[2]:
    st.subheader("📤 Sent Messages")
    
    user_messages = db.get_messages(st.session_state.username, st.session_state.role)
    sent = [m for m in user_messages if m["sender_id"] == st.session_state.username]
    
    if sent:
        for msg in sorted(sent, key=lambda x: x["timestamp"], reverse=True):
            with st.expander(f"To: {msg['receiver_id']} - {msg['timestamp'][:10]}"):
                st.write(msg["message"])
    else:
        st.info("No sent messages")
        
        if sent:
            for msg in sorted(sent, key=lambda x: x["timestamp"], reverse=True):
                with st.expander(f"To: {msg['receiver_id']} - {msg['timestamp'][:10]}"):
                    st.write(msg["message"])
        else:
            st.info("No sent messages")
