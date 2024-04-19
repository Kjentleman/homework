import getpass
import http.client
import json
import os
import psutil
import ssl
import time
from logger import log_activity

class NetworkRunner:
    def __init__(self):
        self.username = getpass.getuser()
        self.pid = os.getpid()
        process = psutil.Process(self.pid)
        self.pname = process.name()
        self.cmdline = " ".join(process.cmdline())
    
    def transmit_data(self):
        host = 'jsonplaceholder.typicode.com'
        path = '/posts'
        headers = {
            "Content-type": "application/json; charset=UTF-8",
        }
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        conn = http.client.HTTPSConnection(host, context=context)
        body = json.dumps({
            "userId": 3,
            "title": "Lorem ipsum",
            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam nec suscipit erat. Ut ornare id turpis vel euismod. Vivamus tristique vehicula sapien, sed posuere nulla. Sed et mi a justo accumsan ultrices. Suspendisse faucibus in ex id cursus. Duis eget venenatis est. Maecenas scelerisque posuere lorem id porta. Nullam elit nulla, convallis eget nunc ut, facilisis lobortis quam. Integer vulputate sagittis nunc, placerat sollicitudin ipsum faucibus sed. Pellentesque vel augue non ipsum tempor fringilla et quis massa. Integer sit amet tristique ipsum. Nullam mattis viverra placerat. Sed efficitur pretium nisi sit amet consequat."
        })

        _ = input(f"""
TRANSMIT DATA
Transmitting data to '{host}{path}'
Enter to continue
> """)
        try:
            timestamp = time.time()
            conn.request("POST", path, body=body, headers=headers)
            sock = conn.sock
            local_address, local_port = sock.getsockname()

            row = f"\n{timestamp},{self.username},{self.pid},{self.pname},{self.cmdline},,,{local_address}:{local_port},{len(body)},HTTPS"
            log_activity(row)
            # response = conn.getresponse()
            # print(response.status)
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()
