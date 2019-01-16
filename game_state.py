import json
import requests

# store of games
all_games = {}

# constants
start_rules = {
    'shuffle_at': 0.5,
    'hit_soft_17': True,
    'unlimited_doubles': False,
    'deck_count': 6,
}

cards_in_deck = 52

# game models
class Game:
    def __init__(self, game_name, deck_id, **kwargs):
        # state of cards
        self.game_name = game_name
        self.deck_id = deck_id

        # state of players
        self.dealer_cards = []
        self.player_cards = []

        # game rules
        for rule, value in kwargs.items():
            start_rules[rule] = value
        self.rules = start_rules

        # tabulate remaining cards in decks and set the amount of cards at which the deck should be shuffled
        self.remaining = cards_in_deck * self.rules['deck_count']
        self.amount_before_shuffle = self.remaining * self.rules['shuffle_at']

    def check_shuffle(self):
        if self.remaining <= self.amount_before_shuffle:
            # todo: factor this call out to a separate method
            new_deck_json = requests.get(
                'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={}'
                    .format(self.rules['deck_count'])
            ).text
            new_deck = json.loads(new_deck_json)
            self.deck_id = new_deck['deck_id']
            return 'Deck has been shuffled!'
        else:
            return ''

    def deal(self):
        # shuffle the deck if you need to
        msg = self.check_shuffle()

        # get initial cards for dealer and player
        # todo: factor out to separate method
        new_cards_json = requests.get(
            'https://deckofcardsapi.com/api/deck/{}/draw/?count=3'
                .format(self.deck_id)
        ).text
        new_cards = json.loads(new_cards_json)

        # update the number of remaining cards
        self.remaining = new_cards['remaining']

        # give the first card to the dealer and the last two cards to the player
        self.dealer_cards = new_cards['cards'][:1]
        self.player_cards = new_cards['cards'][1:]

        return 'New cards have been dealt!' if not msg else msg + ' And new cards have been dealt!'

    def stand(self):
        return ''

    def hit(self):
        return ''

    def double(self):
        return ''

    def check_winner(self):
        return ''

