import discord

from ..model import Player
from ..model import Deck


class BlackJackGame:

    def __init__(self, context):
        self.deck = Deck.Deck()
        self.players = [Player.Player(100, 'dealer'), Player.Player(100, 'player')]
        self.current_player = None
        self.dealer = None
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
        embed_color = discord.Colour.red()

        if player.player_type == 'player':
            embed_color = discord.Colour.blue()

        embed = discord.Embed(title=f'Round {self.rounds_played}', colour=embed_color)

        embed.set_author(name=f'{player.player_type} turn'.upper())

        embed.add_field(name='Round Deal', value=f'$ {str(self.round_deal)}', inline=True)
        embed.add_field(name='Round Bet', value=f'$ {str(self.round_bet)}', inline=True)

        embed.add_field(name='Hand', value=player.current_hand, inline=False)
        embed.add_field(name='Points', value=str(player.current_points), inline=True)

        await self.ctx.send(embed=embed)

        self.debug()

    async def end_round(self, status):

        message = {'won': 'Great, you won!',
                   'lost': 'Sorry, you lost!',
                   'tie': "It's a tie!"}

        if status == 'won':
            self.current_player.give_money(self.round_bet)
        elif status == 'lost':
            self.dealer.give_money(self.round_bet)

        embed = discord.Embed(title=f'{message[status]}',
                              description=f'Round {self.rounds_played}',
                              colour=discord.Colour.green())

        embed.add_field(name='Your Points', value=f'{self.current_player.current_points}', inline=True)
        embed.add_field(name='Dealer Points', value=f'{self.dealer.current_points}', inline=True)

        embed.add_field(name='Your current Money', value=f'${self.current_player.current_money}', inline=False)
        embed.add_field(name='Dealer Money', value=f'${self.dealer.current_money}', inline=True)

        await self.ctx.send(embed=embed)

    async def start_round(self):

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
            await self.calculate_dealer_plays()

    # calculate the hit move
    async def player_hit(self, player=None):

        if player is None:
            player = self.current_player

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

        player_points = self.current_player.current_points
        dealer_points = self.dealer.current_points

        # TODO: Better code this decision logic

        if dealer_points > 21 and player_points > 21:
            await self.end_round('tie')
        elif player_points > 21:
            await self.end_round('lost')
        elif dealer_points > 21:
            await self.end_round('won')
        elif player_points > dealer_points:
            await self.end_round('won')
        elif dealer_points > player_points:
            await self.end_round('lost')
        else:
            await self.end_round('tie')

        await self.start_round()
