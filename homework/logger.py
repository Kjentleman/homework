
import os

log_file_path = 'logs/activity_log.csv'

def init_activity_log():
    with open(log_file_path, 'x') as file:
        file.write('timestamp,username,pid,process_name,command_line,file_path,descriptor,source,payload,protocol')

def get_last_activity():
    if not os.path.exists(log_file_path):
         return None
    # load second to last byte then seek backwards until we find a newline
    with open(log_file_path, 'rb') as file:
        file.seek(-2, 2)
        while file.read(1) != b'\n':
            file.seek(-2,1)
        return file.readline().decode()

def log_activity(row):
    if not os.path.exists(log_file_path):
        init_activity_log()
    with open(log_file_path, 'a') as file:
        file.write(row)