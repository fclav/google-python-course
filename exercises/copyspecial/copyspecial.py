#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(adir):
    filenames = os.listdir(adir)
    filenames = filter(lambda x: re.search(r'__\w+__', x), filenames)
    filenames = map(lambda x: os.path.abspath(x), filenames)
    return filenames

def print_filenames(filenames):
    for filename in filenames:
        print filename

def copy_to(paths, adir):
    os.makedirs(adir)
    for path in paths:
        copy_path = os.path.join(adir, os.path.basename(path))
        shutil.copyfile(path, copy_path)

def zip_to(paths, zippath):
    cmd = "zip -j " + zippath + ' ' + ' '.join(paths)
    commands.getoutput(cmd)

def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print "usage: [--todir dir][--tozip zipfile] dir [dir ...]"
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print "error: must specify one or more dirs"
        sys.exit(1)

    # +++your code here+++
    # Call your functions
    filenames = []
    for arg in args:
        filenames.extend(get_special_paths(arg))


    if len(todir) > 0:
        copy_to(filenames, todir)
    elif len(tozip) > 0:
        zip_to(filenames, tozip)
    else:
        print_filenames(filenames)



if __name__ == "__main__":
    main()
