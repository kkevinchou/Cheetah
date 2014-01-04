from lib.player import Player as BasePlayer

class Player(BasePlayer):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.x = 0
        self.y = 0
    
