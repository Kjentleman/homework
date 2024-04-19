import unittest
from unittest.mock import patch
import re

import sys
sys.path.append('homework')

from logger import get_last_activity
from exe_runner import ExeRunner

class TestExeRunner(unittest.TestCase):    
    def test_init(self):
        runner = ExeRunner()
        if sys.platform == 'win32':
            self.assertEqual(runner.cmdline, 'tmp/example.exe')
        else:
            self.assertEqual(runner.cmdline, 'chmod +x tmp/example.app')

    @patch('builtins.input', return_value='')
    def test_run_exe(self, _):
        runner = ExeRunner()
        runner.run_exe()
        last_activity = get_last_activity()
        regex = rf"""^\d+\.\d+,             # timestamp
            {re.escape(runner.username)},   # username
            \d+,                            # pid
            (chmod|example\.exe),           # process name
            {re.escape(runner.cmdline)},    # command line
            ,                               # file path
            ,                               # descriptor
            ,                               # source
            ,                               # payload
            $                               # protocol
        """
        pattern = re.compile(regex, re.VERBOSE)
        self.assertTrue(pattern.search(last_activity))
if __name__ == '__main__':
    unittest.main()