import getpass
import os
import psutil
import time
from logger import log_activity

class FileRunner:
    def __init__(self):
        self.username = getpass.getuser()
        self.file_path = 'tmp/file.txt'
        self.full_path = os.path.abspath(self.file_path)
        self.pid = os.getpid()
        self.cmdline = " ".join(psutil.Process(self.pid).cmdline())
        
        current_file = os.path.abspath(__file__)
        self.current_dir = os.path.dirname(current_file)

    def create_file(self):
        prompt = input(f"""
-------------
Create a file
-------------
Enter the path to the file to create
Example: 'your/file/path/file.csv'
For reference your current directory is: {self.current_dir}
Or leave blank to create the file 'tmp/file.exe'
> """)
        
        if prompt:
            self.file_path = prompt
            self.full_path = os.path.abspath(self.file_path)
        
        try:
            with open(self.file_path, 'x') as _:
                timestamp = time.time()
                row=f"\n{timestamp},{self.username},{self.pid},,{self.cmdline},{self.full_path},create,,,"
                log_activity(row)
        except FileExistsError:
            print("File already exists")
        except Exception as e:
            print("Unable to create file with error:", e)

    def modify_file(self):
        if not os.path.exists(self.file_path):
            print(f"""
-----------
Modify file
-----------
Unable to modify file. Cannot find {self.file_path}""")
            return None

        prompt = input(f"""
-----------
Modify file
-----------
Modifying {self.file_path}
Enter the text you would like to replace the file contents
> """)
        try:
            with open(self.file_path, 'w') as file:
                file.write(prompt)
                timestamp = time.time()
                row=f"\n{timestamp},{self.username},{self.pid},,{self.cmdline},{self.full_path},modified,,,"
                log_activity(row)
        except Exception as e:
            print("Unable to modify file with error:", e)

    def delete_file(self):
        print(f"""
-------------
Deleting file
-------------
Deleting {self.file_path}
""")
        try:
            os.remove(self.file_path)
            timestamp = time.time()
            row=f"\n{timestamp},{self.username},{self.pid},,{self.cmdline},{self.full_path},delete,,,"
            log_activity(row)
        except Exception as e:
            print("Unable to delete file with error:", e)
        
