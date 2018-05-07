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
├── AbZ
│   └── abz
│       └── A1
│           └── B2
└── Bfd
    ├── AsZ
    └── ASz
        └── a1
            ├── c1
            └── C1

```

## Run Script 

### python3 _rename.py -p /tmp/Test_False_ptha
Path Dir "/tmp/Test_False_ptha" not exist, please validate !

### python3 _rename.py -p /tmp/Test
```
Input Path: /tmp/Test/
Rename /tmp/Test/Bfd/ASz/a1/C1 -> /tmp/Test/Bfd/ASz/a1/c1 :  Already File exist with same name, skipping ..
Rename /tmp/Test/Bfd/ASz/a1/c1 -> /tmp/Test/Bfd/ASz/a1/c1 :  No Change
Rename /tmp/Test/Bfd/ASz/a1 -> /tmp/Test/Bfd/ASz/a1 :  No Change
Rename /tmp/Test/Bfd/ASz -> /tmp/Test/Bfd/asz :  Success Changed
Rename /tmp/Test/Bfd/AsZ -> /tmp/Test/Bfd/asz :  Already File exist with same name, skipping ..
Rename /tmp/Test/AbZ/abz/A1/B2 -> /tmp/Test/AbZ/abz/A1/b2 :  Success Changed
Rename /tmp/Test/AbZ/abz/A1 -> /tmp/Test/AbZ/abz/a1 :  Success Changed
Rename /tmp/Test/AbZ/abz -> /tmp/Test/AbZ/abz :  No Change
Rename /tmp/Test/Bfd -> /tmp/Test/bfd :  Success Changed
Rename /tmp/Test/AbZ -> /tmp/Test/abz :  Success Changed
```
### After run
```
/tmp/Test/
├── abz
│   └── abz
│       └── a1
│           └── b2
└── bfd
    ├── asz
    │   └── a1
    │       ├── c1
    │       └── C1
    └── AsZ

```
