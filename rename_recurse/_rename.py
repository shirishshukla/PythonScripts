#!/usr/bin/env python
"""Rename all files and directory to lowercase

Owner: shirish.linux@gmail.com

Usage:
  _rename.py --path PATH

Examples:
  _rename.py -p /tmp/mytest/

Options:
  -h --help     Show this help section.
  -p, --path     Path of directory.

"""

import sys, os
from docopt import docopt

#
def to_lower(path):
    srcpath = os.path.normpath(path)
    # is path exist
    if os.path.isdir(srcpath):
        for r,d,f in os.walk(srcpath, topdown=False):
           if d: rename_df(r,d)
           if f: rename_df(r,f)


def rename_df(r,items):
    try:
        for i in items:
            on=os.path.join(r,i)
            nm=os.path.join(r,i.lower())
            print("Rename {} -> {} : ".format(on, nm), end="")
            if on == nm:
               print(" No Change")
            else:
                if os.path.exists(nm):
                   if os.path.isdir(nm): ftype="File"
                   else: ftype="Dir"
                   print(" Already {} exist with same name, skipping ..".format(ftype))
                else:
                    os.rename(on,nm)
                    if os.path.exists(nm):   print(" Success Changed")
    except Exception as e:
        print("Error: ", str(e))

#
if __name__ == '__main__':
    arg = docopt(__doc__, version='Rename files dirs to lowercase - v.1.0')
    #print(arg)
    PTH = arg['PATH']
    if not os.path.exists(PTH):
        print("Path Dir \"{}\" not exist, please validate !".format(PTH))
        exit(1)
    arg = os.path.expanduser(PTH)
    print("Input Path: "+PTH)
    to_lower(arg)

