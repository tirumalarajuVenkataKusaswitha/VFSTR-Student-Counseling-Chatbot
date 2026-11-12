"""
Counselor - Notes Page
Maintain counseling notes and records for students
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from database import db
from utils import load_student_data

st.set_page_config(page_title="Counseling Notes", layout="wide")

def require_role(required_role):
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please login to access this page")
        st.stop()
    if st.session_state.get("role") != required_role:
        st.error(f"Access denied. This page is only available to {required_role.title()} users.")
        st.stop()

require_role("counselor")

st.title("?? Counseling Notes & Records")

tabs = st.tabs(["?? Add Note", "?? View Notes", "?? Statistics"])

with tabs[0]:
    st.subheader("?? Add Counseling Note")
    
    # Get all students for selection
    all_students = load_student_data()
    student_options = {f"{s['name']} ({s['student_id']})": s for s in all_students}
    
    with st.form("add_note_form"):
        student_select = st.selectbox("Select Student:", list(student_options.keys()))
        selected_student = student_options[student_select]
        
        note_type = st.selectbox(
            "Note Type:",
            ["General", "Academic", "Mental Health", "Career", "Attendance", "Progress Review"]
        )
        
        note_content = st.text_area("Counseling Note:", height=200)
        
        follow_up = st.checkbox("Schedule Follow-up")
        if follow_up:
            follow_up_date = st.date_input("Follow-up Date:")
        
        tags = st.multiselect(
            "Tags:",
            ["CGPA", "Attendance", "Family", "Health", "Career", "Social", "Other"]
        )
        
        if st.form_submit_button("?? Save Note"):
            if note_content:
                note = db.add_counseling_note(
                    counselor_id=st.session_state.username,
                    student_id=selected_student['student_id'],
                    note=f"""
**Type**: {note_type}
**Tags**: {', '.join(tags)}
**Content**: {note_content}
**Follow-up**: {'Yes - ' + str(follow_up_date) if follow_up else 'No'}
                    """,
                    note_type=note_type.lower()
                )
                st.success(f"? Note saved for {selected_student['name']}")
            else:
                st.error("Please enter the counseling note")

with tabs[1]:
    st.subheader("?? View Counseling Notes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_student = st.text_input("?? Search by student name/ID:")
    
    with col2:
        note_filter = st.selectbox(
            "Filter by type:",
            ["All", "General", "Academic", "Mental Health", "Career", "Attendance"]
        )
    
    all_notes = db.db.get("counseling_notes", [])
    
    if search_student:
        all_notes = [n for n in all_notes if search_student.lower() in n.get("student_id", "").lower()]
    
    if note_filter != "All":
        all_notes = [n for n in all_notes if n.get("note_type") == note_filter.lower()]
    
    if all_notes:
        for note in sorted(all_notes, key=lambda x: x["timestamp"], reverse=True):
            with st.expander(
                f"?? {note['student_id']} | ?? {note['timestamp'][:10]} | ??? {note['note_type'].upper()}"
            ):
                st.write(note["note"])
                
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("?? Edit", key=f"edit_note_{note['id']}"):
                        st.info("Edit functionality coming soon")
                    if st.button("??? Delete", key=f"del_note_{note['id']}"):
                        st.warning("Delete functionality coming soon")
    else:
        st.info("No counseling notes found")

with tabs[2]:
    st.subheader("?? Counseling Statistics")
    
    all_notes = db.db.get("counseling_notes", [])
    
    if all_notes:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Notes", len(all_notes))
        
        with col2:
            unique_students = len(set([n["student_id"] for n in all_notes]))
            st.metric("Students Counseled", unique_students)
        
        with col3:
            follow_ups = len([n for n in all_notes if n.get("follow_up_date")])
            st.metric("Follow-ups", follow_ups)
        
        with col4:
            recent = len([n for n in all_notes if n["timestamp"][:10] == datetime.now().strftime("%Y-%m-%d")])
            st.metric("Today's Notes", recent)
        
        st.markdown("---")
        
        st.markdown("#### Note Type Distribution")
        
        note_types = {}
        for note in all_notes:
            nt = note.get("note_type", "general")
            note_types[nt] = note_types.get(nt, 0) + 1
        
        type_df = pd.DataFrame(list(note_types.items()), columns=["Type", "Count"])
        st.bar_chart(type_df.set_index("Type"))
        
        st.markdown("---")
        
        st.markdown("#### Most Counseled Students")
        
        student_counts = {}
        for note in all_notes:
            sid = note.get("student_id")
            student_counts[sid] = student_counts.get(sid, 0) + 1
        
        sorted_students = sorted(student_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for idx, (student_id, count) in enumerate(sorted_students, 1):
            st.write(f"{idx}. Student {student_id}: {count} notes")
    else:
        st.info("No statistics available yet")
