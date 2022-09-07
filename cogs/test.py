import discord
from discord.ext import commands
from direc import *


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ready')
        a = 0
        for i in self.bot.guilds:
            print(f'run on {i.id} (name: {i.name})')
            a += 1
        print(f'elzelion in {a} guilds')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Hunter's Despair"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if 'elzelion self.bot' in message.content.lower():
            await message.channel.send('https://tenor.com/view/yes-i-am-yes-i-am-gif-4799231')
            return


def setup(bot):
    bot.add_cog(GeneralCog(bot))
