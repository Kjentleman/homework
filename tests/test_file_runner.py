import unittest
import re
from unittest.mock import patch
import sys
import os
sys.path.append('homework')

from logger import get_last_activity
from file_runner import FileRunner

class TestFileRunner(unittest.TestCase):
    def test_init(self):
        runner = FileRunner()
        self.assertEqual(runner.file_path, 'tmp/file.txt')

    @patch('builtins.input', return_value='tmp/test_create.txt')
    def test_create_file(self, _):
        file_path = 'tmp/test_create.txt'
        runner = FileRunner()
        runner.username = 'testuser'
        
        if os.path.exists(file_path): os.remove(file_path)
        runner.create_file()
        self.assertTrue(os.path.exists(file_path))
        
        last_activity = get_last_activity()
        self.assertTrue(
            re.search(r'^\d+\.\d+,testuser,\d+,,.+,.+tmp\\test_create.txt,create,,,$', last_activity)
        )
        
        os.remove(file_path)

    @patch('builtins.input', return_value='new hotness')
    def test_modify_file(self, _):
        file_path = 'tmp/file.txt'
        runner = FileRunner()
        runner.username = 'testuser'
        
        with open(file_path, 'w') as file:
            file.write('old n busted')
        runner.modify_file()
        with open(file_path, 'r') as file:
            self.assertEqual(file.readline(), 'new hotness')

        last_activity = get_last_activity()
        self.assertTrue(
            re.search(r'^\d+\.\d+,testuser,\d+,,.+,.+tmp\\file.txt,modified,,,$', last_activity)
        )

        os.remove(file_path)
    
    def test_delete_file(self):
        file_path = 'tmp/file.txt'
        runner = FileRunner()
        runner.username = 'testuser'

        with open(file_path, 'w') as file:
            file.write('to be deleted')
        runner.delete_file()

        last_activity = get_last_activity()
        self.assertTrue(
            re.search(r'^\d+\.\d+,testuser,\d+,,.+,.+tmp\\file.txt,delete,,,$', last_activity)
        )

if __name__ == '__main__':
    unittest.main()