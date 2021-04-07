#!/usr/bin/env python3

import subprocess
import argparse
import sys
import hashlib

KEEPASS_LS = ['keepassxc-cli', 'ls', '-R', '-f']
KEEPASS_SHOW = ['keepassxc-cli', 'show', '-s']







class DBEntry:
    TITLE = 'Title: '
    USERNAME = 'UserName: '
    PASSWORD = "Password: "
    URL = 'URL: '
    NOTES = 'Notes: '

    def __init__(self, path=None, title=None, user_name=None, password_hash=None, url=None, notes=None):
        self.path = path
        self.title = title
        self.user_name = user_name
        self.password_hash = password_hash
        self.url = url
        self.notes = notes

    @classmethod
    def extract_value(cls, header, line):
        if line.startswith(header):
            return line[len(header):]
        return None

    @classmethod
    def create_password_hash(cls, password, salt='salt'):
        dk = hashlib.pbkdf2_hmac('sha512', password.encode(), salt.encode(), 100000)
        return dk.hex()

    @classmethod
    def from_lines(cls, path, lines, salt):
        title = None
        user_name = None
        password_hash = None
        url = None
        notes = None
        for line in lines:
            value = DBEntry.extract_value(DBEntry.TITLE, line)
            title = value if value is not None else title
            value = DBEntry.extract_value(DBEntry.USERNAME, line)
            user_name = value if value is not None else user_name
            value = DBEntry.extract_value(DBEntry.PASSWORD, line)
            password_hash = DBEntry.create_password_hash(value, salt) if value is not None else password_hash
            value = DBEntry.extract_value(DBEntry.URL, line)
            url = value if value is not None else url
            value = DBEntry.extract_value(DBEntry.NOTES, line)
            notes = value if value is not None else notes
        return cls(path, title, user_name, password_hash, url, notes)

    def __eq__(self, other):
        return self.is_same(other)

    def is_same(self, other,
                ignore_path = False,
                ignore_title = False,
                ignore_username = False,
                ignore_password = False,
                ignore_url = False,
                ignore_notes = False):
        if not isinstance(other, DBEntry):
            return NotImplemented
        return ((ignore_path or self.path == other.path)
                and (ignore_title or self.title == other.title)
                and (ignore_username or self.user_name == other.user_name)
                and (ignore_password or self.password_hash == other.password_hash)
                and (ignore_url or self.url == other.url)
                and (ignore_notes or self.notes == other.notes))


def execute_keepass_command(command, password, suppress_no_entries=False, check=True):
    output = subprocess.run(command, input=password,
                            universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode:
        if (not suppress_no_entries) or ('Could not find entry with path' not in output.stderr):
            print('command failed: ', output.stderr)
        if check:
            output.check_returncode()
        else:
            return
    return output.stdout.splitlines()


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('database1', help='the first database to compare')
    parser.add_argument('password1', help='the password of the first database')
    parser.add_argument('database2', help='the second database to compare')
    parser.add_argument('password2', help='the password of the second database')

    parser.add_argument('--ignore-new-in-first', help='ignore new entries in the first database',
                        dest='ignore_new_in_first', action='store_true', default=False)
    parser.add_argument('--ignore-new-in-second', help='ignore new entries in the second database',
                        dest='ignore_new_in_second', action='store_true', default=False)

    parser.add_argument('--ignore-title', help='do not compare title',
                        dest='ignore_title', action='store_true', default=False)
    parser.add_argument('--ignore-username', help='do not compare username',
                        dest='ignore_username', action='store_true', default=False)
    parser.add_argument('--ignore-password', help='do not compare password',
                        dest='ignore_password', action='store_true', default=False)
    parser.add_argument('--ignore-url', help='do not compare url',
                        dest='ignore_url', action='store_true', default=False)
    parser.add_argument('--ignore-notes', help='do not compare notes',
                        dest='ignore_notes', action='store_true', default=False)

    return parser.parse_args(argv)


def read_database_content(database, password):
    result = []
    lines = execute_keepass_command(KEEPASS_LS + [database], password)
    for path in lines:
        entry = execute_keepass_command(KEEPASS_SHOW + [database, path], password, suppress_no_entries=True,
                                        check=False)
        if entry:
            result.append(DBEntry.from_lines(path, entry, 'salt'))
    return result


def convert(database):
    result = {}
    for entry in database:
        result[entry.path] = entry
    return result


def diff_dbs(argv):
    args = parse_args(argv)
    first_database = convert(read_database_content(args.database1, args.password1))
    second_database = convert(read_database_content(args.database2, args.password2))
    keys = set(first_database)
    keys.union(set(second_database))
    for key in keys:
        first_entry = first_database[key]
        second_entry = second_database[key]
        if first_entry is None and second_entry is not None and args.ignore_new_in_second:
            continue
        else:
            print('new entry in %s:%s', args.database2, second_entry.path)
            continue
        if first_entry is not None and second_entry is None and args.ignore_new_in_first:
            continue
        else:
            print('new entry in %s:%s', args.database1, first_entry.path)
            continue
        if not first_entry.is_same(second_entry,
                                   args.ignore_title,
                                   args.ignore_username,
                                   args.ignore_password,
                                   args.ignore_url,
                                   args.ignore_notes):
            print('%s:%s and %s:%s differ', args.database1, first_entry.path, args.database2, second_entry.path)


if __name__ == "__main__":
    diff_dbs(sys.argv[1:])
