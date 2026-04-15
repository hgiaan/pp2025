# make input functions
    # student
    # course
    # marks
# make display functions
class Student():
    def __init__(self):
        self.name = "" 
        self.id = ""
        self.dob = ""
    def input(self):
        self.name = input("Student name: ")
        self.id = input("Student ID: ")
        self.dob = input("Student dob: ")
    def display(self):
        print(f"Student {self.id}| {self.name}| {self.dob}")

class Course():
    def __init__(self):
        self.name = "" 
        self.id = ""
    def input(self):
        self.name = input("Course name: ")
        self.id = input("Course ID: ")
    def display(self):
        print(f"Course {self.id}| {self.name}")

class Mark():
    def __init__(self):
        self.sid = ""
        self.cid = ""
        self.cname = ""
        self.mark = 0

    def input(self):
        self.sid = input("Student id: ")
        self.cid = input("Course id: ")
        self.mark = input("Mark: ")
        
class MarkManagement():
    def __init__(self):
        self.students=[]
        self.courses=[]
        self.marks=[]

    def inputStudents(self):
        n=int(input("Enter number of students: "))
        for i in range(n):
            s= Student()
            s.input()
            self.students.append(s)
    
    def inputCourses(self):
        n=int(input("Enter number of courses: "))
        for i in range(n):
            c= Course()
            c.input()
            self.courses.append(c)

    def displayStudents(self):
        for s in self.students:
            s.display()
    
    def displayCourses(self):
        for c in self.courses:
            c.display()

    def inputMarks(self):
        cid = input("Choose a course (using ID): ")

        course_found = False
        for c in self.courses:
            if c.id == cid:
                course_found = True
                course_name = c.name  
                break

        if not course_found:
            print("Course not found")
            return

        for s in self.students:
            print(f"Student {s.name}")
            mk = Mark()
            mk.sid = s.id
            mk.cid = cid
            mk.cname = course_name
            mk.sname = s.name
            mk.mark = float(input("Mark: "))
            self.marks.append(mk)

    def displayMarks(self):
        for mk in self.marks:
            print(f"Course {mk.cname} | Student {mk.sname} | ID {mk.sid} | Mark {mk.mark}")

mm = MarkManagement()
mm.inputStudents()
mm.inputCourses()
mm.inputMarks()

# mm.displayStudents()
# mm.displayCourses()
mm.displayMarks()   