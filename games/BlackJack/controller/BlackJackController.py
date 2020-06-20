from ..model import Player
from ..model import Deck


class BlackJackGame:

    def __init__(self, context):
        self.deck = Deck.Deck()
        self.players = [Player.Player(100, 'dealer'), Player.Player(100, 'player')]
        self.current_player: Player = None
        self.dealer: Player = None
        self.round_deal = 15
        self.round_bet = 0
        self.rounds_played = 0
        self.ctx = context

    def debug(self):
        # debug
        print('-----------------------------------------------------')

        print(f'current deck: {self.deck.current_deck}')
        print(f'current bet: {self.round_bet}')

        for player in self.players:
            print(
                f'current {player.player_type} '
                f'money: {player.current_money} '
                f'current player hand: {player.current_hand}')
        print(f'next card: {self.deck.current_deck[self.deck.cards_taken]}')

        print('-----------------------------------------------------')
        print('')

    async def send_player_status(self, player: Player):
        # await ctx.send(f'  : { }')
        await self.ctx.send(f'round deal: ${self.round_deal}  '
                            f'/  round bet: ${self.round_bet}')

        await self.ctx.send(f'{player.player_type} ' f'hand: {player.current_hand}')
        await self.ctx.send(f'{player.player_type} 'f'points: {player.current_points}')

        if player.player_type == 'player':
            await self.ctx.send('press !hit to take one more card or !stay to keep your points...')
        self.debug()

    async def start_round(self):

        await self.ctx.send('--------  new round starting  --------')

        self.rounds_played += 1

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
                self.dealer = player

        await self.send_player_status(self.current_player)

        if self.current_player.current_points == 21:
            await self.ctx.send('BlackJack!!')
            await self.calculate_dealer_plays()

    # calculate the hit move
    async def player_hit(self, player: Player):

        if player.current_points <= 21:
            player.current_hand.append(self.deck.take_card())
            player.current_points = self.deck.calculate_points(player)
            await self.send_player_status(player)

            if player.current_points >= 21:
                await self.calculate_dealer_plays()
        else:
            await self.send_player_status(player)
            await self.calculate_dealer_plays()

    async def player_stay(self):
        await self.calculate_dealer_plays()

    # calculates dealer points
    async def calculate_dealer_plays(self):
        loop = True

        await self.ctx.send('--------  calculating dealer points  --------')
        await self.send_player_status(self.dealer)

        while loop:
            if self.dealer.current_points <= 17:
                # dealer hit
                self.dealer.current_hand.append(self.deck.take_card())
                self.dealer.current_points = self.deck.calculate_points(self.dealer)
                await self.send_player_status(self.dealer)
            else:
                # dealer stay
                loop = False
                await self.decide_round_winner()

    async def decide_round_winner(self):

        await self.ctx.send("--------  finalizing round  --------")

        player_points = self.current_player.current_points
        dealer_points = self.dealer.current_points

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

        await self.start_round()

    async def tie(self):
        await self.ctx.send("It's a tie!")
        await self.ctx.send(
            f'your points: {self.current_player.current_points}  '
            f'/  dealer points: {self.dealer.current_points}')
        await self.ctx.send(
            f'your current money is: ${self.current_player.current_money}  '
            f'/  dealer money: ${self.dealer.current_money}')

    async def player_won(self):
        await self.ctx.send(
            f'your points: {self.current_player.current_points}  '
            f'/  dealer points: {self.dealer.current_points}')
        await self.ctx.send(
            f'Great, you won... \n your current money is: ${self.current_player.current_money} '
            f' /  dealer money: ${self.dealer.current_money}')

        self.current_player.give_money(self.round_bet)

    async def player_lost(self):
        await self.ctx.send(
            f'your points: {self.current_player.current_points}  /  dealer points: {self.dealer.current_points}')
        await self.ctx.send(
            f'sorry, you lost... \n your current money is: ${self.current_player.current_money}  /  dealer money: ${self.dealer.current_money}')

        self.dealer.give_money(self.round_bet)
