import json
import random
import threading
import time

from gevent import pywsgi, sleep
from gevent.pool import Group
from geventwebsocket.handler import WebSocketHandler
from game.game import Game
from websocket import create_connection

SiNGLE_PLAYER = True

def client():
    time.sleep(2)
    ws = create_connection("ws://127.0.0.1:8000")
    ws.send('{"type": "client_test", "field": "meep!"}')
    time.sleep(2)
    ws.close()

class GameApp(object):
    next_player_id = 0

    def __init__(self, *args, **kwargs):
        self.game = Game(60)
        self.game_thread = threading.Thread(target=self.game.main)
        self.game_thread.daemon = True
        self.game_thread.start()

        if SiNGLE_PLAYER:
            self.client_thread = threading.Thread(target=client)
            self.client_thread.daemon = True
            self.client_thread.start()

    def __call__(self, environ, start_response):
        player_id = self.next_player_id
        self.next_player_id += 1

        websocket = environ['wsgi.websocket']

        player_connect_message = {
            'type': 'player_connect',
            'player_id': player_id,
            'websocket': websocket,
        }
        self.game.on_message(player_connect_message)

        while True:
            recv_data = websocket.receive()

            if recv_data is None:
                break

            message = json.loads(recv_data)
            message['player_id'] = player_id
            self.game.on_message(message)

        player_disconnect_message = {
            'type': 'player_disconnect',
            'player_id': player_id,
        }
        self.game.on_message(player_disconnect_message)

server = pywsgi.WSGIServer(("", 8000), GameApp(), handler_class=WebSocketHandler)
server.serve_forever()
