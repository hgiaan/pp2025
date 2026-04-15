import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
import os
import pickle
import gzip
import threading
import time

from domains.student import Student
from domains.course import Course
from domains.mark import Mark

class MarkManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Mark Management System (PW9)")
        self.root.geometry("800x600")

        self.students = []
        self.courses = []
        self.marks = []

        self.create_widgets()

        self.load_data()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tab_students = ttk.Frame(self.notebook)
        self.tab_courses = ttk.Frame(self.notebook)
        self.tab_marks = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_students, text='Students')
        self.notebook.add(self.tab_courses, text='Courses')
        self.notebook.add(self.tab_marks, text='Marks')

        frame_s_input = ttk.LabelFrame(self.tab_students, text="Add Student")
        frame_s_input.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_s_input, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_s_id = ttk.Entry(frame_s_input)
        self.entry_s_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_s_input, text="Name:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_s_name = ttk.Entry(frame_s_input)
        self.entry_s_name.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_s_input, text="DoB:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_s_dob = ttk.Entry(frame_s_input)
        self.entry_s_dob.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(frame_s_input, text="Add", command=self.add_student).grid(row=0, column=6, padx=10)

        self.tree_students = ttk.Treeview(self.tab_students, columns=('ID', 'Name', 'DoB', 'GPA'), show='headings')
        self.tree_students.heading('ID', text='ID')
        self.tree_students.heading('Name', text='Name')
        self.tree_students.heading('DoB', text='DoB')
        self.tree_students.heading('GPA', text='GPA')
        self.tree_students.pack(expand=True, fill='both', padx=10, pady=5)

        frame_c_input = ttk.LabelFrame(self.tab_courses, text="Add Course")
        frame_c_input.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_c_input, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_c_id = ttk.Entry(frame_c_input)
        self.entry_c_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_c_input, text="Name:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_c_name = ttk.Entry(frame_c_input)
        self.entry_c_name.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_c_input, text="Credits:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_c_credits = ttk.Entry(frame_c_input)
        self.entry_c_credits.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(frame_c_input, text="Add", command=self.add_course).grid(row=0, column=6, padx=10)

        self.tree_courses = ttk.Treeview(self.tab_courses, columns=('ID', 'Name', 'Credits'), show='headings')
        self.tree_courses.heading('ID', text='ID')
        self.tree_courses.heading('Name', text='Name')
        self.tree_courses.heading('Credits', text='Credits')
        self.tree_courses.pack(expand=True, fill='both', padx=10, pady=5)

        # --- Marks Tab ---
        frame_m_input = ttk.LabelFrame(self.tab_marks, text="Input Marks")
        frame_m_input.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_m_input, text="Student:").grid(row=0, column=0, padx=5)
        self.combo_students = ttk.Combobox(frame_m_input, state="readonly")
        self.combo_students.grid(row=0, column=1, padx=5)

        ttk.Label(frame_m_input, text="Course:").grid(row=0, column=2, padx=5)
        self.combo_courses = ttk.Combobox(frame_m_input, state="readonly")
        self.combo_courses.grid(row=0, column=3, padx=5)

        ttk.Label(frame_m_input, text="Mark:").grid(row=0, column=4, padx=5)
        self.entry_mark = ttk.Entry(frame_m_input, width=10)
        self.entry_mark.grid(row=0, column=5, padx=5)

        ttk.Button(frame_m_input, text="Input", command=self.add_mark).grid(row=0, column=6, padx=10)

        self.tree_marks = ttk.Treeview(self.tab_marks, columns=('Course', 'Student', 'Mark'), show='headings')
        self.tree_marks.heading('Course', text='Course')
        self.tree_marks.heading('Student', text='Student')
        self.tree_marks.heading('Mark', text='Mark')
        self.tree_marks.pack(expand=True, fill='both', padx=10, pady=5)

        frame_controls = ttk.Frame(self.root)
        frame_controls.pack(fill='x', padx=10, pady=10)

        self.btn_gpa = ttk.Button(frame_controls, text="Calculate GPA (Sort Students)", command=self.calculate_gpa)
        self.btn_gpa.pack(side='left', padx=5)

        self.btn_save = ttk.Button(frame_controls, text="Save Data (Background)", command=self.save_data)
        self.btn_save.pack(side='right', padx=5)

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.lbl_status = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w')
        self.lbl_status.pack(side='bottom', fill='x')

    def refresh_tables(self):
        for row in self.tree_students.get_children():
            self.tree_students.delete(row)
        for s in self.students:
            self.tree_students.insert('', 'end', values=(s.id, s.name, s.dob, s.gpa))

        for row in self.tree_courses.get_children():
            self.tree_courses.delete(row)
        for c in self.courses:
            self.tree_courses.insert('', 'end', values=(c.id, c.name, c.credits))
        
        for row in self.tree_marks.get_children():
            self.tree_marks.delete(row)
        for m in self.marks:
            c_name = next((c.name for c in self.courses if c.id == m.cid), m.cid)
            s_name = next((s.name for s in self.students if s.id == m.sid), m.sid)
            self.tree_marks.insert('', 'end', values=(c_name, s_name, m.mark))

        self.combo_students['values'] = [f"{s.id} - {s.name}" for s in self.students]
        self.combo_courses['values'] = [f"{c.id} - {c.name}" for c in self.courses]

    def add_student(self):
        sid = self.entry_s_id.get()
        name = self.entry_s_name.get()
        dob = self.entry_s_dob.get()
        if sid and name:
            self.students.append(Student(name, sid, dob))
            self.refresh_tables()
            self.entry_s_id.delete(0, 'end')
            self.entry_s_name.delete(0, 'end')
            self.entry_s_dob.delete(0, 'end')
        else:
            messagebox.showerror("Error", "ID and Name are required!")

    def add_course(self):
        cid = self.entry_c_id.get()
        name = self.entry_c_name.get()
        try:
            credits = int(self.entry_c_credits.get())
            self.courses.append(Course(name, cid, credits))
            self.refresh_tables()
            self.entry_c_id.delete(0, 'end')
            self.entry_c_name.delete(0, 'end')
            self.entry_c_credits.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Credits must be an integer!")

    def add_mark(self):
        s_val = self.combo_students.get()
        c_val = self.combo_courses.get()
        m_val = self.entry_mark.get()

        if s_val and c_val and m_val:
            try:
                sid = s_val.split(" - ")[0]
                cid = c_val.split(" - ")[0]
                mark = float(m_val)
                final_mark = math.floor(mark * 10) / 10
                self.marks.append(Mark(sid, cid, final_mark))
                self.refresh_tables()
                self.entry_mark.delete(0, 'end')
            except ValueError:
                messagebox.showerror("Error", "Invalid Mark!")
        else:
            messagebox.showerror("Error", "Please select Student, Course and enter Mark!")

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
        self.refresh_tables()
        messagebox.showinfo("Success", "GPA Calculated and Students Sorted!")

    def load_data(self):
        if os.path.exists("students.dat"):
            try:
                with gzip.open("students.dat", "rb") as f:
                    data = pickle.load(f)
                    self.students = data.get('students', [])
                    self.courses = data.get('courses', [])
                    self.marks = data.get('marks', [])
                self.status_var.set("Data loaded successfully.")
                self.refresh_tables()
            except Exception as e:
                self.status_var.set(f"Error loading data: {e}")

    def save_data_thread(self, data_copy):
        try:
            time.sleep(1)
            with gzip.open("students.dat", "wb") as f:
                pickle.dump(data_copy, f)
            self.root.after(0, lambda: self.status_var.set("Data saved successfully (Background)."))
            self.root.after(0, lambda: messagebox.showinfo("Saved", "Data saved successfully!"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error saving data: {e}"))

    def save_data(self):
        self.status_var.set("Saving data in background...")
        data_to_save = {
            'students': self.students,
            'courses': self.courses,
            'marks': self.marks
        }
        thread = threading.Thread(target=self.save_data_thread, args=(data_to_save,))
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkManagementApp(root)
    root.mainloop()