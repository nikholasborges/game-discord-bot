import discord
from discord.ext import commands, tasks

from games.BlackJack.controller.BlackJackController import BlackJackGame


class BlackJack(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.current_game = None
        self.current_user_playing = None

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

            self.current_game = BlackJackGame(ctx)
            self.current_user_playing = ctx.author
            await self.current_game.start_round()

        else:
            await ctx.send(f'tem gente jogando porra, tá pancado!? espera o {self.current_user_playing} terminar')

    # commands listener
    @commands.command(name='hit')
    async def hit(self, ctx):
        if self.current_game is not None:

            if ctx.author == self.current_user_playing:
                await self.current_game.player_hit()
            else:
                print(f'tem gente jogando porra, tá pancado!? espera o {self.current_user_playing} terminar')

        else:
            await ctx.send("Como que tu quer dar !hit sem começar um game?! da um !blackjack pra começar doidão")

    # commands listener
    @commands.command(name='stay')
    async def stay(self, ctx):
        if self.current_game is not None:

            await self.current_game.player_stay()

        else:
            await ctx.send("Como que tu quer dar !stay sem começar um game?! da um !blackjack pra começar doidão")

    # commands listener
    @commands.command(name='end_game')
    async def end_game(self, ctx):
        if self.current_game is not None:

            self.current_game = None
            await ctx.send("Game finalized!")

        else:
            await ctx.send("Que jogo tu quer terminar se não tem nenhum rodando? maior burrão, da um !blackjack ai")


def setup(client):
    client.add_cog(BlackJack(client))