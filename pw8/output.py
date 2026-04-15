def display_students(students):
    print("\n--- Student List ---")
    for s in students:
        print(f"Student {s.id} | {s.name} | {s.dob} | GPA: {s.gpa}")

def display_courses(courses):
    print("\n--- Course List ---")
    for c in courses:
        print(f"Course {c.id} | {c.name} | Credits: {c.credits}")

def display_marks(marks, students, courses):
    print("\n--- Mark List ---")
    for mk in marks:
        c_name = next((c.name for c in courses if c.id == mk.cid), "Unknown")
        s_name = next((s.name for s in students if s.id == mk.sid), "Unknown")
        print(f"Course {c_name} | Student {s_name} | Mark {mk.mark}")