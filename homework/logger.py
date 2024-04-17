
import os

def init_activity_log():
    with open('logs/activity_log.csv', 'x') as file:
        file.write('timestamp,username,pid,process_name,command_line,file_path,descriptor,source,payload,protocol')

def get_last_activity():
    if not os.path.exists('logs/activity_log.csv'):
         return None
    # load second to last byte then seek backwards until we find a newline
    with open('logs/activity_log.csv', 'rb') as file:
        file.seek(-2, 2)
        while file.read(1) != b'\n':
            file.seek(-2,1)
        return file.readline().decode()

def log_activity(row):
    if not os.path.exists('logs/activity_log.csv'):
        init_activity_log()
    with open('logs/activity_log.csv', 'a') as file:
        file.write(row)