import time
from Queue import Queue
from ecs.entity.player import Player
from lib.game import Game as BaseGame

from lib.ecs.component.cnetworkplayer import CNetworkPlayer

ECHO_IGNORED_MESSAGE_TYPES = ['player_connect', 'player_disconnect']

class Game(BaseGame):
    def __init__(self, fps):
        super(Game, self).__init__(fps)

        player = Player(1, 1)
        self.in_messages = Queue()
        self.players = {}

    def on_message(self, message):
        message['timestamp'] = time.time()

        if 'player_id' in message:
            print '[Player {}] Received message: {}'.format(message['player_id'], message)

        self.in_messages.put(message)

    def _safe_get_in_message(self):
        try:
            message = self.in_messages.get(block=False)
        except:
            message = None

        return message

    def update(self, delta):
        current_timestamp = time.time()
        message = self._safe_get_in_message()
        
        # TODO: requeue a message that is not None but does not fulfill the timestamp requirement
        while message is not None:
            self.handle_message(message)
            message = self._safe_get_in_message()

    def handle_message(self, message):
        if message['type'] == 'player_connect':
            player = Player(
                message['player_id'],
                message['websocket'],
            )
            self.players[player.id] = player

        if message['type'] not in ECHO_IGNORED_MESSAGE_TYPES:
            player = self.players[message['player_id']]
            network_component = player.get_component(CNetworkPlayer.component_id)
            network_component.send_message(message)

    def render(self):
        pass

        # message = {
        #     'timestamp': time.time(),
        #     'render': 'render'
        # }
        # for player_id, player in self.players.iteritems():
        #     player.send_message(message)
