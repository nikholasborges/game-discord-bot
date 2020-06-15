import discord
from discord.ext import commands, tasks

from games.BlackJack.controller.BlackJackController import BlackJackGame


class BlackJack(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.current_game = None
        self.current_player_turn = None

    # background task
    @tasks.loop(seconds=30)
    async def change_status(self):
        if self.current_game is not None:
            await self.client.change_presence(activity=discord.Game('BlackJack'))
        else:
            await self.client.change_presence(activity=discord.Game('Awating to play!'))

    # events listener
    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # commands listener
    @commands.command(name='blackjack')
    async def play_blackjack(self, ctx):
        if self.current_game is None:

            self.current_game = BlackJackGame()
            self.current_game.round()

            await ctx.send(f'your hand: {self.current_game.player.current_hand}')

        else:
            await ctx.send("There's a game currently running, await until it's over")

    # commands listener
    @commands.command(name='hit')
    async def hit(self, ctx):
        if self.current_game is not None:

            self.current_game.player_hit()

            await ctx.send(f'your hand: {self.current_game.player.current_hand}')

        else:
            await ctx.send("There isn't a game running, please start a new game!")

    # commands listener
    @commands.command(name='stay')
    async def stay(self, ctx):
        if self.current_game is not None:
            pass
        else:
            await ctx.send("There isn't a game running, please start a new game!")


def setup(client):
    client.add_cog(BlackJack(client))