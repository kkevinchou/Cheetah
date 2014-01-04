import time
from Queue import Queue
from player import Player
from lib.game import Game as BaseGame

class Game(BaseGame):
    def __init__(self, fps):
        super(Game, self).__init__(fps)

        self.in_messages = Queue()
        self.players = {}

    def on_message(self, message):
        message['timestamp'] = time.time()
    	player_id = message['player_id']
    	self.players[player_id].send_message(message)
        self.in_messages.put(message)

    def _safe_get_in_message(self):
        try:
            message = self.in_messages.get(block=False)
        except:
            message = None

        return message

    def update(self, delta):
        current_time = time.time()

        message = self._safe_get_in_message()
        while message is not None:
            print message
            message = self._safe_get_in_message()

    def render(self):
        pass

        # message = {
        #     'timestamp': time.time(),
        #     'render': 'render'
        # }
        # for player_id, player in self.players.iteritems():
        #     player.send_message(message)
