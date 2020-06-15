class Player:

    def __init__(self, initial_money, player_type):
        self.current_money = initial_money
        self.current_hand = []
        self.current_points = 0
        self.player_type = player_type

    def initial_hand(self, cards):
        if len(self.current_hand) == 0:
            for card in cards:
                self.current_hand.append(card)

    def add_card(self, card):
        self.current_hand.append(card)

    def flush_hand(self):
        self.current_hand = []
        self.current_points = 0

    def give_money(self, value):
        if not value < 0:
            self.current_money += value

    def retrieve_money(self, value):
        if not value < 0:
            self.current_money -= value

        return value
