import os
import sys
import json
import hashlib

def getMd5Sum(f):
    return  hashlib.md5(open(f,'rb').read()).hexdigest()

def matchedfiles():
    if os.path.isdir(dir):
        dict = {}
        for r,d,f in os.walk(dir, topdown=False):
           for v in f:
               md5 = getMd5Sum(os.path.join(r, v))
               if md5 in dict.keys():
                   dict[str(md5)] += [os.path.join(r, v)]
               else:
                   dict[str(md5)] = [os.path.join(r, v)]
        if dict:
            lst = []
            for val in dict.values():
                lst.append(val)
            print(json.dumps({"matches": lst }, indent=1))
    else:
        print("Input dir", dir, "not Exist !!")

dir = sys.argv[1]
print("Grouping files based on md5sum:", dir)
matchedfiles()
