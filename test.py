from lxml import etree 
from xmldiff import main, formatting
import os
import sys
import subprocess

from unittest.mock import patch

PATH_TO_TEST_FOLDER = f"{os.getcwd()}/test/parse-only/"

class Test():

    def __init__(self, ):
        self.cnt_passed = 0
        self.cnt_failed = 0
        self.cnt_tests = 0
        self.cnt_files = 0

        self.args = ["php", "parse.php"]

    def test(self, path, files):

        files = sorted(files, key=str.lower)

        for file in files:
            
            if file == "README.md":
                continue

            if os.path.isdir(f"{path}{file}"):
                files = os.listdir(f"{path}{file}/")
                self.test(f"{path}{file}/", files)
            else:
                self.test_directory(path)
                return

    def test_directory(self, path, set_output = False):
     
        files = os.listdir(path)
        files = sorted(files, key=str.lower)

        for filename in files:

            if filename.endswith('.src'):

                self.cnt_tests += 1

                # Execute parser.php
                file_to_parse = open(f"{path}{filename}")
                status = subprocess.run(self.args, stdin=file_to_parse, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode

                # Compare the return code
                with open(f"{path}{filename[:-4]}.rc", "r") as f:
                    line = f.readline()
                    if int(line) != status:
                        if set_output:
                            print(f"{filename} : Failed")
                            
                        self.cnt_failed += 1
                        continue
                    else:
                        if set_output:
                            print(f"{filename} : OK")
                        
                        if status != 0:
                            self.cnt_passed += 1
                            continue

                # Compare xml files
                result = main.diff_files("output.xml",
                        f"{path}{filename[:-4]}.out",
                        diff_options={'F' : 0.5, 'ratio_mode' : 'fast'})
                
                if len(result) == 0:
                    if set_output:
                        print(f"{filename} : OK")
                    
                    self.cnt_passed += 1
                else:
                    if set_output:
                        print(f"{filename} : {result}")
                    
                    self.cnt_failed += 1

        print(f"Test folder : {path} Passed : {self.cnt_passed} Failed : {self.cnt_failed}")
        print("----------------")
    
    def stats(self):

        print(f"Number of tests : {self.cnt_tests}")
        print(f"Passed : {self.cnt_passed}")
        print(f"Failed : {self.cnt_failed}")
        print(f"Success : {self.cnt_passed / self.cnt_tests * 100}")

    def test_arguments(self):

        # Append arguments
        if len(sys.argv) > 1:
            for arg in sys.argv[1:]:
                self.args.append(arg)
    
        file_to_parse = open(f"{PATH_TO_TEST_FOLDER}basic/read_test.src")
        status = subprocess.run(self.args, stdin=file_to_parse, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode

        # Remove argument for further testing
        self.args = [arg for arg in self.args if arg not in sys.argv]

        return status


    def mock_arguments(self, args, expected_status):

        _args = ['test.py']
        for arg in args:
            _args.append(arg)

        with patch('sys.argv', _args):
            status = self.test_arguments()
            if status == expected_status:
                print(f'Test case {args} -> OK')
            else:
                print(f"Test case {args} -> Failed : {status}")
                
    def test_mock_arguments(self):
        
        file_names = ["file"]

        self.mock_arguments(['--h'], 10)
        self.mock_arguments(['--help'], 0)
        self.mock_arguments(['--stat'], 10)
        self.mock_arguments(['--stata'], 10)
        self.mock_arguments(['--stats'], 10)
        self.mock_arguments(['--stats'], 10)
        self.mock_arguments([f"--stats={file_names[0]}"], 0)
        self.mock_arguments([f"--stats={file_names[0]}", "--help"], 10)
        self.mock_arguments([f"--loc --stats={file_names[0]}"], 10)
        # self.mock_arguments([f'--stats={file_names[1]}'], 0)
        # self.mock_arguments([f"--stats={file_names[1]}", "--help"], 10)
        # self.mock_arguments([f"--stats={file_names[1]}", f"--stats={file_names[1]}"], 11)
        
        for f in file_names:
            os.remove(f)

test = Test()
# test.test_directory(f"{PATH_TO_TEST_FOLDER}defvar/")
test.test(PATH_TO_TEST_FOLDER, os.listdir(PATH_TO_TEST_FOLDER))
# test.test_mock_arguments()
# test.stats()