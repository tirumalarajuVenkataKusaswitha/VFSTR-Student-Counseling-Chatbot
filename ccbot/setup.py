"""
Setup Script - Initialize Application
Run this script once to generate student data and initialize the database
"""

import os
import sys
import json
from datetime import datetime

def setup_application():
    """Setup the application"""
    
    print("\n" + "="*60)
    print("🎓 VIGNAN AI COUNSELOR BOT - SETUP")
    print("="*60 + "\n")
    
    # Step 1: Check if student data exists
    print("📋 Step 1: Checking/Generating Student Data...")
    if not os.path.exists("student_data.json"):
        try:
            from generate_student_data import generate_student_data, save_data
            print("   ⏳ Generating 100 student records...")
            students = generate_student_data()
            save_data(students)
            print("   ✅ Student data generated successfully!")
        except Exception as e:
            print(f"   ❌ Error generating student data: {e}")
            return False
    else:
        print("   ✅ Student data already exists!")
    
    # Step 2: Initialize Database
    print("\n📦 Step 2: Initializing Database...")
    try:
        from database import db
        print("   ✅ Database initialized with default users!")
        
        # Display credentials
        print("\n   📋 Demo Credentials Created:")
        print("   " + "-"*50)
        print("   👤 STUDENT LOGIN")
        print("      - Username: student_001")
        print("      - Password: student123")
        print("   " + "-"*50)
        print("   👨‍👩‍👧 PARENT LOGIN")
        print("      - Username: parent_001")
        print("      - Password: parent123")
        print("   " + "-"*50)
        print("   🎯 COUNSELOR LOGIN")
        print("      - Username: counselor_001")
        print("      - Password: counselor123")
        print("   " + "-"*50)
    except Exception as e:
        print(f"   ❌ Error initializing database: {e}")
        return False
    
    # Step 3: Check for required environment variables
    print("\n🔧 Step 3: Checking Configuration...")
    if not os.getenv("GROQ_API_KEY"):
        print("   ⚠️  WARNING: GROQ_API_KEY not set!")
        print("   Please set your GROQ API key:")
        print("   ")
        print("   Windows (PowerShell):")
        print("      $env:GROQ_API_KEY = 'your-api-key'")
        print("   ")
        print("   Or create a .env file with:")
        print("      GROQ_API_KEY=your-api-key")
    else:
        print("   ✅ GROQ_API_KEY is configured!")
    
    # Step 4: Verify student data
    print("\n✔️ Step 4: Verifying Data...")
    try:
        with open("student_data.json", "r") as f:
            data = json.load(f)
            print(f"   ✅ {len(data)} student records loaded successfully!")
            
            # Show sample statistics
            cgpas = [s.get("cgpa", 0) for s in data]
            print(f"   📊 Average CGPA: {sum(cgpas)/len(cgpas):.2f}")
            
            attendances = [s.get("attendance", 0) for s in data]
            print(f"   📊 Average Attendance: {sum(attendances)/len(attendances):.1f}%")
            
            priority = len([s for s in data if s.get("needs_counseling")])
            print(f"   ⚠️  Students needing counseling: {priority}")
    except Exception as e:
        print(f"   ❌ Error verifying data: {e}")
        return False
    
    # Final message
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("\n🚀 To start the application, run:")
    print("   streamlit run app.py")
    print("\n" + "="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = setup_application()
    sys.exit(0 if success else 1)
