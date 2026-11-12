# 🎓 Vignan AI Counselor Bot

**Advanced Student Counseling & Academic Support System**

A comprehensive multi-role Streamlit application designed for educational institutions to provide intelligent counseling, academic guidance, and student support through AI integration.

## ✨ Features

### 📊 **Three Role-Based Interfaces**

#### 👤 **Student Dashboard**
- Personal academic performance metrics (CGPA, Attendance, Marks)
- Subject-wise analysis and performance trends
- Health indicator (overall academic status)
- Quick actions for counseling requests
- Parent contact information
- Personalized recommendations

#### 👨‍👩‍👧 **Parent Dashboard**
- Monitor child's academic progress
- View subject-wise performance details
- Track attendance status
- Receive alerts for critical issues
- Communication with counselors
- Performance analytics

#### 🎯 **Counselor Dashboard**
- Priority-based student identification
- AI-assisted student counseling chat
- Student notes and records management
- Analytics by department
- Top performers tracking
- Comprehensive student profiles
- Meeting scheduling

### 🤖 **AI-Powered Features**
- **Intelligent Counselor Bot**: Uses Groq AI for context-aware student counseling
- **Natural Language Processing**: Understands student concerns and provides personalized guidance
- **Automated Student Assessment**: Identifies students needing intervention
- **Smart Recommendations**: Provides academic and wellness guidance

### 📈 **Academic Management**
- **R22 Regulation Compliance**
  - T1 = 20 marks
  - T2 = 5 marks
  - T3 = 5 marks
  - T4 = 20 marks
  - 4 Module Assessments = 20 marks each
  - Total = 130 marks per subject

- **100 Sample Students** with realistic data across:
  - 6 subjects
  - 5 departments
  - Multiple semesters
  - Various performance levels

- **Attendance Tracking**: Monitor class attendance (70-98%)
- **Performance Metrics**: CGPA, Grade distribution, trend analysis
- **Alert System**: Automatic alerts for low performance/attendance

### 🔐 **Security & Authentication**
- Secure login system with role-based access control
- Encrypted password storage
- Session management
- User profile customization

### 📞 **Communication**
- Counselor messaging system
- Student-Counselor interaction
- Parent-School communication
- Counseling request management
- Follow-up scheduling

## 🏗️ Project Structure

```
ccbot/
├── app.py                          # Main Streamlit application
├── setup.py                        # Setup and initialization script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── database.py                     # Database & Authentication management
├── generate_student_data.py        # Student data generator (100 students)
├── ai_counselor.py                 # AI counselor module (Groq integration)
├── utils.py                        # Utility functions
│
├── pages/
│   ├── student_dashboard.py        # Student main dashboard
│   ├── student_counselor_chat.py   # Student AI chat interface
│   ├── student_resources.py        # Study tips & resources
│   ├── parent_dashboard.py         # Parent monitoring dashboard
│   ├── parent_messages.py          # Parent messaging
│   ├── parent_alerts.py            # Parent alerts & notifications
│   ├── counselor_dashboard.py      # Counselor main dashboard
│   ├── counselor_students.py       # Counselor student management
│   └── counselor_notes.py          # Counselor notes & records
│
├── clg_data/
│   └── career_guidance.csv         # Career guidance resources
│
├── student_data.json               # Generated student data (100 students)
├── app_database.json               # Application database & logs
└── chat.json                       # Chat history
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- GROQ API Key ([Get free key](https://console.groq.com))

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set GROQ API Key

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY = "your-groq-api-key"
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=your-groq-api-key
```

**Or create .env file in project root:**
```
GROQ_API_KEY=your-groq-api-key
```

### Step 3: Generate Student Data & Initialize Database

```bash
python setup.py
```

This will:
- ✅ Generate 100 student records with R22 regulation marks
- ✅ Initialize database with default users
- ✅ Create configuration files
- ✅ Display demo credentials

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 👥 Demo Credentials

### 👤 Student Account
```
Username: student_001
Password: student123
```

### 👨‍👩‍👧 Parent Account
```
Username: parent_001
Password: parent123
```

### 🎯 Counselor Account
```
Username: counselor_001
Password: counselor123
```

## 📋 Features Overview

### Student Features
- ✅ View academic performance and CGPA
- ✅ Subject-wise marks and grades
- ✅ Attendance tracking
- ✅ Health status indicator
- ✅ AI Counselor chat (24/7)
- ✅ Request human counselor meetings
- ✅ Access study resources and tips
- ✅ View recommendations
- ✅ Achievement tracking

### Parent Features
- ✅ Monitor child's academic progress
- ✅ View detailed subject performance
- ✅ Track attendance
- ✅ Receive real-time alerts
- ✅ View CGPA and grades
- ✅ Contact counselors
- ✅ Request meetings
- ✅ View counselor notes (with permission)
- ✅ Communication inbox

