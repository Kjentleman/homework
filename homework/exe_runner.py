import getpass
import os
import psutil
import subprocess
import sys
import time
from logger import log_activity

class ExeRunner:
    def __init__(self):
        self.username = getpass.getuser()
        if sys.platform == 'win32':
            self.cmdline = 'tmp/example.exe'
        else:
            # self.cmdline = 'chmod +x tmp/example.app'
            self.cmdline = 'tmp/example.app'

    def run_exe(self):
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        
        prompt = input(f"""
RUN EXECUTABLE
Enter the file path to an executable as well as any command line arguments
Example: 'your/file/path/example.exe -f ENV=dev'
For reference the current directory is: {current_dir}
Or leave blank to run '{self.cmdline}'
> """)
        
        if prompt: self.cmdline = prompt

        try:
            cmd = self.cmdline.split(' ')
            if sys.platform != 'win32': cmd = ['open', '-a'] + self.cmdline.split(' ')
            timestamp = time.time()
            process = subprocess.Popen(cmd)
            pname = psutil.Process(process.pid).name()
            row = f"\n{timestamp},{self.username},{process.pid},{pname},{self.cmdline},,,,,"
            log_activity(row)
            process.terminate()
            process.wait()
        except Exception as e:
            print(f"Unable to run '{self.cmdline}' with errors:", e)