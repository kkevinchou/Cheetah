from lib.ecs.entity.entity import Entity
from lib.ecs.component.cnetworkplayer import CNetworkPlayer

class Player(Entity):
    def __init__(self, player_id, socket):
    	super(Player, self).__init__()
        self.id = player_id

        self.add_component(CNetworkPlayer(socket))

    def __eq__(self, other):
        if isinstance(other, Player):
            return other.id == self.id

        return False
