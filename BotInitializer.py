import os
# import discord
from dotenv import load_dotenv
from discord.ext import commands

if __name__ == '__main__':
    load_dotenv()

    token = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(os.getenv('BOT_DEFAULT_PREFIX'))

    @bot.command()
    async def load(ctx, extension):
        bot.load_extension(f'cogs.{extension}')

    @bot.command()
    async def unload(ctx, extension):
        bot.unload_extension(f'cogs.{extension}')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    bot.run(token)
