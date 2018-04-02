import os
from collections import defaultdict
from prettytable import PrettyTable

"""
:author: Daniel Jackson
26Mar18
SSW-810-A
Assignment HW09
Version: 1

Module contains classes to construct and operate on a repository (Repo) of 
education institution data including Students, Professors, and Courses. 

:note: while the Student, Professor, and Course classes are nearly identical 
currently, they're expected to evolve in subsequent versions. If not, these 
will be refactored into a single utility class with more abstracted attribute 
identifiers.

:note: design decision made to deviate slightly from assignment description and 
organize the repository into three separate data stores for each as it was 
somewhat easier to design and work with. Calls in main() print 3 tables instead
of 2, though the courses summary table shows how these data stores can be used
in conjunction with each other.
"""


class Student:
    """Class models a student with ID, name, major, and a container of courses.
    Expected field usage:
    cwid = str
    name = str
    courses = dict of courses completed "successfully"
    major = str

    :assumption: Repo class will provide methods for Course object retrieval,
    so only need to store course name here, not full Course object.

    :note: no functions needed at this time (V1)
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

    :assumption: Repo class will provide methods for Course object retrieval,
    so only need to store course name here, not full Course object.

    :note: no functions needed at this time (V1)
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

    :assumption: Repo class provides methods for student and professor
    retrieval, so only need to store CWID for these, not full objects.

    :note: no functions needed at this time (V1)
    """
    def __init__(self, name, students, prof, dept):
        self.name = name
        self.students = students
        self.prof = prof
        self.dept = dept


class Repo:
    """Class models a repository of students, professors, and courses for an
    ed. institution.

    :assumption: grade data file must always end with "grades.txt" for the temp
    g_data to be correctly populated by read_file(). Much of this class is
    based on that assumption. If changed, pop_students(), pop_professors(),
    pop_courses(), and make_courses_table() will need updates.

    :assumption: students, professors, and courses can be list objects at this
    time since there is no current need for hashing by ID or name, but this can
    be changed easily if future versions require it.
    """
    students = None  # list after init
    professors = None  # list after init
    courses = None  # dict after init

    def __init__(self, directory):
        try:
            std_data = read_file(directory + os.sep + "students.txt")
            prof_data = read_file(directory + os.sep + "instructors.txt")
            grade_data = read_file(directory + os.sep + "grades.txt")

            self.students = self.pop_students(std_data, grade_data)
            self.professors = self.pop_professors(prof_data, grade_data)
            self.courses = self.pop_courses(grade_data)
        except OSError as o:
            print(o)

    def pop_students(self, s_data, g_data):
        """Transforms the s_data raw student data(with items from g_data)
        and returns a list of Student objects.
        """
        list_of_students = []
        for student, values in s_data.items():
            classes = {}
            for course_data in g_data:
                if course_data[0] == student and \
                        course_data[2] != '' and \
                        course_data[2] != 'F':
                    classes[course_data[1]] = course_data[2]
            list_of_students.append(Student(student, values[0],
                                            classes, values[1]))
        return list_of_students

    def pop_professors(self, p_data, g_data):
        """Transforms the p_data raw professor data(with items from g_data)
        and returns a list of Student objects.
        """
        list_of_profs = []
        for prof, values in p_data.items():
            course_dict = {}
            for _, course, _, prf in g_data:
                if prof == prf:
                    if course not in course_dict.keys():
                        course_dict[course] = 1
                    else:
                        course_dict[course] += 1
            list_of_profs.append(Professor(prof, values[0],
                                           course_dict, values[1]))
        return list_of_profs

    def pop_courses(self, g_data):
        """Transforms the g_data raw course data into a dict of Course objects
        keyed by course name and returns it."""
        list_of_courses = {}
        for student, course, _, prof in g_data:
            if course not in list_of_courses.keys():
                list_of_courses[course] = Course(course, [student], prof,
                                                 self.get_professor(prof).dept)
            else:
                list_of_courses[course].students.append(student)
        return list_of_courses

    def get_professor(self, cwid):
        """Searches the professors list and returns the Professor object
        matching the CWID or None if not found"""
        for prof in self.professors:
            if prof.cwid == cwid:
                return prof
        return None

    def get_student(self, cwid):
        """Searches the students list and returns the Student object
        matching the CWID or None if not found"""
        for student in self.students:
            if student.cwid == cwid:
                return student
        return None

    def print_summary_tables(self):
        """Helper to reduce complexity of PrettyTable printers"""
        print("Student Summary")
        print(self.make_student_table())
        print("Professor Summary")
        print(self.make_professor_table())
        print("Course Summary")
        print(self.make_courses_table())

    def make_student_table(self):
        """Returns PrettyTable of Student objects in students."""
        pt = PrettyTable(field_names=["CWID", "Name", "Major",
                                      "Completed Courses"])
        pt.align = 'l'
        for student in self.students:
            pt.add_row([student.cwid, student.name,
                        student.major, student.courses])
        return pt

    def make_professor_table(self):
        """Returns PrettyTable of Professor objects in professors."""
        pt = PrettyTable(field_names=["CWID", "Name", "Dept",
                                      "Taught Courses"])
        pt.align = 'l'
        for professor in self.professors:
            pt.add_row([professor.cwid, professor.name,
                        professor.dept, professor.courses])
        return pt

    def make_courses_table(self):
        """Returns PrettyTable of Coursse objects in courses.

        :note: While printed under the 'Courses Summary' header, this is
        analagous to the HW09 'Professor Summary' table."""
        pt = PrettyTable(field_names=["CWID", "Name", "Dept",
                                      "Course", "Students"])
        pt.align = 'l'
        for key, course_data in self.courses.items():
            pt.add_row([course_data.prof,
                        self.get_professor(course_data.prof).name,
                        self.get_professor(course_data.prof).dept,
                        course_data.name,
                        len(course_data.students)])
        return pt


def read_file(file):
    """Static reader to parse a data file and return a container appropriate to
    the file type of objects contained within that file (list for Student or
    Professor, dict for Courses)."""
    try:
        fp = open(file, 'r')
    except (FileNotFoundError, IOError):
        raise OSError("--Error: file doesn't exist / can't open file")
    else:
        with fp:
            if file.endswith("grades.txt"):
                file_data = []
                for line in fp:
                    line_temp = line.strip("\n").split("\t")
                    if len(line_temp) == 4:
                        file_data.append((line_temp[0], line_temp[1],
                                          line_temp[2], line_temp[3]))
                    else:
                        pass
                        # print("Incomplete class record, cannot parse")
                        # @todo add elegant error handler
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
    repo = Repo(r"C:\Users\Dan\PycharmProjects\hw09\normal")
    repo.print_summary_tables()


if __name__ == '__main__':
    main()
