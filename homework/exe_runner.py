import os
import getpass
import re
import time
import subprocess
import threading
from logger import log_activity

class ExeRunner:
    def __init__(self):
        self.username = getpass.getuser()
        self.cmdline = 'tmp/example.exe'
        self.cmd = ['tmp/example.exe']
        self.name = 'example.exe'

    def prompt(self):
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        
        prompt = input(f"""
Run an Executable
-----------------
Enter the file path to an executable as well as any command line arguments
Example: 'your/file/path/example.exe -f ENV=dev'
For reference your current directory is: {current_dir}
Or leave blank to run 'tmp/example.exe'
> """)
        
        if prompt:
            self.cmdline = prompt
            self.cmd = self.cmdline.split()
            self.name = re.search(r'[^\\/]+$', self.cmd[0]).group()
    
    def run_exe(self):
        def _thread_exe():
            try:
                timestamp = time.time()
                process = subprocess.Popen(self.cmd)
                row = f"\n{timestamp},{self.username},{process.pid},{self.name},{self.cmdline},,,,,"
                log_activity(row)
            except Exception as e:
                print(f"Unble to run '{self.cmdline}' with errors:", e)

        exe_thread = threading.Thread(target=_thread_exe)
        exe_thread.start()