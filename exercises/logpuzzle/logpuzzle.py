#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
SERVER_NAME = "http://code.google.com"

def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    full_log = open(filename, 'r').read()
    entries = set(re.findall(r'\S+puzzle\S+', full_log))
    entries = sorted(set(entries))

    key_entries = []
    for entry in entries:
        key_entry = {}
        key_entry['entry'] = entry
        matches = re.findall(r'\-(\w+)', os.path.basename(entry))
        key_entry['key'] = matches[-1]
        key_entries.append(key_entry)

    key_entries = sorted(key_entries, lambda x, y: cmp(x['key'], y['key']))
    entries = [x['entry'] for x in key_entries]
    return entries

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    local_files = []
    img_counter = 0
    for img_url in img_urls:
        full_url = SERVER_NAME + img_url
        print "Retreaving: " + full_url
        local_file = os.path.join(dest_dir, "img" + str(img_counter) + ".jpg")
        urllib.urlretrieve(full_url, local_file)
        local_files.append(local_file)
        img_counter += 1

    # Write index.html like:
    # <verbatim>
    # <html>
    # <body>
    # <img src="/edu/python/exercises/img0"><img src="/edu/python/exercises/img1"><img src="/edu/python/exercises/img2">...
    # </body>
    # </html>
    # First, build the index file content
    index_content = ""
    index_content += ("<verbatim>\n"
                      "<html>\n"
                      "<body>\n")

    for local_file in local_files:
        img_tag = '<img src="' + os.path.basename(local_file) + '">'
        index_content += img_tag

    index_content += ("</body>\n"
                      "</html>\n")

    # Then, dump the content into a file
    index_filename = os.path.join(dest_dir, "index.html")
    fhandle = open(index_filename, 'w')
    fhandle.write(index_content)
    fhandle.close()


def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)
        print "Number of images: " + str(len(img_urls))


if __name__ == '__main__':
    main()
