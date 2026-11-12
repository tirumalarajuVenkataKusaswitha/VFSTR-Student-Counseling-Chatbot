"""
AI Counselor Module - Enhanced ChatBot for Student Counseling
Provides intelligent responses based on student context
"""

import os
import json
from groq import Groq

class AICounselor:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "mixtral-8x7b-32768"
        
    def get_counselor_system_prompt(self, counselor_name, specialization, expertise, student_context=None):
        """Generate system prompt for counselor based on specialization"""
        
        base_prompt = f"""You are {counselor_name}, a professional counselor at Vignan University.
        
Specialization: {specialization}
Expertise Areas: {', '.join(expertise)}

Your role is to provide supportive, empathetic, and constructive guidance to students. 

GUIDELINES:
1. Be empathetic and non-judgmental
2. Provide actionable advice and practical strategies
3. Ask clarifying questions when needed
4. Refer to mental health professionals when necessary
5. Maintain confidentiality
6. Focus on student's strengths and growth
7. Be culturally sensitive
8. Keep responses concise but meaningful (3-5 sentences)

TONE: Warm, professional, supportive, and encouraging."""

        if student_context:
            base_prompt += f"""

STUDENT CONTEXT:
- Name: {student_context.get('name', 'N/A')}
- CGPA: {student_context.get('cgpa', 'N/A')}
- Attendance: {student_context.get('attendance', 'N/A')}%
- Department: {student_context.get('department', 'N/A')}
- Current Concerns: {student_context.get('concerns', 'General counseling')}

Use this context to personalize your responses."""
        
        return base_prompt
    
    def get_ai_response(self, message, conversation_history, system_prompt):
        """Get AI response from Groq"""
        try:
            # Build message history for context
            messages = []
            
            # Add previous messages for context (last 5)
            for prev_msg in conversation_history[-5:]:
                messages.append({
                    "role": prev_msg.get("role", "user"),
                    "content": prev_msg.get("content", "")
                })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                system=system_prompt,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"I apologize, I encountered an issue processing your message. Error: {str(e)}"
    
    def analyze_student_needs(self, student_data):
        """Analyze student data to identify counseling needs"""
        needs = []
        recommendations = []
        
        # Check CGPA
        if student_data.get("cgpa", 0) < 5.0:
            needs.append("🎓 Academic Performance - Low CGPA")
            recommendations.append("Focus on time management and subject-specific guidance")
        
        # Check Attendance
        if student_data.get("attendance", 100) < 75:
            needs.append("📚 Attendance - Below minimum required")
            recommendations.append("Discuss barriers to attendance and create action plan")
        
        # Check for warnings
        if student_data.get("warnings", 0) > 0:
            needs.append("⚠️ Academic Warnings - Multiple warnings issued")
            recommendations.append("Develop improvement strategy with clear milestones")
        
        # Check for failing subjects
        subject_marks = student_data.get("marks", {})
        failing_subjects = [subj for subj, marks in subject_marks.items() if marks.get("Percentage", 0) < 50]
        if failing_subjects:
            needs.append(f"❌ Failing Subjects - {len(failing_subjects)} subject(s)")
            recommendations.append(f"Remedial classes for: {', '.join(failing_subjects)}")
        
        return {
            "needs": needs if needs else ["✅ Student is performing well"],
            "recommendations": recommendations if recommendations else ["Continue current academic trajectory"],
            "priority": "High" if len(needs) > 2 else "Medium" if len(needs) == 1 else "Low"
        }
    
    def generate_counseling_plan(self, student_data, counselor_notes):
        """Generate personalized counseling plan"""
        plan = {
            "student_name": student_data.get("name"),
            "student_id": student_data.get("student_id"),
            "current_cgpa": student_data.get("cgpa"),
            "attendance": student_data.get("attendance"),
            "counseling_goals": [],
            "action_items": [],
            "follow_up_schedule": []
        }
        
        needs_analysis = self.analyze_student_needs(student_data)
        
        if "Academic Performance" in str(needs_analysis["needs"]):
            plan["counseling_goals"].append("Improve academic performance and CGPA")
            plan["action_items"].append("Weekly study sessions tracking")
            plan["follow_up_schedule"].append("Weekly check-ins for 4 weeks")
        
        if "Attendance" in str(needs_analysis["needs"]):
            plan["counseling_goals"].append("Improve attendance and class participation")
            plan["action_items"].append("Identify barriers and create attendance tracker")
            plan["follow_up_schedule"].append("Bi-weekly check-ins")
        
        if not plan["counseling_goals"]:
            plan["counseling_goals"].append("Maintain excellent academic performance")
            plan["action_items"].append("Continue current positive trajectory")
            plan["follow_up_schedule"].append("Monthly check-ins")
        
        return plan

# Initialize AI Counselor
ai_counselor = AICounselor()
