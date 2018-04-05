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

    def __init__(self,CWID,name,major_id, class_ids=None):
        '''initialize the Student attributes'''
        self.cwid = CWID
        self.name = name
        self.major_id = major_id
        self.major = None
        if class_ids == None:
            self.class_ids = []
        else:
            self.class_ids = class_ids

        self.remaining_required = []
        self.remaining_electives = []



    def __str__(self):
        '''
            allows printing of the student attributes'''

        return str(self.cwid) + self.name + self.major_id + str(self.major_id)

    


class Grades:
    def __init__(self,student_id, course, grade, inst_id):
        '''initialize the attribues related to grades'''

        self.student_id = student_id
        self.course = course
        self.grade = grade
        self.inst_id = inst_id


class Repository:
    '''container for student data'''
    def __init__(self):
        self.students = []
        self.instructors = []
        self.majors = []
        self.grades = []
        self.courses = []
        path = "C:/Users/Mom's PC/Documents/SSW-810"
        print(path + "students.txt")       
        self.students =  self.read_student_file(path + "students.txt")

        self.instructors = self.read_instructor_file("instructors.txt")
        self.majors = self.read_majors_file("majors.txt")
        self.grades = self.read_grades_file("grades.txt")
        self.courses =  self.get_courses()
        self.populate_instructor_courses()
        self.populate_student_courses()
        self.populate_student_major()
        self.populate_student_remaining_courses()

    def read_student_file(self, filename):
        '''get the data from the student file and put into the student 
            attributes
            '''

        students = []

        try:
            fp = open(filename, 'r')
        except FileNotFoundError:
            print("Can't open", filename)
        else:
            with fp:

                for line in fp:
                    line = line.strip()
                    cwid, name, major_id = line.split('\t')
                    student = Student(cwid,name,major_id)
                    students.append(student)
        return (students)

    def read_instructor_file(self, filename):
        '''get instructor data from file and store in
            attributes'''

        instructors = []

        try:
            fp = open(filename, 'r')
        except FileNotFoundError:
            print("Can't open", filename)
        else:
            with fp:
                for line in fp:
                    line = line.strip()
                    inst_id, name, dept = line.split('\t')
                    instructor = Instructor(inst_id, name, dept)
                    instructors.append(instructor)

        return(instructors)

    def read_majors_file(self, filename):
        '''get the data from the student file and put into the student 
            attributes
            '''

        try:
            fp = open(filename, 'r')
        except FileNotFoundError:
            print("Can't open", filename)
        else:
            with fp:
                majors = []
                for line in fp:
                    line = line.strip()
                    major_id, option, course = line.split('\t')
                    major = None

                    for m in majors:
                        if m.major_id == major_id:
                            major = m
                            break

                    if major == None:
                        major = Majors(major_id)
                        majors.append(major)
                        
                
                    if option == 'R':
                        major.req_classes.append(course)
                    else:
                        major.elect_classes.append(course)

                return majors

    def read_grades_file(self, filename):

        grades = []

        try:
            fp = open(filename, 'r')
        except FileNotFoundError:
            print("Can't open", filename)
        else:
            with fp:
                for line in fp:
                    line = line.strip()
                    student_id, course, grade, inst_id = line.split('\t')
                    grade = Grades(student_id, course, grade, inst_id)
                    grades.append(grade)

        return(grades)


    def populate_student_courses(self, students=None, grades=None):
        '''collect student grades'''

        if students == None:
            students = self.students
        if grades == None:
            grades = self.grades

        for g in grades:
            for s in students:
                if s.cwid == g.student_id:
                    s.class_ids.append(g.course)

    def populate_instructor_courses(self, grades=None, instructors=None):
        '''collect instructor class data'''

        if grades == None:
            grades = self.grades
        if instructors == None:
            instructors = self.instructors

        for g in grades:
            for i in instructors:
                if i.inst_id == g.inst_id:
                    i.courses.append(g.course)
        return instructors

    def populate_student_major(self):
        for student in self.students:
            for major in self.majors:
                if student.major_id == major.major_id:
                    student.major = major

    def populate_student_remaining_courses(self):
        for student in self.students:
            major = student.major
            for course_id in major.req_classes:
                if course_id not in student.class_ids:
                    student.remaining_required.append(course_id)

                if course_id not in student.class_ids:
                    student.remaining_electives.append(course_id)

    
    def get_courses(self,grades=None):
        ''' get course data and store in attributes'''
        
        if grades == None:
            grades = self.grades

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

    
    def get_student_table(self, student_data=None):

        if student_data == None:
            student_data = self.students

        student_pt = PrettyTable()
        student_pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])

        for s in student_data:
            s.class_ids.sort()
        for s in student_data:
            student_pt.add_row([s.cwid, s.name, s.class_ids, s.remaining_required, s.remaining_required])
        return (student_pt)

    def get_instructor_table(self, instructor_data=None):

        if instructor_data == None:
            instructor_data = self.instructors

        instructor_pt = PrettyTable()
        instructor_pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', '# of Students'])

        for i in instructor_data:

            instructor_pt.add_row([i.cwid, i.name, i.dept, i.course, len(i.students)]) 
        return instructor_pt

    def get_majors_table(self, majors_data=None):
        
        if majors_data == None:
            majors_data = self.majors
        req_list = []
        elect_list = []

        majors_pt = PrettyTable()
        majors_pt = PrettyTable(field_names = ['Dept', 'Required', 'Elective'])

        for m in majors_data:
            if m.option  == "R":
                req_list.append(m.course)
            else:
                elect_list.append(m.course)
        for m in majors_data:
            majors_pt.add_row(m.major_id, m.req_classes.sort(), m.elect_classes.sort())

        return majors_pt


class Course:
    def __init__(self,course_id, inst_id, students=None):
        '''initialize attributes related to the courses'''

        self.course_id = course_id
        self.inst_id = inst_id
        if students == None:
            self.students = []
        else:
            self.students = students   
        

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

    def get_instructor(self, inst_id, list_of_instructors):
        '''gets a list of instructors'''

        for l in list_of_instructors:
            if inst_id.strip() == l.cwid: 
                return l


class Majors:
    ''' get the list of required and elective courses from a file
        and prints them in a table'''
    def __init__(self, major_id, req_classes=None, elect_classes=None):
        '''initialize the Student attributes'''
        self.major_id = major_id
        self.req_classes = req_classes
        self.elect_classes = elect_classes
        if self.req_classes == None:
            self.req_classes = []
        if self.elect_classes == None:
            self.elect_classes = []


def main():

    repository = Repository()
    print(repository.get_student_table())
    print(repository.get_instructor_table())
    print(repository.get_majors_table())


if __name__ == "__main__":
    main()


