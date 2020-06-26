import discord
from discord.ext import commands, tasks

from context.MongoPosts import UserPost


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

    @commands.command(name='register')
    async def register(self, ctx):
        current_author = str(ctx.author)
        author_id = current_author[current_author.find('#'):]

        for user in UserPost.objects(user_name=author_id):

            if not author_id == user.user_name:
                post = UserPost(user_name=author_id)
                post.save()
                await ctx.send('Registrado com sucesso')
            else:
                await ctx.send('Seu usuário já está cadastrado.')

    @commands.command(name='profile')
    async def profile(self, ctx):
        current_author = str(ctx.author)
        author_id = current_author[current_author.find('#'):]
        author_name = current_author[:current_author.find('#')]

        for user in UserPost.objects(user_name=author_id):

            if author_id == user.user_name:
                await ctx.send(f'Id: {user.user_name}')
                await ctx.send(f'Nome: {author_name}')
                await ctx.send(f'Dinheiro: ${user.user_money}')
                await ctx.send(f'Partidas Ganhas: {user.user_games_won}')
            else:
                await ctx.send('Você ainda não está cadastrado!')


def setup(client):
    client.add_cog(Commands(client))
