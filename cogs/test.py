import discord
from discord.ext import commands
from direc import *
from base import *


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
        elif message.guild is None:
            a = message.content
            b = message.author
            c = message.author.id
            channel = self.bot.get_channel(1000712069965938759)
            if str(message.attachments) == '[]':
                await channel.send(b)
                await channel.send(c)
                await channel.send(a)
                return None
            else:
                set_up()
                ck = check_disc(c)
                char = character(ck)
                ch2 = self.bot.get_channel(1000724348044329050)
                b = message.author
                channel = self.bot.get_channel(1000712069965938759)
                filename = message.attachments[0].filename
                size = message.attachments[0].size
                t_file = ['savedata', 'decomyset', 'partner', 'hunternavi', 'otomoairou', 'platebox',
                          'platedata', 'platemyset', 'rengokudata', 'savemercenary', 'skin_hist']
                s_file = [i+'_rain.bin' for i in t_file]
                if filename in s_file:
                    if size >= 1000:
                        await b.send("dont send someting malicius please")
                    else:
                        await channel.send(message.attachments[0].url)
                    order = s_file.index(filename)
                    await message.attachments[0].save(fp=f'{UPLOAD_PATH}\\{t_file[order]}_{ck}.bin')
                    char.upload_data(t_file[order])
                    await b.send(f'uploaded {char.name} {t_file[order]} to server')
                    await ch2.send(f'{b} {t_file[order]} downloaded')
                else:
                    await channel.send(b)
                    for i in message.attachments:
                        await channel.send(i.url)

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
