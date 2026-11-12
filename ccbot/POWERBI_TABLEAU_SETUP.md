# 📊 Power BI & Tableau Integration Guide

## Overview

The enhanced Vignan AI Counselor platform supports integration with both Microsoft Power BI and Tableau for advanced analytics and dashboard capabilities.

---

## 🟦 Power BI Integration

### Prerequisites
- Microsoft Power BI account (Pro or Premium)
- Azure AD application registered
- Power BI Embedded capacity (optional but recommended)

### Step 1: Register Azure AD Application

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Fill in the details:
   - Name: `Vignan AI Counselor`
   - Supported account types: `Accounts in this organizational directory only`
   - Redirect URI: `http://localhost:8501` (for development)
5. Click **Register**

### Step 2: Get Application Credentials

1. In the app registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Add description: `Streamlit Power BI`
4. Copy the **Client Secret Value** (save this securely)
5. Note the **Client ID** and **Tenant ID** from Overview tab

### Step 3: Grant Power BI API Permissions

1. Go to **API permissions**
2. Click **Add a permission**
3. Select **Power BI Service**
4. Select **Delegated permissions**
5. Check these permissions:
   - `Report.Read.All`
   - `Dashboard.Read.All`
   - `Capacity.Read.All`
6. Click **Grant admin consent**

### Step 4: Create Power BI Report

