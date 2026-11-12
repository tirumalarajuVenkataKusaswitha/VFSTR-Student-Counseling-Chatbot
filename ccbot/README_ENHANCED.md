# 🎓 Vignan AI Counselor - Three-Portal Enhanced Version

**Version 2.0** | **Status:** ✅ Production Ready | **Last Updated:** May 18, 2026

---

## 🚀 What's New?

### ✨ Three Separate Login Portals

Users now have dedicated portals:

1. **👤 Student Portal** - Manage your academic journey
2. **👨‍👩‍👧 Parent Portal** - Monitor your child's progress  
3. **🎯 Counselor Portal** - Advanced student management

### 📊 Power BI & Tableau Integration

Professional business intelligence dashboards for:
- Real-time analytics
- Performance trend analysis
- Statistical reports
- Custom visualizations

### 📈 Enhanced Analytics

- **Interactive Plotly Charts** - Beautiful visualizations
- **Performance Dashboards** - Comprehensive analytics
- **Real-time Alerts** - Immediate notifications
- **AI Recommendations** - Smart suggestions

---

## 🎯 Quick Start (2 minutes)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the App
```bash
streamlit run app_enhanced.py
```

### 3️⃣ Login with Demo Credentials

**Student:**
```
Username: student_001
Password: student123
```

**Parent:**
```
Username: parent_001
Password: parent123
```

**Counselor:**
```
Username: counselor_001
Password: counselor123
```

---

## 📊 Dashboard Features

### For Students 👤
- 📊 Personal performance dashboard
- 📈 CGPA and attendance tracking
- 🤖 AI counselor chatbot
- 📚 Study resources and materials
- 🎯 Personalized recommendations

### For Parents 👨‍👩‍👧
- 📊 **Interactive Analytics Dashboard**
  - CGPA trends (12-month visualization)
  - Attendance distribution charts
  - Subject-wise performance analysis
  - Performance comparison with class average
  
- 🔔 **Real-time Alerts**
  - Low CGPA warnings
  - Attendance drop alerts
  - Academic warnings
  - Success achievements

- 💡 **Recommendations**
  - Academic improvement plans
  - Focus areas
  - Success strategies

- 📈 **Performance Tabs**
  - Analytics Dashboard
  - Performance Trends
  - Alert System
  - Recommendations

### For Counselors 🎯
- 👥 Student caseload management
- 📊 Advanced analytics dashboard
- 📈 Performance distribution analysis
- 📝 Session note management
- 🎓 Student categorization and tracking

---

## 📁 File Structure

```
ccbot/
├── app_enhanced.py                    # 🆕 Main three-portal app
├── dashboard_utils.py                 # 🆕 Power BI/Tableau utilities
├── login_system.py                    # 🆕 Session management
├── app.py                             # Original app
├── database.py                        # Authentication & data
├── requirements.txt                   # 📝 Updated dependencies
├── pages/
│   ├── student_dashboard.py
│   ├── parent_dashboard.py            # 📝 Enhanced
│   ├── counselor_dashboard.py
│   ├── student_counselor_chat.py
│   ├── student_resources.py
│   ├── parent_messages.py
│   ├── parent_alerts.py
│   ├── counselor_students.py
│   └── counselor_notes.py
├── THREE_PORTAL_SETUP.md              # 🆕 Complete setup guide
├── POWERBI_TABLEAU_SETUP.md           # 🆕 BI integration guide
├── MIGRATION_GUIDE.md                 # 🆕 Migration instructions
└── ...
```

---

## 🔌 Integration Capabilities

### Power BI
✅ Azure AD Authentication
✅ Report Embedding
✅ Dashboard Sharing
✅ Interactive Visualizations
✅ Row-Level Security (RLS)

### Tableau
✅ Dashboard Embedding
✅ Public Sharing
✅ Interactive Filters
✅ Real-time Data
✅ Trusted Authentication

See [POWERBI_TABLEAU_SETUP.md](POWERBI_TABLEAU_SETUP.md) for detailed configuration.

---

## 🎨 Enhanced UI/UX

### Login Page
- Three distinct portals
- Color-coded by role
- Clear credential display
- Professional design
- Responsive layout

### Dashboards
- Tabbed interface
- Interactive charts
- Real-time metrics
- Alert indicators
- Recommendation cards

### Navigation
- Role-based sidebar
- Quick access menus
- Session info display
- Secure logout
- User preferences

---

## 🔐 Security Features

✅ **Authentication**
- Secure password hashing
- Session management
- Session timeout (1 hour)
- Activity tracking

✅ **Authorization**
- Role-based access control
- Resource-level permissions
- Data isolation
- Audit logging

✅ **Data Protection**
- Encrypted storage
- Secure API endpoints
- HTTPS support
- Credential masking

---

## 📊 Sample Data

Default demo accounts with sample student data:

**Students:**
- Arjun Sharma (2310001) - CGPA: 7.5, Attendance: 85%
- Priya Singh (2310002) - CGPA: 8.2, Attendance: 90%
- Karan Patel (2310003) - CGPA: 6.3, Attendance: 78%

