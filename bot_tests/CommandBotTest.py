import os
import random
# import discord
from dotenv import load_dotenv
from discord.ext import commands


def command_bot():
    load_dotenv()

    token = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(os.getenv('BOT_PREFIX'))

    @bot.command(name='roll_dice', help='roll a dice')
    async def roll(ctx):
        number_of_sides = 6
        dice = str(random.choice(range(1, number_of_sides + 1)))

        response = 'dice result: {}'.format(dice)
        await ctx.send(response)

    bot.run(token)


if __name__ == '__main__':
    command_bot()