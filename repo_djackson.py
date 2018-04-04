import os
from collections import defaultdict
from prettytable import PrettyTable

"""
:author: Daniel Jackson
1Apr18
SSW-810-A
Assignment HW10

Module contains classes to construct and operate on a repository (Repo) of 
education institution data including Students, Professors, Majors, and Courses. 

:updates: corrections from feedback on HW09; added Majors functionality
and tests
"""


class Student:
    """Class models a student with ID, name, major, and a container of courses.
    Expected field usage:
    cwid = str
    name = str
    courses = dict of courses completed "successfully"
    major = str
    """
    def __init__(self, cwid, name, courses, major):
        self.cwid = cwid
        self.name = name
        self.courses = courses
        self.major = major


class Professor:
    """Class models a professor with ID, name, dept, and a container of courses
    Expected field usage:
    cwid = str
    name = str
    courses = dict of courses taught
    major = str
    """
    def __init__(self, cwid, name, courses, dept):
        self.cwid = cwid
        self.name = name
        self.courses = courses
        self.dept = dept


class Course:
    """Class models a course with course name, department, professor, and a
    container of students.
    Expected field usage:
    name = str
    students = list of student IDs
    dept = str
    prof = str
    """
    def __init__(self, name, students, prof, dept):
        self.name = name
        self.students = students
        self.prof = prof
        self.dept = dept


class Major:
    """Class models a major with name, required courses, and elective courses.
    Expected field usage:
    name = str
    required = list
    elective = list
    """
    def __init__(self, name, required, elective):
        self.name = name
        self.required = required
        self.elective = elective


