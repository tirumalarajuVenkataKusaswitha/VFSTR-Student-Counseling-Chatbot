"""
Student Data Generator - R22 Regulation
Generates 100 students with realistic academic data
R22 Marks: T1=20, T2=5, T3=5, T4=20, 4 assessments of 20 marks each (2 modules per sem)
"""

import json
import random
import pandas as pd
from datetime import datetime, timedelta

# R22 Regulation Mark Structure
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

SUBJECTS = [
    "Data Structures",
    "Database Management",
    "Web Technologies",
    "Operating Systems",
    "Software Engineering",
    "Machine Learning"
]

DEPARTMENTS = ["CSE", "ECE", "ME", "EEE", "CIVIL"]
COURSES = ["B.Tech", "B.Tech Honors"]

def generate_student_data():
    """Generate 100 student records with marks"""
    students = []
    
    for i in range(1, 101):
        student_id = f"23{random.randint(10000, 99999)}"
        
        # Generate marks for all subjects
        subject_marks = {}
        for subject in SUBJECTS:
            marks = {
                "T1": random.randint(15, 20),
                "T2": random.randint(4, 5),
                "T3": random.randint(4, 5),
                "T4": random.randint(15, 20),
                "M1_A1": random.randint(16, 20),
                "M1_A2": random.randint(16, 20),
                "M2_A1": random.randint(16, 20),
                "M2_A2": random.randint(16, 20),
            }
            # Calculate total marks (out of 100)
            total = sum(marks.values())
            marks["Total"] = total
            marks["Percentage"] = round((total / 130) * 100, 2)
            marks["Grade"] = get_grade(marks["Percentage"])
            subject_marks[subject] = marks
        
        # Calculate CGPA
        all_percentages = [m["Percentage"] for m in subject_marks.values()]
        cgpa = round(sum(all_percentages) / len(all_percentages) * 0.1, 2)
        
        # Generate attendance (70-98%)
        attendance = random.randint(70, 98)
        
        student = {
            "student_id": student_id,
            "name": generate_name(i),
            "email": f"student{i}@vignan.ac.in",
            "phone": f"9{random.randint(100000000, 999999999)}",
            "department": random.choice(DEPARTMENTS),
            "course": random.choice(COURSES),
            "semester": random.randint(1, 8),
            "admission_year": 2023,
            "dob": (datetime.now() - timedelta(days=random.randint(6500, 8000))).strftime("%Y-%m-%d"),
            "parent_name": f"Parent_{generate_name(i)}",
            "parent_phone": f"9{random.randint(100000000, 999999999)}",
            "parent_email": f"parent{i}@email.com",
            "address": f"Address {i}, City",
            "marks": subject_marks,
            "attendance": attendance,
            "cgpa": cgpa,
            "warnings": random.randint(0, 2),
            "achievements": random.choice([[], ["Merit Certificate"], ["Scholarship"], ["Dean's List"]]),
            "needs_counseling": cgpa < 5.0 or attendance < 75,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        students.append(student)
    
    return students

def get_grade(percentage):
    """Get grade based on percentage"""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "F"

def generate_name(index):
    """Generate random names"""
    first_names = [
        "Arjun", "Ravi", "Priya", "Neha", "Karan", "Divya", "Amit", "Anjali",
        "Rohan", "Sonia", "Vikram", "Pooja", "Aditya", "Meera", "Nikhil", "Shreya"
    ]
    last_names = [
        "Sharma", "Kumar", "Singh", "Patel", "Gupta", "Verma", "Rao", "Reddy",
        "Nair", "Iyer", "Krishnan", "Bhat", "Desai", "Joshi", "Chopra", "Malik"
    ]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def save_data(students, filename="student_data.json"):
    """Save student data to JSON"""
    with open(filename, 'w') as f:
        json.dump(students, f, indent=2)
    print(f"✅ Generated {len(students)} students and saved to {filename}")
    
    # Also create CSV for easy viewing
    df = pd.json_normalize(students)
    df.to_csv("student_data.csv", index=False)
    print(f"✅ Also created student_data.csv")
    
    # Create summary
    print("\n📊 SUMMARY:")
    print(f"Total Students: {len(students)}")
    print(f"Departments: {', '.join(set([s['department'] for s in students]))}")
    print(f"Average CGPA: {round(sum([s['cgpa'] for s in students])/len(students), 2)}")
    print(f"Students needing counseling: {sum([s['needs_counseling'] for s in students])}")

if __name__ == "__main__":
    print("🚀 Generating Student Data (R22 Regulation)...")
    students = generate_student_data()
    save_data(students)
