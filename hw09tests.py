import unittest
from collections import defaultdict
import hw09_djackson as h

"""
:author: Daniel Jackson
26Mar18
SSW-810-A
Assignment HW09
Version: 1

Container for unittests for the edu institution repo project in 
hw09_djackson.py.
"""


class EduRepoTests(unittest.TestCase):
    """Class is a container for the Repo class and required inputs to that
    class (Student, Professor, Course classes and file_reader() function.
    Test blocks will identify the test data required. All additional
    test data will be delivered with this module."""

    def test_file_reader(self):
        """All tests require abbreviated data files in the TC1 folder."""
        s = h.read_file(r"C:\Users\Dan\PycharmProjects\hw09\test\students.txt")
        self.assertEqual(type(s), defaultdict)
        self.assertEqual(s["10103"], ('Baldwin, C', 'SFEN'))
        self.assertEqual(s["10101"], {})

        p = h.read_file(
            r"C:\Users\Dan\PycharmProjects\hw09\test\instructors.txt")
        self.assertEqual(type(p), defaultdict)
        self.assertEqual(p["98765"], ('Einstein, A', 'SFEN'))
        self.assertEqual(p["0"], ('0', '0'))
        self.assertEqual(p["1"], ('', ''))

        g = h.read_file(r"C:\Users\Dan\PycharmProjects\hw09\test\grades.txt")
        self.assertEqual(type(g), list)
        self.assertEqual(g[0], ('10103', 'SSW 567', 'A', '98765'))
        self.assertEqual(g[4], ('0', '0', '0', '0'))
        with self.assertRaises(IndexError):
            print(g[5])
        with self.assertRaises(OSError):
            h.read_file(r"C:\Users\Dan\PycharmProjects\hw09\test\nothere.txt")

    def test_repo_maker(self):
        """Requires abbreviated data files in the TC1 folder."""
        repo = h.Repo(r"C:\Users\Dan\PycharmProjects\hw09\test")
        self.assertEqual(type(repo.students), list)
        self.assertEqual(type(repo.professors), list)
        self.assertEqual(type(repo.courses), dict)

    def test_student_list(self):
        """Tests all student related functionality in Repo."""
        repo = h.Repo(r"C:\Users\Dan\PycharmProjects\hw09\test")
        s = repo.get_student("10103")
        self.assertEqual((s.cwid, s.name, s.courses, s.major),
                         ("10103", "Baldwin, C",
                          {'SSW 567': 'A', 'SSW 564': 'A-'}, "SFEN"))
        self.assertEqual(repo.get_student("444444"), None)

    def test_professor_list(self):
        """Tests all professor related functionality in Repo."""
        repo = h.Repo(r"C:\Users\Dan\PycharmProjects\hw09\test")
        p = repo.get_professor("98765")
        self.assertEqual((p.cwid, p.name, p.courses, p.dept),
                         ("98765", "Einstein, A",
                          {'SSW 567': 2}, "SFEN"))
        self.assertEqual(repo.get_professor("444444"), None)
        inc_p = repo.get_professor("1")  # tests incomplete professor record
        self.assertEqual((inc_p.cwid, inc_p.name, inc_p.courses, inc_p.dept),
                         ("1", "", {}, ""))

    def test_course_dict(self):
        """Tests all course related functionality in Repo."""
        repo = h.Repo(r"C:\Users\Dan\PycharmProjects\hw09\test")
        self.assertEqual(len(repo.courses), 3)
        c = repo.courses["SSW 567"]
        self.assertEqual((c.name, c.prof, c.dept, c.students),
                         ("SSW 567", "98765",
                          "SFEN", ['10103', '10115']))
        c = repo.courses["0"]
        self.assertEqual((c.name, c.prof, c.dept, c.students),
                         ("0", "0", "0", ['0']))
        with self.assertRaises(KeyError):
            #  tests that the incomplete oourse did not result in a Course obj
            print(repo.courses[1])
