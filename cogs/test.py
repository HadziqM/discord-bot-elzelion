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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ch = self.bot.get_channel(1006812758647521310)
        print(error)
        await ch.send(error)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('This command is on a %.2fs cooldown' % error.retry_after)
            raise error  # re-raise the error so all the errors will still show up in console


async def setup(bot):
    await bot.add_cog(GeneralCog(bot))
