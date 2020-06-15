import discord
from discord.ext import commands, tasks


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # events listener
    @commands.Cog.listener()
    async def on_ready(self):
        print('GameCommands is online')
        await self.client.change_presence(activity=discord.Game('Awating to play!'))

    # commands listener
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send(f'my current ping is: {round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(Commands(client))
