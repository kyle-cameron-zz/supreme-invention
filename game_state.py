# store of games
all_games = {}

# constants
start_rules = {
    'shuffle_at': 0.5,
    'hit_soft_17': True,
    'unlimited_doubles': False,
    'deck_count': 6,
}

# game models
class Game:
    def __init__(self, game_name, deck_id, **kwargs):
        # state of cards
        self.game_name = game_name
        self.deck_id = deck_id
        self.count = 0

        # state of players
        self.dealer_cards = []
        self.player_cards = []

        # game rules
        for rule, value in kwargs.items():
            start_rules[rule] = value
        self.rules = start_rules

# dealer functions
def dealer_hit():
    pass

def player_stand():
    pass

# player functions
def player_hit():
    pass

def player_stand():
    pass

def player_double():
    pass

def player_split():
    pass

def player_surrender():
    pass

# game functions
def check_winner():
    pass

def check_move():
    pass

def check_shuffle():
    pass

def reset_count():
    pass

def new_hand():
    pass

