import discord
import random
from discord.ext import commands
from direc import *
from base import *


admin = 937306936939020309


class Server_Exclusive_Command(commands.Cog):
    """ mostly only decoration command """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guild(self, ctx):
        set_up()
        mod = moderator()
        a = mod.guild_id()
        b = mod.guild_name()
        c = len(a)
        d = [mod.guild_mem(a[i]) for i in range(c)]
        e = [mod.leader_id(a[i]) for i in range(c)]
        embed = discord.Embed(title='Guilds On Rain Server',
                              color=discord.Color.green())
        file = discord.File(
            f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        for i in range(c):
            embed.add_field(
                name=b[i], value=f'Guild ID : {a[i]}\n Member : {d[i]}/60\nLead ID : {e[i]}')
        await ctx.channel.send(file=file, embed=embed)

    @commands.command()
    async def mezeporta(self, ctx):
        bot = self.bot
        ch = bot.get_channel(952396919450243112)
        oke = []
        async for message in ch.history(limit=100):
            if message.attachments != []:
                space = str(message.attachments).split("url=\'")
                a = len(space)-1
                b = [space[i+1] for i in range(a)]
                for i in range(a):
                    c = b[i]
                    res = str(c).split("'>")[0]
                    oke.append(res)
        random.shuffle(oke)
        await ctx.channel.send(oke[0])

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx, spec):
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}")


async def setup(bot):
    await bot.add_cog(Server_Exclusive_Command(bot))
