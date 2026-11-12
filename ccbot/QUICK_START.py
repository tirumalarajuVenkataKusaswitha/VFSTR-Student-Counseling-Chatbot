"""
Quick Start Guide
Easy steps to run the Vignan AI Counselor Bot
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║     🎓 VIGNAN AI COUNSELOR BOT - QUICK START GUIDE 🎓         ║
╚════════════════════════════════════════════════════════════════╝

📋 PREREQUISITE SETUP
─────────────────────────────────────────────────────────────────

1. GET GROQ API KEY:
   • Visit: https://console.groq.com
   • Sign up or login
   • Create API key
   • Keep it safe!

2. INSTALL PYTHON PACKAGES:
   
   Open Terminal/PowerShell in project directory and run:
   
   pip install -r requirements.txt

3. SET GROQ API KEY:
   
   Option A - Windows PowerShell:
   $env:GROQ_API_KEY = "your-groq-api-key-here"
   
   Option B - Create .env file:
   Create a file named '.env' in the project folder with:
   GROQ_API_KEY=your-groq-api-key-here
   
   Option C - Windows Command Prompt:
   set GROQ_API_KEY=your-groq-api-key-here


🚀 RUNNING THE APPLICATION
─────────────────────────────────────────────────────────────────

FIRST TIME SETUP:
1. Run: python setup.py
   • Generates 100 students with R22 marks
   • Creates database
   • Shows demo credentials

EVERY TIME YOU RUN:
2. Run: streamlit run app.py
   • Opens in browser at http://localhost:8501
   • Login with demo credentials


👥 DEMO CREDENTIALS
─────────────────────────────────────────────────────────────────

STUDENT LOGIN:
Username: student_001
Password: student123

PARENT LOGIN:
Username: parent_001
Password: parent123

COUNSELOR LOGIN:
Username: counselor_001
Password: counselor123


📊 WHAT YOU'LL SEE
─────────────────────────────────────────────────────────────────

👤 STUDENT VIEW:
   • Personal dashboard with CGPA and attendance
   • Subject-wise marks and grades
   • AI Counselor chat (24/7 support)
   • Study resources and tips
   • Counseling requests

👨‍👩‍👧 PARENT VIEW:
   • Child's academic progress
   • Subject performance details
   • Attendance tracking
   • Real-time alerts
   • Counselor communication

🎯 COUNSELOR VIEW:
   • Dashboard overview (all students)
   • Priority student list
   • AI chat to counsel students
   • Student notes and records
   • Department analytics


✨ KEY FEATURES
─────────────────────────────────────────────────────────────────

✓ 100 Realistic Student Records
✓ R22 Regulation Marks System
✓ AI-Powered Counselor (Groq)
✓ Real-Time Performance Alerts
✓ Multi-Role Access Control
✓ Beautiful Dashboards
✓ Instant Messaging
✓ Department Analytics
✓ Meeting Scheduling
✓ 24/7 AI Support


💡 TIPS
─────────────────────────────────────────────────────────────────

• Try all 3 roles to see different interfaces
• AI Counselor learns from conversation history
• Explore different student profiles
• Check department analytics
• Test alert notifications
• Try different filters and searches


🔧 TROUBLESHOOTING
─────────────────────────────────────────────────────────────────

Problem: "GROQ_API_KEY not found"
Solution: Make sure you set the environment variable

Problem: "Student data not found"
Solution: Run 'python setup.py' first

Problem: "ModuleNotFoundError"
Solution: Run 'pip install -r requirements.txt'

Problem: "Port already in use"
Solution: Run 'streamlit run app.py --server.port=8502'


📚 PROJECT FILES
─────────────────────────────────────────────────────────────────

Main Files:
• app.py ........................ Main Streamlit application
• setup.py ...................... Setup and initialization
• database.py ................... Authentication & database
• ai_counselor.py ............... AI Counselor module
• generate_student_data.py ...... Student data generator
• utils.py ...................... Utility functions

Dashboards (pages/):
• student_dashboard.py .......... Student interface
• parent_dashboard.py ........... Parent interface
• counselor_dashboard.py ........ Counselor interface

Additional Pages (pages/):
• student_counselor_chat.py ..... AI chat for students
• student_resources.py .......... Study resources
• parent_messages.py ............ Parent messaging
• parent_alerts.py .............. Parent notifications
• counselor_students.py ......... Manage students
• counselor_notes.py ............ Counseling records

Data Files:
• student_data.json ............ 100 student records (auto-generated)
• app_database.json ............ Application database
• requirements.txt ............. Python packages


🎓 FEATURES EXPLAINED
─────────────────────────────────────────────────────────────────

R22 REGULATION MARKS:
T1 = 20 marks (Internal Assessment 1)
T2 = 5 marks (Internal Assessment 2)
T3 = 5 marks (Internal Assessment 3)
T4 = 20 marks (Internal Assessment 4)
M1_A1 = 20 marks (Module 1, Assessment 1)
M1_A2 = 20 marks (Module 1, Assessment 2)
M2_A1 = 20 marks (Module 2, Assessment 1)
M2_A2 = 20 marks (Module 2, Assessment 2)
─────────────────────
TOTAL = 130 marks per subject

CGPA CALCULATION:
Percentage = (Total / 130) × 100
CGPA = Average of all 6 subjects × 0.1

HEALTH SCORE:
• 40% weight: CGPA
• 40% weight: Attendance
• 20% weight: Warnings


🌟 NEXT STEPS
─────────────────────────────────────────────────────────────────

1. Run setup.py to generate data
2. Start app with 'streamlit run app.py'
3. Login with demo credentials
4. Explore all three dashboards
5. Try the AI Counselor chat
6. Check analytics and alerts
7. Customize for your institution


📞 SUPPORT
─────────────────────────────────────────────────────────────────

For issues or questions, refer to:
• SETUP_GUIDE.md (detailed setup guide)
• README.md (project overview)
• Check error messages carefully


════════════════════════════════════════════════════════════════

Ready to use? Run these commands:

1. python setup.py
2. streamlit run app.py

Enjoy the Vignan AI Counselor Bot! 🚀

════════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    input("\nPress Enter to close this guide...")
