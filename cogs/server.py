from typing import Literal
from unicodedata import name
import discord
import random
from discord.ext import commands
from discord import app_commands
from discord.ui import View
from direc import *
from base import *


admin = 937306936939020309


def mguild(dick):
    embed = discord.Embed(title='Guilds On Rain Server',
                          color=discord.Color.green())
    for i in dick:
        embed.add_field(
            name=i, value=f'Guild ID : {dick[i][0]}\n Member : {dick[i][1]}/60\nLead ID : {dick[i][2]}', inline=False)
    return embed


async def mmez(bot):
    embed = discord.Embed(title='Mezfest Leaderboard',
                          color=discord.Color.green())
    mod = moderator()
    li = mod.mez_lead()
    lu = mod.mez_tot()
    user = await bot.fetch_user(int(li[0]))
    embed.set_thumbnail(url=user.avatar)
    la = len(li)
    if la > 5:
        la = 5
    for i in range(la):
        ass = await bot.fetch_user(int(li[i]))
        embed.add_field(name=ass, value=f"Total Point : {lu[i]}")
    return embed


class My2View(View):
    def __init__(self, ctx, bot, listed, message):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.bot = bot
        self.length = len(listed)
        self.ln = 0
        self.dick = listed
        self.msg = message

    @discord.ui.button(label="See Previous", style=discord.ButtonStyle.green)
    async def malebutton(self, interaction, button):
        self.ln -= 1
        if self.ln < 0:
            self.ln = self.length-1
        self.msg = await self.msg.edit(embed=mguild(self.dick[self.ln]))
        button1 = [x for x in self.children if x.custom_id == "acc"][0]
        button1.label = f"{self.ln+1}/{self.length}"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="first page", style=discord.ButtonStyle.grey, disabled=True, custom_id="acc")
    async def femalebutton(self, interaction, button):
        await interaction.response.edit_message(view=self)
        self.value = "y"
        self.uid = self.damn[self.i-1]

    @discord.ui.button(label="See Next", style=discord.ButtonStyle.green, custom_id="oke")
    async def asubutton(self, interaction, button):
        self.ln += 1
        if self.ln == self.length:
            self.ln = 0
        self.msg = await self.msg.edit(embed=mguild(self.dick[self.ln]))
        button1 = [x for x in self.children if x.custom_id == "acc"][0]
        button1.label = f"{self.ln+1}/{self.length}"
        await interaction.response.edit_message(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("this button isn't for you", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        await self.ctx.send("Timeout")


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
        dick = {}
        lust = []
        for i in range(c):
            if d[i] > 1:
                dick[f"{b[i]}"] = [a[i], d[i], e[i]]
                print(dick)
                if len(dick) == 5:
                    lust.append(dick)
                    dick = {}
        lust.append(dick)
        print("section")
        print(lust)
        message = await ctx.send(embed=mguild(lust[0]))
        if len(lust) > 1:
            await ctx.send(view=My2View(ctx, self.bot, lust, message))

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

    # @app_commands.commands(name="mezfes", description="submit mezfes form")
    # @commands.has_role(1021645362974441513)
    # @commands.guild_only()
    # async def sync(self, interaction: discord.Interaction, mention: discord.Member, mez_title: Literal['Panic Honey', 'Guuku Scoop', 'Dokkan! Battle Cats', 'Nyanrendo', 'Uruki Pachinko'], mez_point: str):
    #     await interaction.response.defer()
    #     ch = self.bot.get_channel(1025595703403220992)
    #     oke = ['Panic Honey', 'Guuku Scoop',
    #            'Dokkan! Battle Cats', 'Nyanrendo', 'Uruki Pachinko']
    #     try:
    #         mez = mezfes(mention)
    #     except:
    #         add_mez(mention)
    #         mez = mezfes(mention)
    #     if mez_title == oke[0]:
    #         mez.set_honey(int(mez_point))
    #         ch.send(embed=await mmez(self.bot))
    #     elif mez_title == oke[1]:
    #         mez.set_scoop(int(mez_point))
    #         ch.send(embed=await mmez(self.bot))
    #     elif mez_title == oke[2]:
    #         mez.set_cats(int(mez_point))
    #         ch.send(embed=await mmez(self.bot))
    #     elif mez_title == oke[3]:
    #         mez.set_nyanrendo(int(mez_point))
    #         ch.send(embed=await mmez(self.bot))
    #     elif mez_title == oke[4]:
    #         mez.set_pachinko(int(mez_point))
    #         ch.send(embed=await mmez(self.bot))
    #     await interaction.followup.send("success")


async def setup(bot):
    await bot.add_cog(Server_Exclusive_Command(bot))
