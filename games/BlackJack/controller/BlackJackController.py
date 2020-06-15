from ..model import Player
from ..model import Deck


class BlackJackGame:

    def __init__(self):
        self.deck = Deck.Deck()
        self.dealer = Player.Player(100, 'dealer')
        self.player = Player.Player(100, 'player')
        self.round_deal = 5
        self.round_bet = 0

    def round(self):
        self.deck.shuffle_deck()
        self.round_bet += self.dealer.retrieve_money(self.round_deal)
        self.round_bet += self.player.retrieve_money(self.round_deal)

        index = 0

        while index < 2:
            self.dealer.current_hand.append(self.deck.take_card())
            self.player.current_hand.append(self.deck.take_card())
            index += 1

        # debug
        print(f'current deck: {self.deck.current_deck}')
        print(f'current deck quantity: {len(self.deck.current_deck)}')

        print(f'current bet: {self.round_bet}')
        print(f'current dealer money: {self.dealer.current_money} \n current dealer hand: {self.dealer.current_hand}')
        print(f'current player money: {self.player.current_money} \n current player hand: {self.player.current_hand}')

    def player_hit(self):
        self.player.current_hand.append(self.deck.take_card())
