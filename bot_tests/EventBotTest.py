import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands


class DiscordClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        load_dotenv()

        self.token = os.getenv('DISCORD_TOKEN')

    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == client.user:
            return

        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        if message.content == '99!':
            response = random.choice(brooklyn_99_quotes)
            await message.channel.send(response)


if __name__ == '__main__':
    client = DiscordClient()
    client.run(client.token)
