import discord
import asyncio
from discord import app_commands
from discord.ui import View, Button
from datetime import datetime as dt
from discord.ext import commands
from discord.utils import get
from direc import *
from base import *

icon1 = ['\\GS.png', '\\HS.png', '\\H.png', '\\L.png', '\\SS.png', '\\LB.png', '\\DS.png',
         '\\LS.png', '\\HH.png', '\\GL.png', '\\B.png', '\\T.png', '\\SAF.png', '\\MS.png']
icon = [ICON_PATH+icon1[i] for i in range(len(icon1))]


async def mcard(bot, ctx, arg):
    set_up()
    type(arg)
    char = character(arg)
    a = char.name
    if a == None:
        return None
    b = char.uid
    c = char.username
    d = char.guild
    e = char.gid
    f = char.gender
    g = char.hrp
    h = char.gr
    i = char.login
    embed = discord.Embed(title=a, color=discord.Color.blue())
    if char.discord != None:
        user = await bot.fetch_user(int(char.discord))
        embed.set_author(name=user.display_name, icon_url=user.avatar)
    else:
        None
    file = discord.File(icon[char.weapon], filename='wep.png')
    embed.set_thumbnail(url='attachment://wep.png')
    embed.add_field(
        name='Account', value=f'Username : {c}\nUser ID : {b}\nLast Login : <t:{i}:R>', inline=False)
    embed.add_field(
        name='Character', value=f'Gender : {f}\nHunter Rank : {g}\nGold Rank : {h}', inline=False)
    embed.add_field(
        name='Guild', value=f'Name : {d}\nGuild ID : {e}', inline=False)
    return await ctx.channel.send(file=file, embed=embed)


async def mcur(bot, ctx, arg):
    set_up()
    char = character(arg)
    a = char.gcp
    b = char.prem
    c = char.trial
    d = char.netcafe
    e = char.frontier
    f = char.kouryou
    g = char.bounty
    embed = discord.Embed(title=f"{char.name}\'s currencies",
                          description=f'Bounty Coin : {g}\nGCPoint : {a}\nPremium coin : {b}\ntrial coin : {c}\nnetcafe point : {d}\nfrontier point : {e}\nkouryou point : {f}', color=discord.Color.red())
    if char.discord != None:
        user = await bot.fetch_user(int(char.discord))
        embed.set_author(name=user.display_name, icon_url=user.avatar)
    else:
        None
    await ctx.channel.send(content=None, embed=embed)


async def mboost(bot, ctx, arg):
    set_up()
    char = character(arg)
    a = char.boost()
    b = []
    e = char.name
    for i in range(len(a)):
        if a[i] == 1:
            b.append('cooldown')
        elif a[i] == 0:
            b.append('available')
        else:
            b.append('active')
    embed = discord.Embed(title=e+'''\'s'''+' Login Boost',
                          color=discord.Color.blue())
    if char.discord != None:
        user = await bot.fetch_user(int(char.discord))
        embed.set_author(name=user.display_name, icon_url=user.avatar)
    else:
        None
    for i in range(len(b)):
        embed.add_field(name='Week '+str(i+1), value=b[i], inline=False)
    await ctx.channel.send(content=None, embed=embed)


class My2View(View):
    def __init__(self, ctx, bot, listed):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.bot = bot
        self.damn = listed
        self.i = 0
        self.msg = None

    @discord.ui.button(label=f"See Account", style=discord.ButtonStyle.grey)
    async def malebutton(self, interaction, button):
        button.label = f"see {self.damn[self.i]}"
        if self.msg:
            await self.msg.delete()
        self.msg = await mcard(self.bot, self.ctx, self.damn[self.i])
        self.i += 1
        if self.i == len(self.damn):
            self.i = 0
        button1 = [x for x in self.children if x.custom_id == "acc"][0]
        button1.disabled = False
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Use This Account", style=discord.ButtonStyle.green, disabled=True, custom_id="acc")
    async def femalebutton(self, interaction, button):
        await interaction.response.edit_message(view=self)
        self.value = "y"
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("this button isn't for you")
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        await self.ctx.send("Timeout")


