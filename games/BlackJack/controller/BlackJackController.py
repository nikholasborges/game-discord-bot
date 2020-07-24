import asyncio

import discord

from Util import MoneyParser
from cogs.BlackJackCommands import BlackJackCommands
from context.UserContext import UserContext
from ..model import Player
from ..model import Deck


class BlackJackGame:

    def __init__(self, context, player_money, user_id):
        self.deck = Deck.Deck()
        self.player_bet_money = player_money
        self.players = [Player.Player(MoneyParser.dealer_money_parser(player_money), 'dealer'),
                        Player.Player(player_money, 'player')]
        self.current_player_id = user_id
        self.current_player = None
        self.dealer = None
        self.round_bet = MoneyParser.round_deal_parser(player_money)
        self.round_amount = 0
        self.rounds_played = 0
        self.ctx = context

    def debug(self):
        # debug
        print('-----------------------------------------------------')

        print(f'current deck: {self.deck.current_deck}')
        print(f'current bet: {self.round_amount}')

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

        embed_round = discord.Embed(title=f'Round {self.rounds_played}', colour=embed_color)

        embed_round.set_author(name=f'{player.player_type} turn'.upper())
        embed_round.add_field(name='Round Bet', value=f'$ {self.round_bet:.2f}', inline=True)
        embed_round.add_field(name='Round Amount', value=f'$ {self.round_amount:.2f}', inline=True)
        embed_round.add_field(name='Hand', value=player.current_hand, inline=False)
        embed_round.add_field(name='Points', value=str(player.current_points), inline=True)

        await asyncio.sleep(0.5)
        await self.ctx.send(embed=embed_round)

        self.debug()

    async def start_round(self):

        # checking if the players still have money to gamble
        if self.dealer is not None:
            if self.dealer.current_money <= 0 or self.dealer.current_money - self.round_bet <= 0:
                embed = discord.Embed(
                    title='You won the game!',
                    description=f"The dealear don't have more money to gamble, the game will be finalized",
                    color=discord.Colour.gold())
                await self.ctx.send(embed=embed)
                await self.end_game()
                return

        if self.current_player is not None:
            if self.current_player.current_money <= 0 or self.current_player.current_money - self.round_bet <= 0:
                embed = discord.Embed(
                    title='You lost the game!',
                    description=f"You don't have more money to gamble, the game will be finalized",
                    color=discord.Colour.gold())
                await self.ctx.send(embed=embed)
                await self.end_game()
                return

        # shuffle deck and set overall game status
        self.deck.shuffle_deck()
        self.round_amount = 0
        self.rounds_played += 1

        for player in self.players:
            # refresh player points and hand
            index = 0
            player.flush_hand()

            # retrive player money and place in the round_bet
            self.round_amount += player.retrieve_money(self.round_bet)

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

        # send players money status [single player only]
        embed_money = discord.Embed(title=f'Round {self.rounds_played}', colour=discord.Colour.green())

        embed_money.add_field(name='Your Money', value=f'${self.current_player.current_money:.2f}', inline=True)
        embed_money.add_field(name='Dealer Money', value=f'${self.dealer.current_money:.2f}', inline=True)

        await self.ctx.send(embed=embed_money)

        # send current player status
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

    async def end_round(self, status):

        message = {'won': 'Great, you won!',
                   'lost': 'Sorry, you lost!',
                   'tie': "It's a tie!"}

        if status == 'won':
            self.current_player.give_money(self.round_amount)
        elif status == 'lost':
            self.dealer.give_money(self.round_amount)
        else:
            round_bet_splitted = self.round_amount / len(self.players)
            self.current_player.give_money(round_bet_splitted)
            self.dealer.give_money(round_bet_splitted)

        embed = discord.Embed(title=f'{message[status]}',
                              description=f'Round {self.rounds_played}',
                              colour=discord.Colour.green())

        embed.add_field(name='Your Points', value=f'{self.current_player.current_points}', inline=True)
        embed.add_field(name='Dealer Points', value=f'{self.dealer.current_points}', inline=True)
        embed.add_field(name='Your Money', value=f'${self.current_player.current_money:.2f}', inline=False)
        embed.add_field(name='Dealer Money', value=f'${self.dealer.current_money:.2f}', inline=True)

        await asyncio.sleep(0.5)
        await self.ctx.send(embed=embed)

    async def end_game(self):

        user_context = UserContext(self.current_player_id)
        user_context.receive_money(self.current_player.current_money)

        amount_earned = self.current_player.current_money - self.player_bet_money

        if amount_earned > 0:
            embed = discord.Embed(title=f'Amount earned: ${amount_earned:.2f}', color=discord.Colour.gold())
            await self.ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'You lost: ${amount_earned:.2f}', color=discord.Colour.gold())
            await self.ctx.send(embed=embed)

        # TODO: better code this global game finalized logic
        BlackJackCommands.current_game = None
