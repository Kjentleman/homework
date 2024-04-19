import getpass
import os
import re
import subprocess
import time
from logger import log_activity

class ExeRunner:
    def __init__(self):
        self.username = getpass.getuser()
        self.cmdline = 'tmp/example.exe'
        self.cmd = ['tmp/example.exe']
        self.pname = 'example.exe'

    def run_exe(self):
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        
        prompt = input(f"""
RUN EXECUTABLE
Enter the file path to an executable as well as any command line arguments
Example: 'your/file/path/example.exe -f ENV=dev'
For reference the current directory is: {current_dir}
Or leave blank to run 'tmp/example.exe'
> """)
        
        if prompt:
            self.cmdline = prompt
            self.cmd = self.cmdline.split()
            try:
                self.pname = re.search(r'[^\\/]+$', self.cmd[0]).group()
            except:
                self.pname = prompt

        try:
            timestamp = time.time()
            process = subprocess.Popen(self.cmd)
            row = f"\n{timestamp},{self.username},{process.pid},{self.pname},{self.cmdline},,,,,"
            log_activity(row)
        except Exception as e:
            print(f"Unable to run '{self.cmdline}' with errors:", e)
        finally:
            process.terminate()
            process.wait()