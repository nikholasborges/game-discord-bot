import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

from context.MongoPosts import UserPost
from context.UserContext import UserContext


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
    async def profile(self, ctx, *member: discord.Member):

        if len(member) > 0:
            user_obj = member[0]
        else:
            user_obj = await commands.MemberConverter().convert(ctx, str(ctx.author))  # get the author obj

        user_id = str(user_obj)[str(user_obj).find('#'):]
        user_name = str(user_obj)[:str(user_obj).find('#')]
        user_context = UserContext(user_id).user_obj
        user_avatar = user_obj.avatar_url

        embed = discord.Embed(title='Profile', colour=discord.Colour.blue())

        if user_context is not None:
            embed.set_author(name=user_name, icon_url=user_avatar)
            embed.set_thumbnail(url=user_avatar)
            embed.add_field(name='Dinheiro', value=f'$ {str(user_context.user_money)}', inline=False)
            embed.add_field(name='Rodadas Ganhas', value=user_context.user_games_won, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'{user_obj.nick} ainda não está cadastrado!')

    # command for testing purposes
    @commands.command(name='give_money')
    async def give_money(self, ctx, member: discord.Member, value):
        if member is not None:
            member_id = str(member)[str(member).find('#'):]
            result = UserContext(member_id).receive_money(float(value))

            if result:
                embed = discord.Embed(description=f'User {member} received ${float(value)} sucessfully!',
                                      colour=discord.Colour.green())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'User did not received the money correctly',
                                      colour=discord.Colour.red())
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
