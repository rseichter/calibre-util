#!/usr/bin/env python3
"""
Scans Calibre libraries for duplicates by case insensitive comparison of
subdirectory names ignoring numerical suffixes. Potential duplicates are printed
in pairs of directory paths. Separators and quoting are configurable using
options, so the output can be CSV or easily fed to utilities like 'awk' for
further processing.
"""
__author__ = 'Ralph Seichter'

import argparse
import os
import re

args = None
book_dir_pat = re.compile(r'(.+)(\s+\(\d+\))$')


class Book(object):

    def __init__(self, path, title, suffix):
        self.path = path
        self.title = title
        self.suffix = suffix

    def __str__(self):
        return '(title="%s", suffix="%s", path="%s")' % (self.title, self.suffix, self.path)


def checkdir(dir_entry):
    mo = book_dir_pat.search(dir_entry.name)
    if mo:
        return Book(dir_entry.path, mo.group(1), mo.group(2))
    return None


def dir_entry_key(dir_entry):
    return dir_entry.name.casefold()


def dupescan(dir, depth):
    if depth > args.d:
        return
    books = []
    with os.scandir(dir) as entries:
        for dir_entry in sorted(entries, key=dir_entry_key):
            if dir_entry.is_dir(follow_symlinks=False):
                book = checkdir(dir_entry)
                if book:
                    books.append(book)
                dupescan(dir_entry.path, depth + 1)
    for i in range(len(books) - 1):
        book1 = books[i]
        book2 = books[i + 1]
        if book1.title.casefold() == book2.title.casefold():
            print('%s%s%s%s%s%s%s' % (args.qs, book1.path,
                                      args.qe, args.s, args.qs, book2.path, args.qe))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find duplicates in Calibre library directories.')
    parser.add_argument('-qs', default='"',
                        help='Start quote string (default: ")')
    parser.add_argument('-qe', default='"',
                        help='End quote string (default: ")')
    parser.add_argument('-d', type=int, default=3,
                        help='Scan depth limit (default: 3)')
    parser.add_argument('-s', default='\t',
                        help='Separator string (default: Tabulator)')
    parser.add_argument('directory', nargs='+')
    args = parser.parse_args()
    for d in args.directory:
        dupescan(d, 0)
