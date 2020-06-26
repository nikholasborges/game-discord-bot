import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

from context.MongoPosts import UserPost


class Commands(commands.Cog):

    def __init__(self, bot_obj):
        load_dotenv()
        self.bot = bot_obj

    # events listener
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
        await self.bot.change_presence(activity=discord.Game('Awating to play!'))

    # commands listener
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send(f'my current ping is: {round(self.bot.latency * 1000)}ms')

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

        print(current_author)
        print(author_id)

        for user in UserPost.objects():

            if not author_id == user.user_name or user is None:
                post = UserPost(user_name=author_id)
                post.save()
                await ctx.send('Registrado com sucesso')
            else:
                await ctx.send('Seu usuário já está cadastrado.')

    @commands.command(name='profile')
    async def profile(self, ctx):

        converter = commands.MemberConverter()
        author_obj = await converter.convert(ctx, str(ctx.author))  # get the author obj
        embed = discord.Embed(title='Profile', colour=discord.Colour.blue())

        author_id = str(ctx.author)[str(ctx.author).find('#'):]
        author_name = str(ctx.author)[:str(ctx.author).find('#')]
        author_avatar = author_obj.avatar_url

        for user in UserPost.objects():

            if author_id == user.user_name:
                embed.set_author(name=author_name, icon_url=author_avatar)
                embed.set_thumbnail(url=author_avatar)
                embed.add_field(name='Dinheiro', value=f'$ {str(user.user_money)}', inline=False)
                embed.add_field(name='Rodadas Ganhas', value=user.user_games_won, inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send('Você ainda não está cadastrado!')


def setup(client):
    client.add_cog(Commands(client))
