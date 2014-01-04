# import sys
# import os
# sys.path.append(os.getcwd())
# print sys.path

import json
import random
import threading

from gevent import pywsgi, sleep
from gevent.pool import Group
from geventwebsocket.handler import WebSocketHandler
from game.game import Game
import json

class GameApp(object):
    next_client_id = 0

    def __init__(self, *args, **kwargs):
        self.game = Game(60)
        self.game_thread = threading.Thread(target=self.game.main)
        self.game_thread.daemon = True
        self.game_thread.start()

    def __call__(self, environ, start_response):
        client_id = next_client_id
        next_client_id += 1

        websocket = environ['wsgi.websocket']

        client_connect_message = {
            'type': 'client_connect',
            'client_id': client_id,
            'websocket': websocket,
        }
        self.game.on_message(client_connect_message)

        while True:
            recv_data = websocket.receive()

            if recv_data is None:
                break

            message = json.loads(recv_data)
            message['player_id'] = player_id
            self.game.on_message(message_dict)

        client_disconnect_message = {
            'type': 'client_disconnect',
            'client_id': client_id,
        }
        self.game.on_message(client_connect_message)

server = pywsgi.WSGIServer(("", 8000), GameApp(), handler_class=WebSocketHandler)
server.serve_forever()