from ..model import Player
from ..model import Deck


class BlackJackGame:

    def __init__(self):
        self.deck = Deck.Deck()
        self.players = [Player.Player(100, 'dealer'), Player.Player(100, 'player')]
        self.current_player = None
        self.current_dealer = None
        self.round_deal = 5
        self.round_bet = 0
        self.rounds_played = 0

    def start_round(self):

        # shuffle deck and set overall game status
        self.deck.shuffle_deck()
        self.round_bet = 0
        self.rounds_played += 1

        for player in self.players:
            # refresh player points and hand
            index = 0
            player.flush_hand()

            # retrive player money and place in the round_bet
            self.round_bet += player.retrieve_money(self.round_deal)

            # load player hand with the 2 starting cards
            while index < 2:
                player.current_hand.append(self.deck.take_card())
                index += 1

            # calculate player inicial points
            player.current_points = self.deck.calculate_points(player)

            # separate normal player and dealer player
            if player.player_type == 'player':
                self.current_player = player
            else:
                self.current_dealer = player

        # debug
        print(f'current deck: {self.deck.current_deck}')
        print(f'current deck quantity: {len(self.deck.current_deck)}')
        print(f'current bet: {self.round_bet}')
        for player in self.players:
            print(f'current {player.player_type} money: {player.current_money} current player hand: {player.current_hand}')

    def player_hit(self):
        self.current_player.current_hand.append(self.deck.take_card())
        self.current_player.current_points = self.deck.calculate_points(self.current_player)

    def player_stay(self):
        pass

    def calculate_dealer_plays(self):
        pass
