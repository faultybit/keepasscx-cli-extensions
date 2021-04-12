#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from diff_dbs import DBEntry


class TestDBEntry(unittest.TestCase):

    def test_extract_value(self):
        self.assertEqual('abc', DBEntry.extract_value('', 'abc'))

    def test_extract_value_title(self):
        self.assertEqual('testtitle', DBEntry.extract_value(DBEntry.TITLE, 'Title: testtitle'))

    def test_extract_value_title_wrong_header(self):
        self.assertEqual(None, DBEntry.extract_value(DBEntry.TITLE, 'Title:testtitle'))

    def test_create_password_hash(self):
        self.assertEqual('f9ab2ea533dcc96f57b0278ca4243eabef5f0bb3f21fa1bba64a70963da273ba523458bddbe602eb6bf'
                         'b6329372ba038484596b00a4bbc8c6f92e72c04ced0dd', DBEntry.create_password_hash('a', 'b'))

    def assertDBEntryEqual(self, left, right):
        self.assertEqual(left.path, right.path)
        self.assertEqual(left.title, right.title)
        self.assertEqual(left.user_name, right.user_name)
        self.assertEqual(left.password_hash, right.password_hash)
        self.assertEqual(left.url, right.url)
        self.assertEqual(left.notes, right.notes)

    def test_from_lines_empty(self):
        left = DBEntry()
        right = DBEntry.from_lines(None, [], None)
        self.assertDBEntryEqual(left, right)

    def test_from_lines_with_path_title_username(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username')
        right = DBEntry.from_lines(left.path, ['Title: ' + left.title, 'UserName: ' + left.user_name], None)
        self.assertDBEntryEqual(left, right)

    def test_from_lines_empty_path(self):
        password = 'abc´"1!++#A2233m'
        salt = 'abc'
        left = DBEntry(path='', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash(password, salt), url='https://www.gmail.com',
                       notes='nnn')
        right = DBEntry.from_lines(left.path, ['Title: ' + left.title, 'UserName: ' + left.user_name,
                                               'Password: ' + password, 'URL: ' + left.url,
                                               'Notes: ' + left.notes], salt)
        self.assertDBEntryEqual(left, right)

    def test_from_lines_empty_title(self):
        password = 'abc´"1!++#A2233m'
        salt = 'abc'
        left = DBEntry(path='/a/b', title='', user_name='test_username',
                       password_hash=DBEntry.create_password_hash(password, salt), url='https://www.gmail.com',
                       notes='nnn')
        right = DBEntry.from_lines(left.path, ['Title: ' + left.title, 'UserName: ' + left.user_name,
                                               'Password: ' + password, 'URL: ' + left.url,
                                               'Notes: ' + left.notes], salt)
        self.assertDBEntryEqual(left, right)

    def test_from_lines_empty_username(self):
        password = 'abc´"1!++#A2233m'
        salt = 'abc'
        left = DBEntry(path='/a/b', title='testtitle', user_name='',
                       password_hash=DBEntry.create_password_hash(password, salt), url='https://www.gmail.com',
                       notes='nnn')
        right = DBEntry.from_lines(left.path, ['Title: ' + left.title, 'UserName: ' + left.user_name,
                                               'Password: ' + password, 'URL: ' + left.url,
                                               'Notes: ' + left.notes], salt)
        self.assertDBEntryEqual(left, right)

    def test_from_lines_empty_password(self):
        password = ''
        salt = 'abc'
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash(password, salt),
                       url='https://www.gmail.com', notes='nnn')
        right = DBEntry.from_lines(left.path, ['Title: ' + left.title, 'UserName: ' + left.user_name,
                                               'Password: ' + password, 'URL: ' + left.url,
                                               'Notes: ' + left.notes], salt)
        self.assertDBEntryEqual(left, right)

    def test_from_lines_empty_url(self):
        password = 'abc´"1!++#A2233m'
        salt = 'abc'
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash(password, salt), url='', notes='nnn')
        right = DBEntry.from_lines(left.path, ['Title: ' + left.title, 'UserName: ' + left.user_name,
                                               'Password: ' + password, 'URL: ' + left.url,
                                               'Notes: ' + left.notes], salt)
        self.assertDBEntryEqual(left, right)

    def test_from_lines_empty_notes(self):
        password = 'abc´"1!++#A2233m'
        salt = 'abc'
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash(password, salt), url='https://www.gmail.com',
                       notes='')
        right = DBEntry.from_lines(left.path, ['Title: ' + left.title, 'UserName: ' + left.user_name,
                                               'Password: ' + password, 'URL: ' + left.url,
                                               'Notes: ' + left.notes], salt)
        self.assertDBEntryEqual(left, right)

    def test_from_lines_full(self):
        password = 'abc´"1!++#A2233m'
        salt = 'abc'
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash(password, salt), url='https://www.gmail.com',
                       notes='nnn')
        right = DBEntry.from_lines(left.path, ['Title: ' + left.title, 'UserName: ' + left.user_name,
                                               'Password: ' + password, 'URL: ' + left.url,
                                               'Notes: ' + left.notes], salt)
        self.assertDBEntryEqual(left, right)

    def test_equals_diff_class(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        self.assertNotEqual(left, 'right')

    def test_equals_diff_the_same(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        self.assertEqual(left, left)

    def test_equals_diff_the_same_values(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        right = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                        password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        self.assertEqual(left, right)

    def test_equals_diff_path(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        right = DBEntry(path='/a/c', title='testtitle', user_name='test_username',
                        password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn2')
        self.assertNotEqual(left, right)

    def test_equals_diff_title(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        right = DBEntry(path='/a/b', title='testtitle1', user_name='test_username',
                        password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        self.assertNotEqual(left, right)

    def test_equals_diff_user_name(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        right = DBEntry(path='/a/b', title='testtitle', user_name='test_username1',
                        password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        self.assertNotEqual(left, right)

    def test_equals_diff_password(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        right = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                        password_hash=DBEntry.create_password_hash('b', 'b'), url='https://www.gmail.com', notes='nnn')
        self.assertNotEqual(left, right)

    def test_equals_diff_url(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        right = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                        password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail2.com', notes='nnn')
        self.assertNotEqual(left, right)

    def test_equals_diff_notes(self):
        left = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                       password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn')
        right = DBEntry(path='/a/b', title='testtitle', user_name='test_username',
                        password_hash=DBEntry.create_password_hash('a', 'b'), url='https://www.gmail.com', notes='nnn2')
        self.assertNotEqual(left, right)

    @parameterized.expand([
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            [False, False, False, False, False, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title', 'user_name', 'password', 'url', 'notes'],
            [False, False, False, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title', 'user_name', 'password', 'url', 'notes'],
            [True, False, False, False, False, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title2', 'user_name', 'password', 'url', 'notes'],
            [False, False, False, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title2', 'user_name', 'password', 'url', 'notes'],
            [False, True, False, False, False, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title', 'user_name2', 'password', 'url', 'notes'],
            [False, False, False, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title', 'user_name2', 'password', 'url', 'notes'],
            [False, False, True, False, False, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title', 'user_name', 'password2', 'url', 'notes'],
            [False, False, False, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title', 'user_name', 'password2', 'url', 'notes'],
            [False, False, False, True, False, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title', 'user_name', 'password', 'url2', 'notes'],
            [False, False, False, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title', 'user_name', 'password', 'url2', 'notes'],
            [False, False, False, False, True, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title', 'user_name', 'password', 'url', 'notes2'],
            [False, False, False, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path', 'title', 'user_name', 'password', 'url', 'notes2'],
            [False, False, False, False, False, True],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name', 'password', 'url', 'notes'],
            [True, False, False, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name', 'password', 'url', 'notes'],
            [True, True, False, False, False, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name2', 'password', 'url', 'notes'],
            [True, True, False, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name2', 'password', 'url', 'notes'],
            [True, True, False, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name2', 'password', 'url', 'notes'],
            [True, True, True, False, False, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name2', 'password2', 'url', 'notes'],
            [True, True, True, False, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name2', 'password2', 'url', 'notes'],
            [True, True, True, True, False, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name2', 'password2', 'url2', 'notes'],
            [True, True, True, True, False, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name2', 'password2', 'url2', 'notes'],
            [True, True, True, True, True, False],
            True
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name2', 'password2', 'url2', 'notes2'],
            [True, True, True, True, True, False],
            False
        ],
        [
            ['path', 'title', 'user_name', 'password', 'url', 'notes'],
            ['path2', 'title2', 'user_name2', 'password2', 'url2', 'notes2'],
            [True, True, True, True, True, True],
            True
        ]
    ])
    def test_eq(self, first, second, same_parameters, expected):
        first_entry = DBEntry(first[0], first[1], first[2],
                              DBEntry.create_password_hash(first[3]),
                              first[4], first[5])
        second_entry = DBEntry(second[0], second[1], second[2],
                               DBEntry.create_password_hash(second[3]),
                               second[4], second[5])
        self.assertEqual(expected,
                         first_entry.is_same(second_entry,
                                             ignore_path=same_parameters[0],
                                             ignore_title=same_parameters[1],
                                             ignore_username=same_parameters[2],
                                             ignore_password=same_parameters[3],
                                             ignore_url=same_parameters[4],
                                             ignore_notes=same_parameters[5]
                                             ))


if __name__ == '__main__':
    unittest.main()
