from client import Client
import json

class Player(Client):
    id_generator = 0

    def __init__(self, websocket):
        super(Player, self).__init__(websocket)

        self.socket = websocket
        self.id = self.id_generator
        self.id_generator += 1

    def __eq__(self, other):
        if isinstance(other, Player):
            return other.id == self.id

        return False

    def send_message(self, message):
        message_json = json.dumps(message)
        self.socket.send(message_json)
