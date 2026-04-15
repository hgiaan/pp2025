import math
import numpy as np
import os
import pickle
import gzip
import threading  
import time
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
        self.load_data()

    def load_data(self):
        if os.path.exists("students.dat"):
            try:
                print("Loading data from students.dat...")
                with gzip.open("students.dat", "rb") as f:
                    data = pickle.load(f)
                    self.students = data.get('students', [])
                    self.courses = data.get('courses', [])
                    self.marks = data.get('marks', [])
                print("Data loaded successfully.")
            except Exception as e:
                print(f"Error loading data: {e}")
                self.students = []
                self.courses = []
                self.marks = []
        else:
            print("No existing data found.")

    def save_data_thread(self, data_copy):
        """The actual saving logic to be run in a thread"""
        try:
            with gzip.open("students.dat", "wb") as f:
                pickle.dump(data_copy, f)
            print("\n[Background] Data saved successfully to students.dat")
        except Exception as e:
            print(f"\n[Background] Error saving data: {e}")

    def save_data(self):
        print("Starting background save...")
        data_to_save = {
            'students': self.students,
            'courses': self.courses,
            'marks': self.marks
        }
        
        thread = threading.Thread(target=self.save_data_thread, args=(data_to_save,))
        thread.start()

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
        print("6. Save Data (Background Thread)") 
        choice = input("Enter choice: ")
        
        if choice == '1': mm.load_students()
        elif choice == '2': mm.load_courses()
        elif choice == '3': mm.load_marks()
        elif choice == '4': mm.show_marks()
        elif choice == '5': mm.calculate_gpa()
        elif choice == '6': mm.save_data()
        elif choice == '7': 
            mm.save_data() 
            break
        else: print("Invalid choice!")