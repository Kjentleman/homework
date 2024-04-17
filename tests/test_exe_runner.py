import unittest
import re
from unittest.mock import patch
import sys
sys.path.append('homework')

from logger import get_last_activity
from exe_runner import ExeRunner

class TestExeRunner(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.runner = ExeRunner()
        self.runner.username = 'testuser'
    
    def test_init(self):
        self.assertEqual(self.runner.cmdline, 'tmp/example.exe')
        self.assertEqual(self.runner.cmd, ['tmp/example.exe'])
        self.assertEqual(self.runner.name, 'example.exe')

    @patch('builtins.input', return_value='path/to/file.exe -r ENV=dev')
    def test_prompt(self, _):
        self.runner.prompt()
        self.assertEqual(self.runner.cmdline, 'path/to/file.exe -r ENV=dev')
        self.assertEqual(self.runner.cmd, ['path/to/file.exe', '-r', 'ENV=dev'])
        self.assertEqual(self.runner.name, 'file.exe')

    def test_run_exe(self):
        self.runner.cmdline = 'tmp/example.exe'
        self.runner.cmd = ['tmp/example.exe']
        self.runner.name = 'example.exe'
        self.runner.run_exe()

        last_activity = get_last_activity()
        self.assertTrue(
            re.search(r'^\d+\.\d+,testuser,\d+,example\.exe,tmp\/example.exe,,,,,$', last_activity)
        )

if __name__ == '__main__':
    unittest.main()