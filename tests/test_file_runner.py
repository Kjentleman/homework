import unittest
from unittest.mock import patch
import os
import re

import sys
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
        
        if os.path.exists(file_path): os.remove(file_path)
        runner.create_file()
        self.assertTrue(os.path.exists(file_path))

        last_activity = get_last_activity()
        regex = rf"""^\d+\.\d+,             # timestamp
            {re.escape(runner.username)},   # username
            {runner.pid},                   # pid
            ,                               # process name
            {re.escape(runner.cmdline)},    # command line
            {re.escape(runner.full_path)},  # file path
            create,                         # descriptor
            ,                               # source
            ,                               # payload
            $                               # protocol
        """
        pattern = re.compile(regex, re.VERBOSE)
        self.assertTrue(pattern.search(last_activity))
        
        os.remove(file_path)

    @patch('builtins.input', return_value='new hotness')
    def test_modify_file(self, _):
        file_path = 'tmp/file.txt'
        runner = FileRunner()
        
        with open(file_path, 'w') as file:
            file.write('old n busted')
        
        runner.modify_file()
        with open(file_path, 'r') as file:
            self.assertEqual(file.readline(), 'new hotness')

        last_activity = get_last_activity()
        regex = rf"""^\d+\.\d+,             # timestamp
            {re.escape(runner.username)},   # username
            {runner.pid},                   # pid
            ,                               # process name
            {re.escape(runner.cmdline)},    # command line
            {re.escape(runner.full_path)},  # file path
            modified,                       # descriptor
            ,                               # source
            ,                               # payload
            $                               # protocol
        """
        pattern = re.compile(regex, re.VERBOSE)
        self.assertTrue(pattern.search(last_activity))

        os.remove(file_path)
    
    @patch('builtins.input', return_value='')
    def test_delete_file(self, _):
        file_path = 'tmp/file.txt'
        runner = FileRunner()

        with open(file_path, 'w') as file:
            file.write('to be deleted')
        runner.delete_file()
        self.assertFalse(os.path.exists(file_path))

        last_activity = get_last_activity()
        regex = rf"""^\d+\.\d+,             # timestamp
            {re.escape(runner.username)},   # username
            {runner.pid},                   # pid
            ,                               # process name
            {re.escape(runner.cmdline)},    # command line
            {re.escape(runner.full_path)},  # file path
            delete,                         # descriptor
            ,                               # source
            ,                               # payload
            $                               # protocol
        """
        pattern = re.compile(regex, re.VERBOSE)
        self.assertTrue(pattern.search(last_activity))

if __name__ == '__main__':
    unittest.main()