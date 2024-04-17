from exe_runner import ExeRunner
from file_runner import FileRunner

# Run executable
exer = ExeRunner()
exer.prompt()
exer.run_exe()

# Create, modify, and delete file
filer = FileRunner()
filer.create_file()
filer.modify_file()
filer.delete_file()

# Tranmit data over network connection