class Repo:
    """Class models a repository of students, professors, and courses for an
    ed. institution.

    :assumption: grade date file will always end with "grades.txt" and majors
    data file will always end with "majors.txt"
    """
    students = None  # list after init
    professors = None  # list after init
    courses = None  # dict after init

    def __init__(self, directory):
        std_data = read_file(os.path.join(directory, "students.txt"))
        prof_data = read_file(os.path.join(directory, "instructors.txt"))
        grade_data = read_file(os.path.join(directory, "grades.txt"))
        major_data = read_file(os.path.join(directory, "majors.txt"))

        self.students = self.pop_students(std_data, grade_data)
        self.professors = self.pop_professors(prof_data, grade_data)
        self.courses = self.pop_courses(grade_data)
        self.majors = self.pop_majors(major_data)

    def pop_students(self, s_data, g_data):
        """Transforms the s_data raw student data(with items from g_data)
        and returns a list of Student objects.
        """
        list_of_students = {}
        for student, values in s_data.items():
            classes = {}
            for course_data in g_data:
                if course_data[0] == student and \
                        course_data[2] != '' and \
                        course_data[2] != 'F':
                    classes[course_data[1]] = course_data[2]
            list_of_students[student] = Student(student, values[0],
                                                classes, values[1])
        return list_of_students

    def pop_professors(self, p_data, g_data):
        """Transforms the p_data raw professor data(with items from g_data)
        and returns a list of Student objects.
        """
        list_of_profs = {}
        for prof, values in p_data.items():
            course_dict = {}
            for _, course, _, prf in g_data:
                if prof == prf:
                    if course not in course_dict.keys():
                        course_dict[course] = 1
                    else:
                        course_dict[course] += 1
            list_of_profs[prof] = Professor(prof, values[0],
                                            course_dict, values[1])
        return list_of_profs

    def pop_courses(self, g_data):
        """Transforms the g_data raw course data into a dict of Course objects
        keyed by course name and returns it."""
        list_of_courses = {}
        for student, course, _, prof in g_data:
            if course not in list_of_courses.keys():
                list_of_courses[course] = Course(course, [student], prof,
                                                 self.professors[prof].dept)
            else:
                list_of_courses[course].students.append(student)
        return list_of_courses

    def pop_majors(self, m_data):
        """Transforms the m_data raw majors data and returns a list of
        Student objects.
        """
        list_of_majors = {}
        for major, req, name in m_data:
            if major not in list_of_majors.keys():
                list_of_majors[major] = Major(major, [], [])
            if req == 'R':
                list_of_majors[major].required.append(name)
            else:
                list_of_majors[major].elective.append(name)
        return list_of_majors

    def required_remaining(self, student):
        return sorted([course for course in self.majors[student.major].required
                       if course not in student.courses])

    def elective_remaining(self, student):
        temp = []
        for course in self.majors[student.major].elective:
            if course in student.courses:
                return None
            else:
                temp.append(course)
        return sorted(temp)

    def print_summary_tables(self):
        """Helper to reduce complexity of PrettyTable printers"""
        print("Student Summary")
        print(self.make_student_table())
        print("Professor Summary")
        print(self.make_professor_table())
        print("Course Summary")
        print(self.make_courses_table())
        print("Majors Summary")
        print(self.make_majors_table())

    def make_student_table(self):
        """Returns PrettyTable of Student objects in students."""
        pt = PrettyTable(field_names=["CWID", "Name", "Major",
                                      "Completed Courses",
                                      "Required Remaining",
                                      "Elective Remaining"])
        pt.align = 'l'
        for _, student in self.students.items():
            pt.add_row([student.cwid, student.name,
                        student.major, sorted(student.courses.keys()),
                        self.required_remaining(student),
                        self.elective_remaining(student)])
        return pt

    def make_professor_table(self):
        """Returns PrettyTable of Professor objects in professors."""
        pt = PrettyTable(field_names=["CWID", "Name", "Dept",
                                      "Taught Courses"])
        pt.align = 'l'
        for _, professor in self.professors.items():
            pt.add_row([professor.cwid, professor.name,
                        professor.dept, sorted(professor.courses.keys())])
        return pt

    def make_courses_table(self):
        """Returns PrettyTable of Coursse objects in courses.

        :note: While printed under the 'Courses Summary' header, this is
        analogous to the HW09 'Professor Summary' table."""
        pt = PrettyTable(field_names=["CWID", "Name", "Dept",
                                      "Course", "Students"])
        pt.align = 'l'
        for key, course_data in self.courses.items():
            pt.add_row([course_data.prof,
                        self.professors[course_data.prof].name,
                        self.professors[course_data.prof].dept,
                        course_data.name,
                        len(course_data.students)])
        return pt

    def make_majors_table(self):
        """Returns PrettyTable of Major objects in majors."""
        pt = PrettyTable(field_names=["Dept", "Required", "Elective"])
        pt.align = 'l'
        for _, value in self.majors.items():
            pt.add_row([value.name, sorted(value.required),
                        sorted(value.elective)])
        return pt


def read_file(file):
    """Static reader to parse a data file and return a container appropriate to
    the file type of objects contained within that file (list for Student or
    Professor, dict for Courses)."""
    try:
        fp = open(file, 'r')
    except (FileNotFoundError, IOError):
        raise OSError("--Error: {} doesn't exist or can't be "
                      "opened for reading.".format(file))
    else:
        with fp:
            if file.endswith("grades.txt"):
                file_data = []
                for line in fp:
                    line_temp = line.strip("\n").split("\t")
                    if len(line_temp) == 4:
                        file_data.append((line_temp[0], line_temp[1],
                                          line_temp[2], line_temp[3]))
            elif file.endswith("majors.txt"):
                file_data = []
                for line in fp:
                    line_temp = line.strip("\n").split("\t")
                    if len(line_temp) == 3:
                        file_data.append((line_temp[0], line_temp[1],
                                          line_temp[2]))
            else:
                file_data = defaultdict(dict)
                for line in fp:
                    line_temp = line.strip("\n").split("\t")
                    if len(line_temp) == 3:
                        file_data[line_temp[0]] = (line_temp[1], line_temp[2])
                    else:
                        file_data[line_temp[0]] = ("", "")
    return file_data


def main():
    repo = Repo(os.path.join(os.getcwd(), "normal"))
    repo.print_summary_tables()


if __name__ == '__main__':
    main()
