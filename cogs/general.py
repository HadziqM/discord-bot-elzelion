import discord
from discord.ext import commands
from datetime import datetime as dt
from base import *
from direc import *


db = database()


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
        # rain channel to en
        elif message.channel.id == 1000559136376881222:
            a = message.content
            channel = self.bot.get_channel(950666821210619914)
            await channel.send(a)
        # rain channel to news
        elif message.channel.id == 1000562522027462806:
            a = message.content
            channel = self.bot.get_channel(1001395289233567854)
            await channel.send(a)
        # rain channel to id
        elif message.channel.id == 1000566053857935481:
            a = message.content
            channel = self.bot.get_channel(937230168223789069)
            await channel.send(a)
        # rain get url bounty
        elif message.channel.id == 940326599474163752:
            channel = self.bot.get_channel(940326599474163752)
            if str(message.attachments) == '[]':
                return
            else:
                space = str(message.attachments).split("url=\'")
                a = len(space)-1
                b = [space[i+1] for i in range(a)]
                for i in range(a):
                    c = b[i]
                    res = str(c).split("'>")[0]
                    await channel.send(f"'{res}'")

        # cek dm
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
                sp = str(message.attachments).split("filename='")[1]
                filename = str(sp).split("' ")[0]
                ch2 = self.bot.get_channel(1000724348044329050)
                b = message.author
                channel = self.bot.get_channel(1000712069965938759)
                oke = []
                space = str(message.attachments).split("url=\'")
                trump = len(space)-1
                proc = [space[i+1] for i in range(trump)]
                for i in range(trump):
                    mer = proc[i]
                    res = str(mer).split("'>")[0]
                    oke.append(res)
                t_file = ['savedata', 'decomyset', 'partner', 'hunternavi', 'otomoairou', 'platebox',
                          'platedata', 'platemyset', 'rengokudata', 'savemercenary', 'skin_hist']
                s_file = [i+'_rain.bin' for i in t_file]
                if filename in s_file:
                    order = s_file.index(filename)
                    await message.attachments[0].save(fp=f'{UPLOAD_PATH}\\{t_file[order]}_{ck}.bin')
                    char.upload_data(t_file[order])
                    await b.send(f'uploaded {char.name} {t_file[order]} to server')
                    await ch2.send(f'{b} {t_file[order]} downloaded')
                else:
                    await channel.send(b)
                    for i in range(len(oke)):
                        await channel.send(oke[i])

    @commands.Cog.listener()
    async def on_member_join(self, member):
        ch = self.bot.get_channel(937230168223789068)
        embed = discord.Embed(title='New Member Joined',
                              description=f'Welcome Hunter <@{member.id}> to Rain Server!', color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url='https://images-ext-1.discordapp.net/external/y2SXBjVyNZtx2Gl4JQAOQS1kwJtO5gqonPIDjmJuxMg/https/1.bp.blogspot.com/-yVYtMyRqaAs/Xl-n-TDOlDI/AAAAAAAz79I/-I4BXPabFHAUMSYwlLro4XsZgI01gupsgCLcBGAsYHQ/s1600/AW4185658_11.gif')
        embed.add_field(name='First Thing First',
                        value='Please be sure to read and follow our <#944826144727904256>.\nPick your <#950728487319257099> for general identity.', inline=False)
        embed.add_field(name='General Chat Channel',
                        value='dont be shy to say hi to everyone at <#937230168223789069> for indonesian.\nand <#950666821210619914> for others region.', inline=False)
        embed.add_field(name='MHFZ Info', value='you could play mhfz in our server, you can check <#937301957935255583> for installation.\nand be sure to check <#1001395289233567854> so you dont miss out on event and new feature', inline=False)
        await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        ch = self.bot.get_channel(944837581034623007)
        guild = self.bot.get_guild(937230168223789066)
        joined = int(dt.timestamp(member.joined_at))
        embed = discord.Embed(title='Member Leave',
                              description=f'{member}', color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='joined since',
                        value=f"<t:{joined}:R>", inline=False)
        a = str(member.roles)
        b = a.split("name='")
        for i in range(len(b)-2):
            c = (b[i+2].split("'>")[0])
            embed.add_field(name='role', value=c, inline=False)
        embed.add_field(name='member count',
                        value=guild.member_count, inline=False)
        await ch.send(embed=embed)

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
