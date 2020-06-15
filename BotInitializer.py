import os
# import discord
from dotenv import load_dotenv
from discord.ext import commands

if __name__ == '__main__':
    load_dotenv()

    token = os.getenv('DISCORD_TOKEN')
    client = commands.Bot(os.getenv('BOT_DEFAULT_PREFIX'))

    @client.command()
    async def load(ctx, extension):
        client.load_extension(f'cogs.{extension}')

    @client.command()
    async def unload(ctx, extension):
        client.unload_extension(f'cogs.{extension}')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

    client.run(token)
