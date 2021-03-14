from lxml import etree 
from xmldiff import main, formatting
import os
import sys
import subprocess

PATH_TO_OUTPUT = "result"
PATH_TO_TEST_FOLDER = f"parse-only/{sys.argv[1]}"


if not os.path.exists(PATH_TO_OUTPUT):
    os.mkdir(PATH_TO_OUTPUT)
else:
    os.rmdir(PATH_TO_OUTPUT)
    os.mkdir(PATH_TO_OUTPUT)    

cwd = os.getcwd()
folder = cwd + f"/test/{PATH_TO_TEST_FOLDER}"

files = os.listdir(folder)
files = sorted(files, key=str.lower)

cnt_passed = 0
cnt_failed = 0
cnt_tests = 0

for filename in files:
    
    if filename.endswith('.src'):

        cnt_tests += 1

        # Execute parser.php
        file_to_parse = open(f"{folder}/{filename}")
        FNULL = open(os.devnull, 'w')
        status = subprocess.run(["php", "parse.php"], stdin=file_to_parse, stdout=FNULL, stderr=subprocess.STDOUT).returncode

        # Check the return code
        if status != 0:
            with open(f"./test/{PATH_TO_TEST_FOLDER}/{filename[:-4]}.rc", "r") as f:
                line = f.readline()
                if int(line) != status:
                    print(f"{filename} : Failed")
                    cnt_failed += 1
                else:
                    print(f"{filename} : OK")
                    cnt_passed += 1
            continue

        # Compare xml files
        result = main.diff_files("output.xml",
                f"./test/{PATH_TO_TEST_FOLDER}/{filename[:-4]}.out",
                diff_options={'F' : 0.5, 'ratio_mode' : 'fast'})
        
        if len(result) == 0:
            print(f"{filename} : OK")
            cnt_passed += 1
        else:
            print(f"{filename} : {result}")
            cnt_failed += 1

print("----------------")
print(f"Number of tests : {cnt_tests}")
print(f"Passed : {cnt_passed}")
print(f"Failed : {cnt_failed}")
print(f"Success : {cnt_passed / cnt_tests * 100}")