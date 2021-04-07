#!/usr/bin/env python3

import unittest
import io
from unittest.mock import patch
from diff_dbs import diff_dbs


class TestDiffDbs(unittest.TestCase):
    STD_ERR = 'sys.stderr'
    STD_OUT = 'sys.stdout'

    def __init__(self, method_name):
        super().__init__(method_name)
        self.database_a = 'testA.kdbx'
        self.password_a = 'a1'
        return

    @patch(STD_ERR, new_callable=io.StringIO)
    @patch(STD_OUT, new_callable=io.StringIO)
    def test_empty(self, mout, merr):
        with self.assertRaises(SystemExit) as exc:
            diff_dbs([])
        self.assertEqual(exc.exception.code, 2)
        self.assertEqual(mout.getvalue(), '')
        lines = merr.getvalue().splitlines()
        self.assertEqual(['usage: Test_diff_dbs.py [-h] [--ignore-new-in-first] [--ignore-new-in-second]',
                          '                        [--ignore-title] [--ignore-username]',
                          '                        [--ignore-password] [--ignore-url] [--ignore-notes]',
                          '                        database1 password1 database2 password2',
                          'Test_diff_dbs.py: error: the following arguments are required: database1, password1,'
                          ' database2, password2'],
                         lines)

    @patch(STD_ERR, new_callable=io.StringIO)
    @patch(STD_OUT, new_callable=io.StringIO)
    def test_help(self, mout, merr):
        with self.assertRaises(SystemExit) as exc:
            diff_dbs(['-h'])
        self.assertEqual(exc.exception.code, 0)
        self.assertEqual(merr.getvalue(), '')
        lines = mout.getvalue().splitlines()
        self.assertEqual(['usage: Test_diff_dbs.py [-h] [--ignore-new-in-first] [--ignore-new-in-second]',
                          '                        [--ignore-title] [--ignore-username]',
                          '                        [--ignore-password] [--ignore-url] [--ignore-notes]',
                          '                        database1 password1 database2 password2', '',
                          'positional arguments:',
                          '  database1             the first database to compare',
                          '  password1             the password of the first database',
                          '  database2             the second database to compare',
                          '  password2             the password of the second database', '', 'optional arguments:',
                          '  -h, --help            show this help message and exit', '  --ignore-new-in-first',
                          '                        ignore new entries in the first database',
                          '  --ignore-new-in-second',
                          '                        ignore new entries in the second database',
                          '  --ignore-title        do not compare title',
                          '  --ignore-username     do not compare username',
                          '  --ignore-password     do not compare password',
                          '  --ignore-url          do not compare url',
                          '  --ignore-notes        do not compare notes'],
                         lines)

    @patch(STD_ERR, new_callable=io.StringIO)
    @patch(STD_OUT, new_callable=io.StringIO)
    def test_the_same(self, mout, merr):
        diff_dbs([self.database_a, self.password_a, self.database_a, self.password_a])
        self.assertEqual(mout.getvalue(), '')
        self.assertEqual(merr.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
