# 🎓 Vignan AI Counselor - Three-Portal System Setup Guide

## 📋 Overview

The enhanced Vignan AI Counselor platform now features three separate login portals for different user types:

1. **👤 Student Portal** - For students to manage their academic journey
2. **👨‍👩‍👧 Parent Portal** - For parents to monitor their child's progress
3. **🎯 Counselor Portal** - For counselors to manage student cases and analytics

Each portal has been enhanced with **Power BI** and **Tableau** dashboard capabilities for superior data visualization and analytics.

---

## 🚀 Quick Start

### Running the Application

#### Option 1: Use the Enhanced App (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the enhanced three-portal app
streamlit run app_enhanced.py
```

#### Option 2: Use the Original App
```bash
streamlit run app.py
```

---

## 🔐 Demo Credentials

### Student Login
- **Username:** `student_001`, `student_002`, `student_003`
- **Password:** `student123`

### Parent Login
- **Username:** `parent_001`, `parent_002`
- **Password:** `parent123`

### Counselor Login
- **Username:** `counselor_001`, `counselor_002`, `counselor_003`
- **Password:** `counselor123`

---

## 👤 Student Portal Features

### Dashboard
- 📊 Personal academic dashboard
- 📈 Performance tracking over time
- 📚 Subject-wise analysis
- 🎯 Personalized recommendations

### AI Counselor
- 🤖 AI-powered counseling chatbot
- 💬 Real-time academic guidance
- 🎯 Career counseling
- 🧠 Mental health support

### Resources
- 📚 Study materials
- 🎥 Video tutorials
- 📖 Subject guides
- 💡 Tips and tricks

---

## 👨‍👩‍👧 Parent Portal Features

### Enhanced Analytics Dashboard
- 📊 Interactive charts and visualizations
- 📈 CGPA trends (12-month view)
- 📊 Attendance pie charts
- 📚 Subject-wise performance bars

### Performance Comparison
- 📊 Radar charts comparing student vs class average
- 🎓 Performance breakdown by category
- 📊 Counseling sessions tracking
- 📈 Progress trends

### Real-time Alerts
- 🔴 Low CGPA alerts
- ⚠️ Attendance warnings
- ✅ Achievement notifications
- 📢 Counselor messages

### Personalized Recommendations
- 💡 Data-driven suggestions
- 📈 Academic improvement plans
- 🎯 Focus areas
- ✨ Success strategies

### Contact & Support
- 📧 Request counselor meetings
- 💬 Direct messaging with counselors
- 📝 View counselor notes (with permission)
- 🔔 Notification preferences

---

## 🎯 Counselor Portal Features

### Dashboard Analytics
- 👥 Student caseload overview
- 📊 CGPA distribution analysis
- 📈 Performance breakdown
- 🎓 Student categorization

### Student Management
- 👥 Manage assigned students
- 📊 Individual student analytics
- 📝 Session history
- 🎯 Progress tracking

### Session Recording
- 📝 Detailed session notes
- 📅 Schedule follow-ups
- 💾 Archive old records
- 🔍 Quick search

### Advanced Analytics
- 📊 Tableau dashboards
- 📈 Trend analysis
- 🎓 Performance metrics
- 📊 Statistical reports

---

## 🔌 Power BI & Tableau Integration

### Power BI Setup

#### 1. Connect to Power BI Service
```python
from azure.identity import InteractiveBrowserCredential
from dashboard_utils import embed_powerbi_dashboard

# Get your Power BI report ID and access token
report_id = "YOUR_REPORT_ID"
access_token = "YOUR_ACCESS_TOKEN"

# Embed in Streamlit
embed_powerbi_dashboard(report_id, access_token)
```

#### 2. Environment Variables
Create a `.env` file:
```
POWERBI_CLIENT_ID=your_client_id
POWERBI_CLIENT_SECRET=your_client_secret
POWERBI_TENANT_ID=your_tenant_id
```

#### 3. Enable Power BI in App
Update `app_enhanced.py` to include:
```python
# In parent dashboard section
if st.checkbox("📊 Show Power BI Dashboard"):
    embed_powerbi_dashboard(
        report_id="your_report_id",
        access_token=st.secrets.get("powerbi_token")
    )
```

### Tableau Setup

#### 1. Create Tableau Dashboards
- Create dashboards in Tableau Server/Online
- Configure public or embedded sharing
- Generate public URL

#### 2. Embed in Streamlit
```python
from dashboard_utils import embed_tableau_dashboard