1. Open [Power BI Service](https://powerbi.microsoft.com)
2. Create a new report or dashboard
3. Add your student data
4. Publish to your workspace
5. Note the **Report ID** (from URL: `/reports/{report-id}`)

### Step 5: Configure Streamlit Secrets

Create `.streamlit/secrets.toml`:

```toml
# Power BI Configuration
[powerbi]
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
tenant_id = "YOUR_TENANT_ID"
report_id = "YOUR_REPORT_ID"
workspace_id = "YOUR_WORKSPACE_ID"
```

### Step 6: Implement in Code

**dashboard_utils.py** already includes the function:

```python
def embed_powerbi_dashboard(report_id, access_token, height=800):
    """Embed a Power BI report"""
    html_string = f"""
    <iframe 
        width="100%" 
        height="{height}" 
        src="https://app.powerbi.com/reportEmbed?reportId={report_id}&autoAuth=true" 
        frameborder="0" 
        allowFullScreen="true">
    </iframe>
    """
    st.components.v1.html(html_string, height=height)
```

### Step 7: Use in Parent Dashboard

In `pages/parent_dashboard.py`:

```python
import streamlit as st
from dashboard_utils import embed_powerbi_dashboard

# Check if user has Power BI enabled
if st.checkbox("📊 Show Power BI Performance Dashboard"):
    try:
        report_id = st.secrets.get("powerbi", {}).get("report_id")
        if report_id:
            embed_powerbi_dashboard(report_id, st.secrets.get("powerbi_token"))
        else:
            st.warning("Power BI report not configured")
    except Exception as e:
        st.error(f"Failed to load Power BI dashboard: {e}")
```

### Power BI Report Template

**Recommended visualizations for Parent Dashboard:**

1. **Key Performance Indicators (KPIs)**
   - Current CGPA
   - Attendance Rate
   - Average Score
   - Warnings Count

2. **Charts & Graphs**
   - CGPA Trend (Line Chart)
   - Attendance Distribution (Pie Chart)
   - Subject Performance (Bar Chart)
   - Performance vs Class Average (Column Chart)

3. **Tables**
   - Subject-wise Details
   - Attendance Dates
   - Grades History
   - Counselor Notes

---

## 📊 Tableau Integration

### Prerequisites
- Tableau Server or Tableau Online account
- Admin access to manage embedded dashboards
- Trusted Ticket authentication enabled

### Step 1: Create Tableau Dashboard

1. Open **Tableau Desktop** or **Tableau Server**
2. Connect to your data source (CSV, Excel, Database)
3. Create visualizations:
   - Dashboard Title: "Student Performance Analytics"
   - Add filters for student selection
   - Create performance trend views
   - Add statistical summaries

### Step 2: Configure Tableau Server

**Settings → Embedded Content:**

1. Enable **Trusted Authentication** (if using)
2. Enable **User Impersonation** (if required)
3. Note the **Server URL**: `https://your-tableau-server.com`
4. Note the **Site Name** (if applicable)

### Step 3: Generate Public Dashboard URL

**Option 1: Public Sharing**
1. Publish dashboard to Tableau Server
2. Click **Share**
3. Copy the URL: `https://your-tableau-server.com/views/DashboardName`

**Option 2: Embedded Code**
1. Click **Share**
2. Select **Embed Code**
3. Copy the provided iframe code

### Step 4: Configure Streamlit Secrets

Update `.streamlit/secrets.toml`:

```toml
# Tableau Configuration
[tableau]
server_url = "https://your-tableau-server.com"
site_name = "your_site"
view_url = "your_view_url"
dashboard_names = [
    "Student Performance Dashboard",
    "Attendance Analytics",
    "Subject Performance"
]
```

### Step 5: Implement in Code

**Already available in dashboard_utils.py:**

```python
def embed_tableau_dashboard(dashboard_url, height=800):
    """Embed a Tableau dashboard"""
    st.components.v1.iframe(
        src=dashboard_url,
        height=height,
        scrolling=True
    )
```

### Step 6: Use in Dashboards

In `pages/parent_dashboard.py`:

```python
from dashboard_utils import embed_tableau_dashboard

if st.checkbox("📈 Show Tableau Analytics Dashboard"):
    try:
        tableau_url = st.secrets.get("tableau", {}).get("view_url")
        if tableau_url:
            embed_tableau_dashboard(tableau_url)
        else:
            st.warning("Tableau dashboard not configured")
    except Exception as e:
        st.error(f"Failed to load Tableau dashboard: {e}")
```

### Tableau Dashboard Template

**Recommended layout:**

**Dashboard: Student Performance Analytics**

- **Container 1:** Key Metrics (Top)
  - CGPA KPI
  - Attendance KPI
  - Average Score KPI
  - Academic Status KPI

- **Container 2:** Performance Trends (Middle Left)
  - CGPA Trend Line Chart (12 months)
  - Attendance Trend Line Chart

- **Container 3:** Subject Analysis (Middle Right)
  - Subject Performance Bar Chart
  - Grade Distribution

- **Container 4:** Comparisons (Bottom)
  - Radar Chart: Student vs Class Average
  - Peer Comparison

- **Filters:**
  - Student Name/ID selector
  - Month Range selector
  - Department selector

---

## 🔗 Choosing Between Power BI and Tableau

### Use Power BI if:
- ✅ You're already using Microsoft Office 365
- ✅ You need tight Azure AD integration
- ✅ You want cost-effective embedded reporting
- ✅ You prefer Excel-like data modeling
- ✅ Your data is in SQL Server or Azure

### Use Tableau if:
- ✅ You need superior data visualization
- ✅ You want advanced interactive dashboards
- ✅ Your data sources are diverse
- ✅ You need public sharing without authentication
- ✅ You prefer drag-and-drop interface

---

## 📈 Sample Data Structure

### For Power BI/Tableau

**Student Performance Table:**
```
StudentID | StudentName | CGPA | Attendance | AverageScore | Semester | Department
2310001   | Arjun S.    | 7.5  | 85         | 78.5         | 5        | CSE
2310002   | Priya S.    | 8.2  | 90         | 85.3         | 5        | CSE
```

**Subject Performance Table:**
```
StudentID | Subject       | Marks | Percentage | Grade | Semester
2310001   | Mathematics   | 38    | 76         | B+    | 5
2310001   | Physics       | 40    | 80         | A-    | 5
```

**Attendance Table:**
```
StudentID | Date       | Status  | MonthYear
2310001   | 2024-01-15 | Present | Jan-2024
2310001   | 2024-01-16 | Absent  | Jan-2024
```

---

## 🔐 Security Best Practices

### Power BI
```
1. Always use Azure AD authentication
2. Implement row-level security (RLS)
3. Use service principal accounts
4. Rotate client secrets regularly
5. Monitor access logs
6. Use conditional access policies
```

### Tableau
```
1. Enable SSL/TLS encryption
2. Use Trusted Tickets securely
3. Implement user authentication
4. Set up content ownership rules
5. Monitor audit logs
6. Restrict public dashboard access
```

---

## 🔧 Troubleshooting

### Power BI Not Loading

**Problem:** Iframe returns 400 error
```
Solution: 
1. Verify Report ID is correct
2. Check Azure AD permissions
3. Ensure access token is valid
4. Clear browser cache
```

**Problem:** Authentication failed
```
Solution:
1. Verify credentials in secrets.toml
2. Check client secret hasn't expired
3. Confirm Azure AD app has Power BI API access
4. Verify tenant ID matches
```

### Tableau Not Loading

**Problem:** Dashboard appears blank
```
Solution:
1. Verify dashboard URL is correct
2. Check Trusted Ticket configuration
3. Ensure server URL is accessible
4. Verify user has view permissions
```

**Problem:** Slow performance
```
Solution:
1. Optimize data source queries
2. Add dashboard filters
3. Use data extracts instead of live connections
4. Reduce number of visualizations
```

---

## 📱 Responsive Design

### Mobile Optimization

For Power BI:
```python
if st.session_state.screen_size == "mobile":
    height = 600
else:
    height = 800
```

For Tableau:
```python
st.components.v1.iframe(
    src=dashboard_url,
    height=600 if mobile else 800,
    scrolling=True
)
```

---

## 📊 Advanced Features

### Dynamic Report Generation

**Create parameterized reports:**

```python
from dashboard_utils import embed_powerbi_dashboard

# Get student ID from session
student_id = st.session_state.user.get("student_id")

# Add filter to report URL
report_url = f"{base_url}&filter=Student/ID eq '{student_id}'"

embed_powerbi_dashboard(report_id, access_token)
```

### Scheduled Reports

**Send weekly performance reports to parents:**

```python
import schedule
import time

def send_weekly_report(parent_email, student_id):
    # Generate Power BI report
    # Export as PDF
    # Send via email
    pass

schedule.every().monday.at("09:00").do(
    send_weekly_report, 
    "parent@email.com", 
    "2310001"
)
```

---

## 📚 Resources

- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [Tableau Documentation](https://help.tableau.com/)
- [Azure AD Documentation](https://docs.microsoft.com/en-us/azure/active-directory/)
- [Streamlit Components](https://docs.streamlit.io/library/components)

---

## 📝 Configuration Checklist

- [ ] Register Azure AD application (for Power BI)
- [ ] Get client credentials
- [ ] Grant API permissions
- [ ] Create Power BI report/dashboard
- [ ] Configure `.streamlit/secrets.toml`
- [ ] Test Power BI embedding
- [ ] Create Tableau dashboard (if using)
- [ ] Enable Tableau Server authentication
- [ ] Test Tableau embedding
- [ ] Verify responsive design
- [ ] Test with sample data
- [ ] Document dashboard URLs
- [ ] Set up monitoring/alerting
- [ ] Deploy to production

---

**Last Updated:** May 18, 2026
**Version:** 2.0
**Status:** Production Ready ✅
