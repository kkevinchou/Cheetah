import time
from websocket import create_connection

def basic_client():
    time.sleep(2)
    ws = create_connection("ws://127.0.0.1:8000")
    ws.send('{"type": "client_test", "message": "basic client message!"}')
    time.sleep(2)
    ws.close()

basic_client()