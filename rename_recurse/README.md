# Prerequisite:

 - Python3
 - Lib: sys, os, docopt

# Usage:
  _rename.py --path PATH

# Options:
  -h --help     Show this help section.
  -p, --path     Path of directory.


# Example 
- File structure 
 /tmp/Test/:
total 8
drwxr-xr-x. 3 root root 4096 May  7 06:00 Aabc
drwxr-xr-x. 3 root root 4096 May  7 06:00 zAbcD

/tmp/Test/Aabc:
total 4
-rw-r--r--. 1 root root    0 May  7 06:00 {a-f}
drwxr-xr-x. 2 root root 4096 May  7 06:00 zxv_{1a

/tmp/Test/Aabc/zxv_{1a:
total 0

/tmp/Test/zAbcD:
total 4
drwxr-xr-x. 2 root root 4096 May  7 06:00 abcd
-rw-r--r--. 1 root root    0 May  7 06:00 {g-m}

/tmp/Test/zAbcD/abcd:

#Run Script 

# python3 _rename.py -p /tmp/Test_False_ptha
Path Dir "/tmp/Test_False_ptha" not exist, please validate !

# python3 _rename.py -p /tmp/Test
{code}
 Input Path: /tmp/Test
 Rename /tmp/Test/zAbcD/abcd -> /tmp/Test/zAbcD/abcd :  No Change
 Rename /tmp/Test/zAbcD/{g-m} -> /tmp/Test/zAbcD/{g-m} :  No Change
 Rename /tmp/Test/Aabc/zxv_{1a -> /tmp/Test/Aabc/zxv_{1a :  No Change
 Rename /tmp/Test/Aabc/{a-f} -> /tmp/Test/Aabc/{a-f} :  No Change
 Rename /tmp/Test/zAbcD -> /tmp/Test/zabcd :  Success
 Rename /tmp/Test/Aabc -> /tmp/Test/aabc :  Success
{code}
 
