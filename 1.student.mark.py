def student():
    n=int(input("Number of students: "))
    sid={}
    sname={}
    sdob={}
    for i in range (n):
        print("Student #",i+1)
        sid[i] = input("ID: ")
        sname[i] = input("Name: ")
        sdob[i] = input("DoB: ")
    return n, sid, sname

def course():
    cid={}
    cname={}
    m=int(input("Number of courses: "))
    for i in range (m):
        print("Course #",i+1)
        cid[i] = input("Id:  ")
        cname[i] = input("Name: ")
    return m, cid, cname

def mark(n, sname, m, cid, cname):
    marks = {}
    se_course=input("Choose course: ")
    found = -1
    for i in range(m):
        if cid[i] == se_course:
            found = i
            break
    if found != -1:
        print("Course",cname[found])
        for i in range (n):
            score = float(input("Mark for " + sname[i]+':'))
            marks[se_course, sname[i]] = score
    else:
        print("Course not found")
    return marks

num_students, students_ids, student_names = student()
num_courses, course_ids, course_names = course()
mark_fin = mark(num_students, student_names, num_courses, course_ids, course_names)

print(mark_fin)