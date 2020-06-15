import random

from games.BlackJack.model import Player


class Deck:
    def __init__(self):
        self.card_faces = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.card_suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
        self.current_deck = self.create_deck()
        self.cards_taken = 0

    def create_deck(self):
        new_deck = []

        for card_suit in self.card_suits:
            for card_faces in self.card_faces:
                new_deck.append(card_faces + ' of ' + card_suit)

        return new_deck

    def shuffle_deck(self):
        self.cards_taken = 0
        random.shuffle(self.current_deck)

    def take_card(self):
        top_card = self.current_deck[self.cards_taken]
        self.cards_taken += 1
        return top_card

    def calculate_points(self, player: Player):
        current_points = 0

        for card in player.current_hand:
            if any(i in card[:2] for i in ('J', 'Q', 'K', '10')):
                current_points += 10
            elif 'Ace' in card[:3]:
                current_points += 1
            else:
                current_points += int(card[:1])

        return current_points
