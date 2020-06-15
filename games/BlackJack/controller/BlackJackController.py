from ..model import Player
from ..model import Deck


class BlackJackGame:

    def __init__(self, context):
        self.deck = Deck.Deck()
        self.players = [Player.Player(100, 'dealer'), Player.Player(100, 'player')]
        self.current_player: Player = None
        self.current_dealer: Player = None
        self.round_deal = 5
        self.round_bet = 0
        self.rounds_played = 0
        self.ctx = context

    async def send_player_status(self):
        # await ctx.send(f'  : { }')
        await self.ctx.send(f'round deal: ${self.round_deal}  /  round bet: ${self.round_bet}')
        await self.ctx.send(f'your hand: {self.current_player.current_hand}')
        await self.ctx.send(f'your points: {self.current_player.current_points}')
        await self.ctx.send('press !hit to take one more card or !stay to keep your points...')

    def debug(self):
        # debug
        print('-----------------------------------------------------')
        print(f'current deck: {self.deck.current_deck}')
        print(f'current bet: {self.round_bet}')
        for player in self.players:
            print(
                f'current {player.player_type} money: {player.current_money} current player hand: {player.current_hand}')
        print(f'next card: {self.deck.current_deck[self.deck.cards_taken]}')
        print('-----------------------------------------------------')
        print('')

    async def start_round(self):

        await self.ctx.send('---new round starting---')

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

        self.debug()
        await self.send_player_status()

        if self.current_player.current_points == 21:
            await self.ctx.send('BlackJack!!')
            await self.calculate_dealer_plays()

    async def player_hit(self):
        if self.current_player.current_points <= 21:
            self.current_player.current_hand.append(self.deck.take_card())
            self.current_player.current_points = self.deck.calculate_points(self.current_player)
            self.debug()
            await self.send_player_status()

            if self.current_player.current_points >= 21:
                await self.calculate_dealer_plays()
        else:
            self.debug()
            await self.send_player_status()
            await self.calculate_dealer_plays()

    async def player_stay(self):
        await self.calculate_dealer_plays()

    async def calculate_dealer_plays(self):
        loop = True

        await self.ctx.send('calculating dealer points...')

        while loop:
            if self.current_dealer.current_points <= 17:
                # dealer hit
                self.current_dealer.current_hand.append(self.deck.take_card())
                self.current_dealer.current_points = self.deck.calculate_points(self.current_dealer)
                self.debug()
            else:
                # dealer stay
                loop = False
                await self.decide_round_winner()

    async def decide_round_winner(self):

        await self.ctx.send("--finalizing round---")

        player_points = self.current_player.current_points
        dealer_points = self.current_dealer.current_points

        if dealer_points > 21 and player_points > 21:
            await self.tie()
        elif player_points > 21:
            await self.player_lost()
        elif dealer_points > 21:
            await self.player_won()
        elif player_points > dealer_points:
            await self.player_won()
        elif dealer_points > player_points:
            await self.player_lost()
        else:
            await self.tie()

        self.debug()

        await self.start_round()

    async def tie(self):
        await self.ctx.send("It's a tie!")
        await self.ctx.send(f'your points: {self.current_player.current_points}  /  dealer points: {self.current_dealer.current_points}')

        await self.ctx.send(
            f'your current money is: ${self.current_player.current_money}  /  dealer money: ${self.current_dealer.current_money}')

    async def player_won(self):
        await self.ctx.send(
            f'your points: {self.current_player.current_points}  /  dealer points: {self.current_dealer.current_points}')

        self.current_player.give_money(self.round_bet)

        await self.ctx.send(
            f'Great, you won... \n your current money is: ${self.current_player.current_money}  /  dealer money: ${self.current_dealer.current_money}')

    async def player_lost(self):
        await self.ctx.send(
            f'your points: {self.current_player.current_points}  /  dealer points: {self.current_dealer.current_points}')

        self.current_dealer.give_money(self.round_bet)

        await self.ctx.send(
            f'sorry, you lost... \n your current money is: ${self.current_player.current_money}  /  dealer money: ${self.current_dealer.current_money}')
