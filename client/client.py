from websocket import create_connection
ws = create_connection("ws://127.0.0.1:8000")
ws.send('{"type": "client_test", "field": "meep!"}')

import time
time.sleep(10)
data = ws.recv()
print data
ws.close()
