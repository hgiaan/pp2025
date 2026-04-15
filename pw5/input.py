import math
import os

def get_number_of_students():
    try:
        return int(input("Enter number of students: "))
    except ValueError:
        return 0

def input_student_data():
    print("--- Add New Student ---")
    name = input("Student name: ")
    sid = input("Student ID: ")
    dob = input("Student dob: ")
    
    with open("students.txt", "a") as f:
        f.write(f"{sid},{name},{dob}\n")
        
    return name, sid, dob

def get_number_of_courses():
    try:
        return int(input("Enter number of courses: "))
    except ValueError:
        return 0

def input_course_data():
    print("--- Add New Course ---")
    name = input("Course name: ")
    cid = input("Course ID: ")
    credits = 0
    while True:
        try:
            credits = int(input("Credits: "))
            break
        except ValueError:
            print("Credits must be an integer.")
            
    with open("courses.txt", "a") as f:
        f.write(f"{cid},{name},{credits}\n")
        
    return name, cid, credits

def input_mark_data(students, course_obj):
    print(f"Entering marks for course: {course_obj.name}")
    marks_list = []
    
    with open("marks.txt", "a") as f:
        for s in students:
            try:
                m_input = float(input(f"Mark for {s.name} (ID: {s.id}): "))
                final_mark = math.floor(m_input * 10) / 10
                
                mark_entry = {
                    'sid': s.id,
                    'cid': course_obj.id,
                    'mark': final_mark
                }
                marks_list.append(mark_entry)
                
                f.write(f"{s.id},{course_obj.id},{final_mark}\n")
                
            except ValueError:
                print("Invalid mark input.")
                
    return marks_list

def select_course(courses):
    cid = input("Choose a course (using ID): ")
    for c in courses:
        if c.id == cid:
            return c
    return None