**Parents:**
- Rajesh Sharma (parent of student 2310001)
- Sunita Singh (parent of student 2310002)

**Counselors:**
- Dr. Ananya Verma - Academic Guidance
- Prof. Rajesh Kumar - Mental Health
- Ms. Shreya Nair - Career & Placement

---

## 📈 New Visualizations

### Parent Dashboard Charts
1. **CGPA Trend Line** - 12-month performance history
2. **Attendance Pie Chart** - Present vs Absent distribution
3. **Subject Performance Bar** - Marks by subject
4. **Radar Chart** - Student vs class average comparison
5. **Counseling Sessions** - Sessions by type

### Analytics Metrics
- Performance health status
- Risk indicators
- Achievement levels
- Trend directions

---

## ⚙️ Configuration

### Required Setup
1. ✅ Dependencies installed
2. ✅ Database configured (auto-created)
3. ✅ Credentials ready (demo included)

### Optional Setup (for BI features)
1. Power BI account and credentials
2. Tableau Server/Online URL
3. `.streamlit/secrets.toml` configuration

See [POWERBI_TABLEAU_SETUP.md](POWERBI_TABLEAU_SETUP.md) for details.

---

## 🚀 Deployment

### Development
```bash
streamlit run app_enhanced.py
```

### Production
```bash
# Install system dependencies
# Configure environment
# Set up SSL certificates
# Configure reverse proxy
# Deploy with PM2 or supervisor

pm2 start "streamlit run app_enhanced.py" --name vignan-counselor
```

### Docker (Optional)
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app_enhanced.py"]
```

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [THREE_PORTAL_SETUP.md](THREE_PORTAL_SETUP.md) | Complete feature & setup guide |
| [POWERBI_TABLEAU_SETUP.md](POWERBI_TABLEAU_SETUP.md) | BI integration instructions |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | Migration from v1 to v2 |
| [README.md](README.md) | Project overview |
| [START_HERE.md](START_HERE.md) | Getting started guide |

---

## 🐛 Troubleshooting

### Common Issues

**Login failing:**
```
→ Check credentials are correct
→ Verify database file exists (app_database.json)
→ Clear browser cache and cookies
```

**Dashboards not loading:**
```
→ Verify Plotly is installed: pip install plotly
→ Check data is available in database
→ Try refreshing the page
```

**Charts rendering slowly:**
```
→ Use st.cache_data decorator
→ Reduce data size in visualizations
→ Clear Streamlit cache: rm -rf ~/.streamlit
```

See [THREE_PORTAL_SETUP.md](THREE_PORTAL_SETUP.md#troubleshooting) for more solutions.

---

## 📞 Support

- 📧 **Email:** support@vignan.ac.in
- 💬 **In-App:** Counselor messaging
- 📖 **Docs:** See documentation files
- 🐛 **Issues:** Check troubleshooting guide

---

## 📊 System Requirements

- **Python:** 3.8 or higher
- **Streamlit:** 1.28.0+
- **Memory:** 2GB minimum
- **Storage:** 500MB for dependencies
- **Browser:** Modern (Chrome, Firefox, Safari, Edge)

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ✅ Pre-deployment Checklist

- [ ] All dependencies installed
- [ ] Database created and populated
- [ ] Three portals tested
- [ ] Demo credentials work
- [ ] Dashboards display correctly
- [ ] Charts render properly
- [ ] Alerts system functional
- [ ] Mobile responsive design works
- [ ] Logout/session management works
- [ ] Documentation reviewed
- [ ] Performance tested
- [ ] Security review completed

---

## 🎯 Next Steps

### For Users
1. Create your user account
2. Explore your dashboard
3. Try AI counselor chat
4. Review recommendations
5. Set preferences

### For Administrators
1. Configure Power BI (optional)
2. Set up Tableau (optional)
3. Train staff on new features
4. Monitor system performance
5. Collect user feedback

### For Developers
1. Review code structure
2. Understand data flow
3. Set up development environment
4. Create custom features
5. Deploy to production

---

## 📈 Version History

### v2.0 (Current) - May 18, 2026 ✅
- ✨ Three separate login portals
- ✨ Power BI integration
- ✨ Tableau support
- ✨ Enhanced analytics dashboards
- ✨ Real-time alerts system
- ✨ Improved session management
- ✨ Role-based access control

### v1.0 - March 11, 2026
- Basic single login system
- Simple dashboards
- Counselor chat integration
- Student data management

---

## 📜 License & Attribution

This enhanced version builds upon the original Vignan AI Counselor Bot with significant improvements in:
- User experience
- Analytics capabilities
- Security
- Scalability
- Professional BI integration

---

## 🎉 Thank You!

Thank you for using Vignan AI Counselor. We're committed to supporting student success through technology and innovation.

**Questions?** Contact: support@vignan.ac.in

---

**Status:** ✅ Production Ready
**Version:** 2.0
**Last Updated:** May 18, 2026
