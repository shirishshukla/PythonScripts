## Prerequisite:

 - Python3
 - Lib: sys, os, docopt

## Usage:
  _rename.py --path PATH

## Options:
  -h --help     Show this help section.
  -p, --path     Path of directory.


## Example 
* Directory structure 
```
/tmp/Test/
├── A
│   └── z
│       ├── a1
│       │   └── b3
│       │       └── test.txt
│       └── A1
│           └── b3
│               └── TeSt.txt
└── R
    └── P
        └── D1
            └── B3
                └── ZteSt1.Txt
```

## Run Script 

### python3 _rename.py -p /tmp/Test_False_ptha
Path Dir "/tmp/Test_False_ptha" not exist, please validate !

### python3 _rename.py -p /tmp/Test
```
 Input Path: /tmp/Test
 Rename /tmp/Test/zAbcD/abcd -> /tmp/Test/zAbcD/abcd :  No Change
 Rename /tmp/Test/zAbcD/{g-m} -> /tmp/Test/zAbcD/{g-m} :  No Change
 Rename /tmp/Test/Aabc/zxv_{1a -> /tmp/Test/Aabc/zxv_{1a :  No Change
 Rename /tmp/Test/Aabc/{a-f} -> /tmp/Test/Aabc/{a-f} :  No Change
 Rename /tmp/Test/zAbcD -> /tmp/Test/zabcd :  Success
 Rename /tmp/Test/Aabc -> /tmp/Test/aabc :  Success
```