### Counselor Features
- ✅ Dashboard overview of all students
- ✅ Identify high-priority students
- ✅ AI-assisted student counseling
- ✅ Maintain detailed student notes
- ✅ Schedule meetings
- ✅ Track student progress
- ✅ Analytics by department
- ✅ Message students and parents
- ✅ Generate counseling plans
- ✅ View top performers

## 🤖 AI Counselor Features

The AI counselor uses **Groq's Mixtral model** and provides:

- **Context-Aware Responses**: Understands individual student situations
- **Personalized Guidance**: Based on CGPA, attendance, and department
- **24/7 Availability**: Instant support for students
- **Smart Specialization**: Counselor-specific expertise (Academic, Mental Health, Career)
- **Conversation History**: Maintains context across sessions
- **Empathetic Approach**: Warm and supportive tone

### Example Interactions
```
Student: "I'm struggling with Data Structures"
AI: "I understand! Data Structures can be challenging. 
     Try the Feynman Technique - explain each concept simply.
     Would you like specific tips for [topic]?"

Parent: "My child has low attendance"
AI: "This is concerning. Let's identify barriers:
     - Transportation issues?
     - Health problems?
     - Lack of interest?
     Let's create an action plan together."
```

## 📊 Data Structure

### Student Record (R22 Regulation)
```json
{
  "student_id": "2310001",
  "name": "Arjun Sharma",
  "department": "CSE",
  "cgpa": 7.45,
  "attendance": 85,
  "marks": {
    "Data Structures": {
      "T1": 19,
      "T2": 5,
      "T3": 4,
      "T4": 18,
      "M1_A1": 18,
      "M1_A2": 19,
      "M2_A1": 17,
      "M2_A2": 18,
      "Total": 118,
      "Percentage": 90.77,
      "Grade": "A+"
    }
  },
  "warnings": 0,
  "needs_counseling": false
}
```

## 🔒 Security Considerations

- Passwords are hashed using SHA-256
- Role-based access control
- Session-based authentication
- Confidentiality of counseling notes
- Parental access restrictions
- Audit logging (in production)

## ⚙️ Configuration

### Marks Structure (R22)
Modify in `generate_student_data.py`:
```python
MARKS_STRUCTURE = {
    "T1": 20,      # Internal Assessment 1
    "T2": 5,       # Internal Assessment 2
    "T3": 5,       # Internal Assessment 3
    "T4": 20,      # Internal Assessment 4
    "M1_A1": 20,   # Module 1 Assessment 1
    "M1_A2": 20,   # Module 1 Assessment 2
    "M2_A1": 20,   # Module 2 Assessment 1
    "M2_A2": 20,   # Module 2 Assessment 2
}
```

### Departments
Edit in `generate_student_data.py`:
```python
DEPARTMENTS = ["CSE", "ECE", "ME", "EEE", "CIVIL"]
```

### Subjects
Edit in `generate_student_data.py`:
```python
SUBJECTS = [
    "Data Structures",
    "Database Management",
    "Web Technologies",
    # ... add more subjects
]
```

## 🐛 Troubleshooting

### Issue: GROQ_API_KEY not found
**Solution**: Set environment variable or create .env file

### Issue: Student data not generating
**Solution**: Run `python setup.py` again

### Issue: Streamlit not starting
**Solution**: Ensure Streamlit is installed: `pip install streamlit --upgrade`

### Issue: Database corruption
**Solution**: Delete `app_database.json` and run `python setup.py`

## 📈 Future Enhancements

- [ ] Mobile app integration
- [ ] Video counseling sessions
- [ ] Advanced analytics dashboard
- [ ] Machine learning-based student performance prediction
- [ ] Multi-language support
- [ ] Integration with college ERP systems
- [ ] Export reports (PDF/Excel)
- [ ] SMS/Email notifications
- [ ] Voice-based counseling
- [ ] Peer learning groups

## 📞 Support & Contact

For issues or feature requests:
- 📧 Email: support@vignan.ac.in
- 🎓 Portal: www.vignan.ac.in

## 📄 License

This project is provided as-is for educational purposes.

## 👨‍💼 Development Team

**Vignan University - AI & ML Department**

---

## 🎯 Key Statistics

- **100 Students** across 6 departments
- **6 Subjects** per student with R22 regulation marks
- **3 Roles** (Student, Parent, Counselor)
- **5 Departments** coverage
- **8 Semesters** of academic progression
- **Real-time Analytics** and dashboards

## 🌟 Highlights

✨ **AI-Powered**: Groq AI integration for intelligent counseling  
✨ **Multi-Role**: Tailored interfaces for students, parents, counselors  
✨ **Comprehensive**: Complete academic and counseling management  
✨ **Real-time**: Instant alerts and notifications  
✨ **Scalable**: Support for institution-wide deployment  
✨ **User-Friendly**: Intuitive and interactive UI  

---

**Built with ❤️ using Streamlit, Groq AI, and Python**
