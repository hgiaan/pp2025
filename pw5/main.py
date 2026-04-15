import math
import numpy as np
import os
import zipfile
import input as ui_in
import output as ui_out
from domains.student import Student
from domains.course import Course
from domains.mark import Mark

class MarkManagement:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = []
        self.check_and_load_data()

    def check_and_load_data(self):
        if os.path.exists("students.dat"):
            print("Loading data from students.dat...")
            with zipfile.ZipFile("students.dat", "r") as zip_ref:
                zip_ref.extractall()
        
        if os.path.exists("students.txt"):
            with open("students.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        self.students.append(Student(parts[1], parts[0], parts[2]))

        if os.path.exists("courses.txt"):
            with open("courses.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        self.courses.append(Course(parts[1], parts[0], int(parts[2])))

        if os.path.exists("marks.txt"):
             with open("marks.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        self.marks.append(Mark(parts[0], parts[1], float(parts[2])))

    def save_and_compress(self):
        print("Compressing data into students.dat...")
        files_to_compress = []
        
        if os.path.exists("students.txt"): files_to_compress.append("students.txt")
        if os.path.exists("courses.txt"): files_to_compress.append("courses.txt")
        if os.path.exists("marks.txt"): files_to_compress.append("marks.txt")
        
        if files_to_compress:
            with zipfile.ZipFile("students.dat", "w") as zipf:
                for file in files_to_compress:
                    zipf.write(file)
            print("Data saved successfully.")
        else:
            print("No data files to save.")

    def load_students(self):
        n = ui_in.get_number_of_students()
        for _ in range(n):
            name, sid, dob = ui_in.input_student_data()
            self.students.append(Student(name, sid, dob))

    def load_courses(self):
        n = ui_in.get_number_of_courses()
        for _ in range(n):
            name, cid, credits = ui_in.input_course_data()
            self.courses.append(Course(name, cid, credits))

    def load_marks(self):
        if not self.courses or not self.students:
            print("Enter Students and Courses first!")
            return
        
        selected_course = ui_in.select_course(self.courses)
        if not selected_course:
            print("Course not found!")
            return

        raw_marks = ui_in.input_mark_data(self.students, selected_course)
        for rm in raw_marks:
            self.marks.append(Mark(rm['sid'], rm['cid'], rm['mark']))

    def show_marks(self):
        ui_out.display_marks(self.marks, self.students, self.courses)

    def calculate_gpa(self):
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
        ui_out.display_students(self.students)

if __name__ == "__main__":
    mm = MarkManagement()
    while True:
        print("\n=== MENU ===")
        print("1. Input Students")
        print("2. Input Courses")
        print("3. Input Marks")
        print("4. Display Marks")
        print("5. Display Students (Sorted by GPA)")
        print("6. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1': mm.load_students()
        elif choice == '2': mm.load_courses()
        elif choice == '3': mm.load_marks()
        elif choice == '4': mm.show_marks()
        elif choice == '5': mm.calculate_gpa()
        elif choice == '6': 
            mm.save_and_compress() 
            break
        else: print("Invalid choice!")