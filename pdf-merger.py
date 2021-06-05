#!/usr/bin/python
"""A simple script to merge two PDFs."""

import argparse
from os import listdir
from os.path import join as opjoin
import shutil
from subprocess import check_call, CalledProcessError
import tempfile

SEPARATE = 'pdfseparate %s %s'
MERGE = 'pdfunite %s %s'

def my_exec(command):
    """Execute a command from a shell, ignoring errors."""
    try:
        check_call(command, shell=True)
    except CalledProcessError:
        pass

def run(odd, even, out, reverse_odd=False, reverse_even=True):
    """Interleave odd and even pages from two PDF files."""
    folder = tempfile.mkdtemp()
    my_exec(SEPARATE % (odd, opjoin(folder, 'odd%d.pdf')))
    my_exec(SEPARATE % (even, opjoin(folder, 'even%d.pdf')))
    odd_files = []
    even_files = []
    for curr_file in listdir(folder):
        filepath = opjoin(folder, curr_file)
        if curr_file.startswith('odd'):
            odd_files.append((filepath, int(curr_file[3:-4])))
        elif curr_file.startswith('even'):
            even_files.append((filepath, int(curr_file[4:-4])))
    func = lambda x: x[1]
    odd_files.sort(key=func, reverse=reverse_odd)
    even_files.sort(key=func, reverse=reverse_even)
    parts = []
    for line in zip(odd_files, even_files):
        parts.append(line[0][0])
        parts.append(line[1][0])
    my_exec(MERGE % (' '.join(parts), out))
    shutil.rmtree(folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge two PDF files.')
    parser.add_argument('odd_pages', help='PDF containing the odd pages.')
    parser.add_argument('even_pages', help='PDF containing the even pages.')
    parser.add_argument('output_file', help='The target output file.')
    parser.add_argument('--reverse-odd', action='store_true', 
                        help='Insert the odd pages in reverse order.')
    parser.add_argument('--no-reverse-even', action='store_true',
                        help='Suppress reversal of the even pages.')
    args = parser.parse_args()
    run(args.odd_pages, args.even_pages, args.output_file,
        args.reverse_odd, not args.no_reverse_even)
