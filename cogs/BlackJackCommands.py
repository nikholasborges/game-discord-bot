import discord
from discord.ext import commands, tasks
from Util import Validator
from context.UserContext import UserContext
from games.BlackJack.controller.BlackJackController import BlackJackGame


current_game = None


class BlackJack(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.current_user_playing = None

    # background task
    @tasks.loop(seconds=30)
    async def change_status(self):
        pass

    # events listener
    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # commands listener
    @commands.command(name='blackjack')
    async def play_blackjack(self, ctx, *args):
        global current_game

        # TODO: better code this decision logic

        author_id = str(ctx.author)[str(ctx.author).find('#'):]
        user_context = UserContext(author_id)

        if user_context.user_doc is None:
            embed = discord.Embed(description=f"current user isn't registered {ctx.author} \n"
                                              f"You must register in order to play any game <!register>")
            await ctx.send(embed=embed)
            return

        if current_game is not None:
            embed = discord.Embed(
                description=f"there's a game running played by {self.current_user_playing}")
            await ctx.send(embed=embed)
        else:
            if len(args) > 1:
                embed = discord.Embed(
                    description=f'!blackjack command only accept number as argument like: !blackjack 20')
                await ctx.send(embed=embed)
                return

            if len(args) == 0:
                embed = discord.Embed(
                    description=f'Bet value was not decided, please set a bet value like: !blackjack <Bet Value>')
                await ctx.send(embed=embed)
                return

            if Validator.valid_int(args[0]):
                money = float(args[0])
                user_id = str(ctx.author)[str(ctx.author).find('#'):]

                # Validate if the money choosen to bet is less than the minimum allowed
                if money < 25:
                    embed = discord.Embed(
                        description=f'Value choosen to bet ${money} is lower than the minimun required $25 \n'
                                    f'The value that will be used to bet will be $25')
                    await ctx.send(embed=embed)
                    money = 25

                # Validate if the money choosen to bet is more the user actually have
                if user_context.user_money - money < 0:
                    embed = discord.Embed(
                        description=f'Value choosen to bet ${money} is more than your current money ${user_context.user_money}')
                    await ctx.send(embed=embed)
                    return

                user_context.retrieve_money(money)
                current_game = BlackJackGame(ctx, money, user_id)
                self.current_user_playing = ctx.author
                await current_game.start_round()

    # commands listener
    @commands.command(name='hit')
    async def hit(self, ctx):
        global current_game

        if current_game is not None:

            if ctx.author == self.current_user_playing:
                await current_game.player_hit()
            else:
                embed = discord.Embed(description=f"There's a game currently running for {self.current_user_playing}")
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description="There isn't a game running right now.")
            await ctx.send(embed=embed)

    # commands listener
    @commands.command(name='stay')
    async def stay(self, ctx):
        global current_game

        if current_game is not None:
            await current_game.player_stay()
        else:
            embed = discord.Embed(description="There isn't a game running right now.")
            await ctx.send(embed=embed)

    # commands listener
    @commands.command(name='end_game')
    async def end_game(self, ctx):
        global current_game

        if current_game is not None:
            await current_game.end_game()
            embed = discord.Embed(description="Game Finalized.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="There isn't a game running right now.")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(BlackJack(client))