class MyView(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    @discord.ui.button(label="Register as Male", style=discord.ButtonStyle.green)
    async def malebutton(self, interaction, button):
        await interaction.response.edit_message(view=self)
        self.value = "m"
        self.stop()

    @discord.ui.button(label="Register as Female", style=discord.ButtonStyle.blurple)
    async def femalebutton(self, interaction, button):
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.value = "f"
        self.stop()

    @discord.ui.button(label="do nothing", style=discord.ButtonStyle.red)
    async def nobutton(self, interaction, button):
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("understanable, Have a nice day!")
        self.value = None
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("this button isn't for you")
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        await self.ctx.send("Timeout")


class MHFZ_User_Interactive(commands.Cog):
    """ all the command needed to connect to your Mhfz game """

    def __init__(self, bot):
        bot.tree.on_error = self.on_app_command_error
        self.bot = bot

    async def on_app_command_error(self, interaction, error):
        print(error)

    @commands.hybrid_command(name="id")
    async def id(self, ctx: commands.Context, in_game_name: str):
        set_up()
        b = [i for i in in_game_name]
        for i in range(len(b)):
            if b[i] == "'":
                b[i] = "''"
        arg = ''.join(b)
        a = char_id(arg)
        view = MyView(ctx)
        if a == None:
            await ctx.send("that charachter name isnt exist on Rain server database\nmake sure that youare playing on rain server and input correct charachter name (not username)")
        elif isinstance(a, int):
            await mcard(self.bot, ctx, a)
            msg = await ctx.send(view=view)
            await view.wait()
            if view.value == "m":
                await ctx.send("male")
            elif view.value == "f":
                await ctx.send("femmale")
            await msg.delete()
        else:
            view2 = My2View(ctx, self.bot, a)
            length = len(a)
            await ctx.send(f'there is {length} character with same name')
            msg = await ctx.send(view=view2)
            await view2.wait()
            if view2.value == "y":
                await msg.delete()
                msg2 = await ctx.send(view=view)
                await view.wait()
                if view.value == "m":
                    await ctx.send("male")
                elif view.value == "f":
                    await ctx.send("femmale")
                await msg2.delete()

    @commands.command()
    async def card(self, ctx, arg):
        try:
            int(arg)
        except:
            did = int(arg[2:-1])
            set_up()
            arg = check_disc(did)
        await mcard(self.bot, ctx, arg)

    @commands.command()
    async def mycard(self, ctx):
        a = ctx.message.author.id
        set_up()
        try:
            arg = check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        await mcard(self.bot, ctx, arg)

    @commands.command()
    async def currency(self, ctx, arg):
        try:
            int(arg)
        except:
            did = int(arg[2:-1])
            set_up()
            arg = check_disc(did)
        await mcur(self.bot, ctx, arg)

    @commands.command()
    async def mycurrency(self, ctx):
        a = ctx.message.author.id
        set_up()
        try:
            arg = check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        await mcur(self.bot, ctx, arg)

    @commands.command()
    async def myboost(self, ctx):
        a = ctx.message.author.id
        set_up()
        try:
            arg = check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        await mboost(self.bot, ctx, arg)

    @commands.command()
    async def transmog(self, ctx):
        a = ctx.message.author.id
        set_up()
        try:
            arg = check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        char = character(arg)
        char.mog()
        await ctx.send(f"{char.name} transmog is all unlocked")

    @commands.command()
    async def boost(self, ctx, arg):
        try:
            int(arg)
        except:
            did = int(arg[2:-1])
            set_up()
            arg = check_disc(did)
        await mboost(self.bot, ctx, arg)

    @commands.command()
    async def myboost_off(self, ctx):
        a = ctx.message.author.id
        set_up()
        arg = check_disc(a)
        char = character(arg)
        char.boost_off()
        await ctx.channel.send(f"turn off {char.name} boost")

    @commands.command()
    async def myboost_on(self, ctx):
        a = ctx.message.author.id
        set_up()
        arg = check_disc(a)
        char = character(arg)
        now = int(dt.timestamp(dt.now()))
        if now >= char.boostcd:
            char.boost_on()
            char.set_boostcd(now+(60*60*24*7))
            await ctx.channel.send(f"turn on {char.name} boost")
        else:
            await ctx.send(f"sorry this command is on cooldown for you till <t:{char.boostcd}:R>")

    @commands.command()
    async def join_guild(self, ctx, arg1):
        a = ctx.message.author.id
        set_up()
        try:
            int(arg1)
        except:
            arg1 = guild_check(arg1)
        arg = check_disc(a)
        char = character(arg)
        mod = moderator()
        if char.guild != 'No Guild':
            return await ctx.send("youare already on guild")
        if mod.guild_mem(arg1) >= 60:
            await ctx.channel.send(f"Guild already overloaded")
            return
        char.join_guild(arg1)
        await ctx.channel.send(f"{char.name} joined a guild")

    @commands.command()
    async def transfer_guild(self, ctx, arg1):
        a = ctx.message.author.id
        set_up()
        arg = check_disc(a)
        char = character(arg)
        char.transfer_guild(arg1)
        await ctx.channel.send(f"{char.name} transfered")

    @commands.command()
    async def mysave(self, ctx):
        a = ctx.message.author.id
        set_up()
        arg = check_disc(a)
        char = character(arg)
        char.download_file()
        user = await self.bot.fetch_user(int(char.discord))
        await user.send(f"downloading {char.name} savedata")
        await user.send(file=discord.File(f'{SAVE_PATH}\\savedata_{char.cid}.bin'))
        await user.send(f"downloading {char.name} partner data")
        await user.send(file=discord.File(f'{SAVE_PATH}\\partner_{char.cid}.bin'))
        await ctx.channel.send("dm'd")

    @commands.command()
    async def mysave_all(self, ctx):
        a = ctx.message.author.id
        set_up()
        arg = check_disc(a)
        char = character(arg)
        user = await self.bot.fetch_user(int(char.discord))
        list = char.download_all()
        for i in list:
            await user.send(file=discord.File(i))
        await user.send(f"downloaded all {char.name} not empty character data")
        await ctx.channel.send("dm'd")

    @commands.command()
    async def claim_newb(self, ctx, arg):
        list = ["BGM01", "BGM02", "BGM03", "BGM04", "BGM05", "BGM06"]
        if arg not in list:
            await ctx.send("i cant recognize set, check your spelling")
            return
        a = ctx.message.author.id
        set_up()
        try:
            cid = check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        char = character(cid)
        if char.newbie == False:
            await ctx.send("you already claim once")
            return
        else:
            gr = int(char.gr)
            if 200 <= gr < 500:
                char.newbie_rw(arg)
                await ctx.send("reward already distributed")
            else:
                await ctx.send("GR requirement not met")

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def register(self, ctx, arg, arg1):
        cd = int(dt.timestamp(dt.now())) + 60
        bot = self.bot
        a = ctx.message.author.id
        set_up()
        try:
            char = character(arg)
        except:
            return await ctx.send(f"id not found, or invalid id being input\nwait for <t:{cd}:R> b4 you can use this command again")

        if char.discord != None:
            return await ctx.channel.send(f"character already owned\nwait for <t:{cd}:R> b4 you can use this command again")

        try:
            b = check_disc(a)
            return await ctx.channel.send(f"you have own {b}\nwait for <t:{cd}:R> b4 you can use this command again")

        except:
            None
        if arg1 == 'm' or arg1 == 'f':
            None
        else:
            await ctx.channel.send("invalid genderwait for <t:{cd}:R> b4 you can use this command again")
            return
        await mcard(self.bot, ctx, arg)
        button1 = Button(label="Yes!", style=discord.ButtonStyle.green)
        button2 = Button(label="Nope!", style=discord.ButtonStyle.red)
        view = View()
        view.add_item(button1)
        view.add_item(button2)

        async def button1_callback(interaction):
            await self.mytest(ctx, a, arg, arg1)

        async def button2_callback(interaction):
            await interaction.response.send_message("understanable have a nice day!")

        button1.callback = button1_callback
        button2.callback = button2_callback
        await ctx.send(view=view)

    async def mytest(self, ctx, sub, arg, arg1):
        role = get(ctx.message.guild.roles, id=1017643913667936318)
        await ctx.author.add_roles(role)
        char = character(arg)
        char.add_data(sub, arg1)
        gac = gacha(sub)
        gac.add_gacha(100)
        return await ctx.channel.send('now you are registered\nand congrats you also got got free 10 try on gacha')


async def setup(bot):
    await bot.add_cog(MHFZ_User_Interactive(bot))
