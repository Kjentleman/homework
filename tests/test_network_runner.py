import unittest
from unittest.mock import patch
import re

import sys
sys.path.append('homework')

from logger import get_last_activity
from network_runner import NetworkRunner

class TestExeRunner(unittest.TestCase):
    @patch('builtins.input', return_value='')
    def test_transmit_data(self, _):
        runner = NetworkRunner()
        runner.transmit_data()
        
        last_activity = get_last_activity()
        regex = rf"""^\d+\.\d+,           # timestamp
            {re.escape(runner.username)}, # username
            {runner.pid},                 # pid
            {re.escape(runner.pname)},    # process name
            {re.escape(runner.cmdline)},  # command line
            ,                             # file path
            ,                             # descriptor
            \d+\.\d+\.\d+\.\d+:\d+,       # source
            685,                          # payload
            HTTPS$                        # protocol
        """
        pattern = re.compile(regex, re.VERBOSE)
        self.assertTrue(pattern.search(last_activity))

if __name__ == '__main__':
    unittest.main()