import discord
from discord.ext import commands, tasks


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # events listener
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
        await self.client.change_presence(activity=discord.Game('Awating to play!'))

    # commands listener
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send(f'my current ping is: {round(self.client.latency * 1000)}ms')

    @commands.command(name='clear')
    async def clear(self, ctx):
        current_channel = ctx.message.channel

        # checking the current amount of messages to delete
        messages = await current_channel.history(limit=None).flatten()

        # deleting messages from the channel
        await current_channel.purge(limit=len(messages))

        await ctx.send(f'Deleted {len(messages)} messages from this channel.')
        messages.clear()


def setup(client):
    client.add_cog(Commands(client))