# Embed Tableau dashboard
tableau_url = "https://your-tableau-server.com/views/YourDashboard"
embed_tableau_dashboard(tableau_url)
```

#### 3. Tableau Server Configuration
```
Tableau Server URL: https://your-tableau-server.com
Trusted Ticket Enabled: Yes
Embedded Authentication: Enabled
```

---

## 📊 Dashboard Components

### For Parents

#### Interactive Performance Chart
```python
# CGPA Trend (12 months)
# Attendance Distribution (Pie Chart)
# Subject Performance (Bar Chart)
# Performance Comparison (Radar Chart)
# Counseling Sessions (Bar Chart)
```

#### Health Status Indicators
- 🟢 **Excellent:** CGPA ≥ 7.5, Attendance ≥ 85%
- 🟡 **Good:** CGPA ≥ 6.0, Attendance ≥ 75%
- 🟠 **Fair:** CGPA ≥ 5.0, Attendance ≥ 70%
- 🔴 **At Risk:** Below thresholds

### For Students

#### Performance Metrics
- 📊 CGPA display
- ✅ Attendance percentage
- 📚 Subjects count
- ⭐ Performance rating

#### Interactive Charts
- 📈 CGPA trend line
- 📊 Attendance pie chart
- 📚 Subject performance
- 🎯 Monthly progress

---

## 🔧 File Structure

```
ccbot/
├── app_enhanced.py                 # Main app with three-portal login
├── app.py                          # Original app
├── dashboard_utils.py              # Power BI/Tableau integration utilities
├── requirements.txt                # Updated with BI dependencies
├── database.py                     # Authentication and data management
├── pages/
│   ├── student_dashboard.py       # Student dashboard
│   ├── parent_dashboard.py        # Enhanced parent dashboard with BI
│   ├── counselor_dashboard.py     # Counselor dashboard
│   ├── student_counselor_chat.py
│   ├── student_resources.py
│   ├── parent_messages.py
│   ├── parent_alerts.py
│   ├── counselor_students.py
│   └── counselor_notes.py
└── ...
```

---

## 🔐 Security Features

### Authentication
- ✅ Password hashing (SHA-256)
- ✅ Role-based access control
- ✅ Session management
- ✅ Logout functionality

### Data Protection
- ✅ Encrypted credentials storage
- ✅ Secure session state
- ✅ HTTPS enforcement (production)
- ✅ Field-level permissions

---

## 🚨 Troubleshooting

### Login Issues
```
Issue: Invalid credentials error
Solution: Ensure username exists and password is correct (case-sensitive)

Issue: Session not persisting
Solution: Check st.session_state initialization in app_enhanced.py
```

### Dashboard Issues
```
Issue: Charts not rendering
Solution: Verify plotly and kaleido are installed

Issue: Power BI not loading
Solution: Check Power BI access token and report ID validity
```

### Performance Issues
```
Issue: Slow dashboard loading
Solution: Reduce chart complexity or optimize data queries

Issue: Memory errors
Solution: Implement data caching using st.cache_data
```

---

## 📈 Customization Guide

### Add New Dashboard Metrics

1. **Edit `dashboard_utils.py`:**
```python
def create_custom_metric(data):
    """Create custom metric"""
    metric_value = calculate_metric(data)
    st.metric("Metric Name", metric_value)
```

2. **Use in Dashboard:**
```python
from dashboard_utils import create_custom_metric
create_custom_metric(student_data)
```

### Modify Alert Thresholds

Edit `dashboard_utils.py`:
```python
def get_health_status(student_data):
    cgpa = student_data['cgpa']
    
    if cgpa >= 7.5:  # Modify threshold
        return "🟢 Excellent", "#4CAF50"
```

### Add New Features

1. Create new page in `pages/` directory
2. Import in `app_enhanced.py`
3. Add navigation link in sidebar
4. Implement feature logic

---

## 📚 API Reference

### dashboard_utils.py Functions

```python
# Power BI
embed_powerbi_dashboard(report_id, access_token, height=800)

# Tableau
embed_tableau_dashboard(dashboard_url, height=800)

# Dashboards
create_student_performance_dashboard(student_data)
create_parent_analytics_dashboard(student_data)
create_counselor_analytics_dashboard(counselor_id, students_data)

# Utilities
create_alert_card(alert_type, student_name, message, severity)
get_health_status(student_data)
get_recommendations(student_data)
```

---

## 🎯 Best Practices

### For Parents
- ✅ Check dashboard weekly
- ✅ Review real-time alerts immediately
- ✅ Communicate with counselors
- ✅ Set realistic academic goals

### For Students
- ✅ Update profile information
- ✅ Attend counseling sessions
- ✅ Review recommendations
- ✅ Track progress regularly

### For Counselors
- ✅ Document all sessions
- ✅ Set follow-up schedules
- ✅ Use analytics for insights
- ✅ Maintain confidentiality

---

## 📞 Support & Resources

### Documentation
- 📖 See [README.md](README.md) for general info
- 📖 See [START_HERE.md](START_HERE.md) for quick start
- 📖 See [SETUP_GUIDE.md](SETUP_GUIDE.md) for installation

### Contact
- 📧 Email: support@vignan.ac.in
- 💬 Chat: In-app counselor messaging
- 📞 Phone: +91-XXX-XXX-XXXX

---

## 📝 Version History

### v2.0 (Current)
- ✨ Three-portal login system
- ✨ Power BI integration
- ✨ Tableau dashboard support
- ✨ Enhanced analytics
- ✨ Real-time alerts

### v1.0
- Basic single-login system
- Simple dashboards
- Counselor chat

---

## 📋 Deployment Checklist

- [ ] Install all dependencies: `pip install -r requirements.txt`
- [ ] Configure Power BI credentials (if using)
- [ ] Configure Tableau URLs (if using)
- [ ] Update `.env` with secrets
- [ ] Test all three login portals
- [ ] Verify all dashboards load
- [ ] Test alert system
- [ ] Check responsive design
- [ ] Load test with multiple users
- [ ] Deploy to production server

---

**Last Updated:** May 18, 2026
**Version:** 2.0
**Status:** Production Ready ✅
