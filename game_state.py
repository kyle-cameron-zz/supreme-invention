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

card_values = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'JACK': 10,
    'QUEEN': 10,
    'KING': 10,
}

ace_values = (1, 11)
black_jack = 21
dealer_hit_until = 17


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
        [player_val, dealer_val] = self.check_values()
        if player_val > black_jack:
            return 'You went bust. Dealer wins.'
        elif dealer_val < 17:
            # give dealer another card
            new_cards_json = requests.get(
                'https://deckofcardsapi.com/api/deck/{}/draw/?count=1'
                    .format(self.deck_id)
            ).text
            new_cards = json.loads(new_cards_json)

            # update the number of remaining cards
            self.remaining = new_cards['remaining']

            # give the new card to the dealer
            self.dealer_cards.append(new_cards['cards'][0])
            return self.stand()
        else:
            return self.check_winner()

    def hit(self):
        [player_val, dealer_val] = self.check_values()
        if player_val > black_jack:
            return 'You went bust. Dealer wins.'
        else:
            # give player another card
            new_cards_json = requests.get(
                'https://deckofcardsapi.com/api/deck/{}/draw/?count=1'
                    .format(self.deck_id)
            ).text
            new_cards = json.loads(new_cards_json)

            # update the number of remaining cards
            self.remaining = new_cards['remaining']

            # give the new card to the dealer
            self.player_cards.append(new_cards['cards'][0])
            return 'You have hit!'

    def double(self):
        [player_val, dealer_val] = self.check_values()
        if player_val > black_jack:
            return 'You went bust. Dealer wins.'
        else:
            # give player another card
            new_cards_json = requests.get(
                'https://deckofcardsapi.com/api/deck/{}/draw/?count=1'
                    .format(self.deck_id)
            ).text
            new_cards = json.loads(new_cards_json)

            # update the number of remaining cards
            self.remaining = new_cards['remaining']

            # give the new card to the player
            self.player_cards.append(new_cards['cards'][0])
            return self.stand()

    def check_winner(self):
        [player, dealer] = self.check_values()
        if player == dealer:
            return 'Both you and the dealer have a {}, resulting in a push.'.format(player)
        elif player > 21:
            return 'You went bust. Dealer wins.'
        elif dealer > 21:
            return 'The dealer went bust. You win with a {}.'.format(player)
        elif player > dealer:
            return 'You win with a {} over the dealer\'s {}.'.format(player, dealer)
        elif dealer > player:
            return 'The dealer wins with a {} over your {}.'.format(player, dealer)

    def check_values(self):
        # todo: make this function more DRY
        player_values = [0]
        for card in self.player_cards:
            if card['value'] == 'ACE':
                # duplicate the current list
                player_values *= 2
                # add 1 to the first half of the list and add 11 to the second half of the list
                player_values = list(map(lambda x: x + ace_values[0], player_values[:len(player_values) / 2])) + \
                                list(map(lambda x: x + ace_values[1], player_values[len(player_values) / 2:]))
            else:
                print('here card = ', card)
                print('here card[value] = ', card['value'])
                player_values = list(map(lambda x: x + card_values[card['value']], player_values))

        dealer_values = [0]
        for card in self.dealer_cards:
            if card['value'] == 'ACE':
                # duplicate the current list
                dealer_values *= 2
                # add 1 to the first half of the list and add 11 to the second half of the list
                dealer_values = list(map(lambda x: x + ace_values[0], dealer_values[:len(dealer_values) / 2])) + \
                                list(map(lambda x: x + ace_values[1], dealer_values[len(dealer_values) / 2:]))
            else:
                dealer_values = list(map(lambda x: x + card_values[card['value']], dealer_values))

        player_value = min(player_values) if all(x > black_jack for x in player_values) \
            else max(x for x in player_values if x <= black_jack)
        dealer_value = min(dealer_values) if all(x > black_jack for x in dealer_values) \
            else max(x for x in dealer_values if x <= black_jack)

        return [player_value, dealer_value]
