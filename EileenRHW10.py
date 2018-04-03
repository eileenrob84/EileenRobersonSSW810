'''
    Homework assignment #10
    Eileen Roberson
    program to help students track grades, required courses, completed courses.
    It can also be a tool for faculty advisors to help students create a study
    plan.

    This is installment #2.  Added functionality to show the remaining required
    courses for each student.'''
    

import unittest
import os
from prettytable import PrettyTable

class Student:
    '''
        contains student ID number, student name, major and classes
        that have been completed.'''
    def __init__(self,CWID,name,major, class_ids=None):
        '''initialize the Student attributes'''
        self.cwid = CWID
        self.name = name
        self.major = major
        if class_ids == None:
            self.class_ids = []
        else:
            self.class_ids = class_ids

    def __str__(self):
        '''
            allows printing of the student attributes'''

        return str(self.cwid) + self.name + self.major + str(self.class_ids)


    def get_data(fn):
        '''get the data from the student file and put into the student 
            attributes
            '''
        file_name1 = fn
        students = []

        try:
            fp = open(file_name1, 'r')
        except FileNotFoundError:
            print("Can't open", file_name1)
        else:
            with fp:

                for line in fp:
                    cwid, name, major = line.split('\t')
                    student = Student(cwid,name,major)
                    students.append(student)
        return (students)

class Grades:
    def __init__(self,student_id, course, grade, inst_id):
        '''initialize the attribues related to grades'''

        self.student_id = student_id
        self.course = course
        self.grade = grade
        self.inst_id = inst_id

    def get_grades(fn):
        ''' get the data related to the grades from a file and put
            them into attributes'''

        file_name2=fn
        grades = []

        try:
            fp = open(file_name2, 'r')
        except FileNotFoundError:
            print("Can't open", file_name2)
        else:
            with fp:
                for line in fp:
                    student_id, course, grade, inst_id = line.split('\t')
                    grade = Grades(student_id, course, grade, inst_id)
                    grades.append(grade)

        return(grades)

class Repository:
    '''container for student data'''

    def student_grades(self, students, grades):
        '''collect student grades'''

        for g in grades:
            for s in students:
                if s.cwid == g.student_id:
                    s.class_ids.append(g.course)

    def instructor_courses(self, grades, instructors):
        '''collect instructor class data'''

        for g in grades:
            for i in instructors:
                if i.inst_id == g.inst_id:
                    i.courses.append(g.course)

    def course_students(self, grades):
        pass

class Course:
    def __init__(self,course_id, inst_id, students=None):
        '''initialize attributes related to the courses'''

        self.course_id = course_id
        self.inst_id = inst_id
        if students == None:
            self.students = []
        else:
            self.students = students   

    def get_courses(grades):
        ''' get course data and store in attributes'''
        
        courses = []
        for g in grades:
            found = False
            for c in courses:
                if c.course_id == g.course:
                    c.students.append(g.student_id)
                    found = True
            if found == False:
                course = Course(g.course, g.inst_id)
                course.students.append(g.student_id)
                courses.append(course)
        return courses


        

class Instructor:
    '''gets instructor data and stores in attributes'''

    def __init__(self,CWID,name,dept, courses=None):
        '''initial instructor attributes'''

        self.cwid = CWID
        self.name = name
        self.dept = dept
        
        if courses == None:
            self.courses = []
        else:
            self.courses = courses


    def get_instructors(fn):
        '''get instructor data from file and store in
            attributes'''

        file_name3=fn
        instructors = []

        try:
            fp = open(file_name3, 'r')
        except FileNotFoundError:
            print("Can't open", file_name3)
        else:
            with fp:
                for line in fp:
                    line = line.strip()
                    inst_id, name, dept = line.split('\t')
                    instructor = Instructor(inst_id, name, dept)
                    instructors.append(instructor)

        return(instructors)

    def get_instructor(inst_id, list_of_instructors):
        '''gets a list of instructors'''

        for l in list_of_instructors:
            if inst_id.strip() == l.cwid: 
                return l

class Majors:
    ''' get the list of required and elective courses from a file
        and prints them in a table'''
    def __init__(self,major, option, class_id):
        '''initialize the Student attributes'''
        self.major = major
        self.option = option
        self.class_id = class_id    

    def get_majors(fn):
        '''get the data from the student file and put into the student 
            attributes
            '''
        file_name1 = fn
        classes = []
        #pt1 = PrettyTable(field_names=['CWID', 'Name', 'Major'])

        try:
            fp = open(file_name1, 'r')
        except FileNotFoundError:
            print("Can't open", file_name1)
        else:
            with fp:

                for line in fp:
                    major, option, class_ids = line.split('\t')
                    class_list = Majors(major, option, class_ids)
                    classes.append(class_list)
        return (classes)
            
            
            


def main():
    student_data = Student.get_data("students.txt")
    #print(student_data)
    '''for s in student_data:
        print(str(s))'''

    student_pt = PrettyTable()
    student_pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])

    grades_data = Grades.get_grades("grades.txt")

    r = Repository()
    
    r.student_grades(student_data,grades_data)
    for s in student_data:
        s.class_ids.sort()
    for s in student_data:
        student_pt.add_row([s.cwid, s.name, s.class_ids])
    print(student_pt)


    instructor_pt = PrettyTable()
    instructor_pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])

    instructors = Instructor.get_instructors("instructors.txt")
    course = Course.get_courses(grades_data)
    for c in course:
        instructor = Instructor.get_instructor(c.inst_id, instructors)
        instructor_pt.add_row([instructor.cwid, instructor.name, instructor.dept, c.course_id, len(c.students)])        
    print(instructor_pt)

if __name__ == "__main__":
    main()


