import math
import numpy as np

class Student():
    def __init__(self):
        self.name = ""
        self.id = ""
        self.dob = ""
        self.gpa = 0.0

    def input(self):
        print("--- Add New Student ---")
        self.name = input("Student name: ")
        self.id = input("Student ID: ")
        self.dob = input("Student dob: ")

    def display(self):
        print(f"Student {self.id} | {self.name} | {self.dob} | GPA: {self.gpa}")

class Course():
    def __init__(self):
        self.name = ""
        self.id = ""
        self.credits = 0

    def input(self):
        print("--- Add New Course ---")
        self.name = input("Course name: ")
        self.id = input("Course ID: ")
        while True:
            try:
                self.credits = int(input("Credits: "))
                break
            except ValueError:
                print("Credits must be an integer.")

    def display(self):
        print(f"Course {self.id} | {self.name} | Credits: {self.credits}")

class Mark():
    def __init__(self):
        self.sid = ""
        self.cid = ""
        self.cname = ""
        self.sname = ""
        self.mark = 0.0

class MarkManagement():
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = []

    def inputStudents(self):
        try:
            n = int(input("Enter number of students: "))
            for i in range(n):
                s = Student()
                s.input()
                self.students.append(s)
        except ValueError:
            print("Invalid number.")

    def inputCourses(self):
        try:
            n = int(input("Enter number of courses: "))
            for i in range(n):
                c = Course()
                c.input()
                self.courses.append(c)
        except ValueError:
            print("Invalid number.")

    def inputMarks(self):
        if not self.courses or not self.students:
            print("Enter Students and Courses first!")
            return

        cid = input("Choose a course (using ID): ")
        
        course_obj = None
        for c in self.courses:
            if c.id == cid:
                course_obj = c
                break
        
        if not course_obj:
            print("Course not found!")
            return

        print(f"Entering marks for course: {course_obj.name}")
        for s in self.students:
            try:
                m_input = float(input(f"Mark for {s.name} (ID: {s.id}): "))
                mk = Mark()
                mk.sid = s.id
                mk.cid = cid
                mk.cname = course_obj.name
                mk.sname = s.name
                mk.mark = math.floor(m_input * 10) / 10
                self.marks.append(mk)
            except ValueError:
                print("Invalid mark input.")

    def displayMarks(self):
        print("\n--- Mark List ---")
        for mk in self.marks:
            print(f"Course {mk.cname} | Student {mk.sname} | Mark {mk.mark}")

    def sortStudents(self):
        for s in self.students:
            scores = []
            credits = []
            
            for mk in self.marks:
                if mk.sid == s.id:
                    scores.append(mk.mark)
                    for c in self.courses:
                        if c.id == mk.cid:
                            credits.append(c.credits)
                            break
            
            if len(scores) > 0:
                np_scores = np.array(scores)
                np_credits = np.array(credits)
                if np.sum(np_credits) > 0:
                    s.gpa = np.average(np_scores, weights=np_credits)
                    s.gpa = math.floor(s.gpa * 10) / 10
                else:
                    s.gpa = 0.0
            else:
                s.gpa = 0.0
        
        self.students.sort(key=lambda x: x.gpa, reverse=True)
        
        print("\n--- Students Sorted by GPA ---")
        for s in self.students:
            s.display()

if __name__ == "__main__":
    mm = MarkManagement()
    while True:
        print("\n___MENU___")
        print("1. Input Students")
        print("2. Input Courses")
        print("3. Input Marks")
        print("4. Display Marks")
        print("5. Display Students (Sorted by GPA)")
        print("6. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1': mm.inputStudents()
        elif choice == '2': mm.inputCourses()
        elif choice == '3': mm.inputMarks()
        elif choice == '4': mm.displayMarks()
        elif choice == '5': mm.sortStudents()
        elif choice == '6': break
        else: print("Invalid choice!")