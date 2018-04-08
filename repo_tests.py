import unittest
import os
from collections import defaultdict
import repo_djackson as h

"""
:author: Daniel Jackson
1Apr18
SSW-810-A
Assignment HW10

Container for unittests for the edu institution repo project in 
hw09_djackson.py.
"""


class EduRepoTests(unittest.TestCase):
    """Class is a container for the Repo class and required inputs to that
    class (Student, Professor, Course classes and file_reader() function.
    Test blocks will identify the test data set required via the path variable.
    All additional test data will be delivered with this module."""

    PATH_TC1 = os.path.join(os.getcwd(), "test")

    def test_file_reader(self):
        s = h.read_file(os.path.join(EduRepoTests.PATH_TC1, "students.txt"))
        self.assertEqual(type(s), defaultdict)
        self.assertEqual(s["10103"], ('Baldwin, C', 'SFEN'))
        self.assertEqual(s["10101"], {})

        p = h.read_file(os.path.join(EduRepoTests.PATH_TC1, "instructors.txt"))
        self.assertEqual(type(p), defaultdict)
        self.assertEqual(p["98765"], ('Einstein, A', 'SFEN'))
        self.assertEqual(p["0"], ('0', '0'))
        self.assertEqual(p["1"], ('', ''))

        g = h.read_file(os.path.join(EduRepoTests.PATH_TC1, "grades.txt"))
        self.assertEqual(type(g), list)
        self.assertEqual(g[0], ('10103', 'SSW 567', 'A', '98765'))
        self.assertEqual(g[4], ('0', '0', '0', '0'))
        with self.assertRaises(IndexError):
            print(g[5])
        with self.assertRaises(OSError):
            h.read_file(os.path.join(EduRepoTests.PATH_TC1, "nothere.txt"))

    def test_repo_maker(self):
        repo = h.Repo(EduRepoTests.PATH_TC1)
        self.assertEqual(type(repo.students), dict)
        self.assertEqual(type(repo.professors), dict)
        self.assertEqual(type(repo.courses), dict)

    def test_student_list(self):
        repo = h.Repo(EduRepoTests.PATH_TC1)
        s = repo.students["10103"]
        self.assertEqual((s.cwid, s.name, s.courses, s.major),
                         ("10103", "Baldwin, C",
                          {'SSW 564': 'A-', 'SSW 567': 'A'}, "SFEN"))

    def test_professor_list(self):
        repo = h.Repo(EduRepoTests.PATH_TC1)
        p = repo.professors["98765"]
        self.assertEqual((p.cwid, p.name, p.courses, p.dept),
                         ("98765", "Einstein, A",
                          {'SSW 567': 2}, "SFEN"))
        inc_p = repo.professors["1"]  # tests incomplete professor record
        self.assertEqual((inc_p.cwid, inc_p.name, inc_p.courses, inc_p.dept),
                         ("1", "", {}, ""))

    def test_course_dict(self):
        repo = h.Repo(EduRepoTests.PATH_TC1)
        self.assertEqual(len(repo.courses), 3)
        c = repo.courses["SSW 567"]
        self.assertEqual((c.name, c.prof, c.dept, c.students),
                         ("SSW 567", "98765",
                          "SFEN", ['10103', '10115']))
        c = repo.courses["0"]
        self.assertEqual((c.name, c.prof, c.dept, c.students),
                         ("0", "0", "0", ['0']))
        with self.assertRaises(KeyError):
            #  tests that the incomplete course did not result in a Course obj
            print(repo.courses[1])

    def test_majors_dict(self):
        repo = h.Repo(EduRepoTests.PATH_TC1)
        self.assertEqual(len(repo.majors), 3)
        m = repo.majors["SFEN"]
        self.assertEqual(m.name, "SFEN")
        self.assertEqual(m.required,
                         ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'])
        self.assertEqual(m.elective,
                         ['CS 501', 'CS 513', 'CS 545'])
        with self.assertRaises(KeyError):
            #  tests that the incomplete line did not result in a Major obj
            print(repo.majors["SSSS"])
        b = repo.majors["BIO"]
        self.assertEqual(b.required, ['BIO 101', 'BIO 102', 'BIO 103'])
        self.assertEqual(b.elective, ['1', '2'])

    def test_course_remainers(self):
        repo = h.Repo(EduRepoTests.PATH_TC1)
        self.assertEqual(repo.required_remaining(repo.students["10103"]),
                         ['SSW 540', 'SSW 555'])
        self.assertEqual(repo.elective_remaining(repo.students["10103"]),
                         ['CS 501', 'CS 513', 'CS 545'])
