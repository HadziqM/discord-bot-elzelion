from direc import *
from base import *
import discord
from discord.ui import View, TextInput, Modal
from bounty_cog import *
from datetime import datetime as dt


icon1 = ['\\GS.png', '\\HS.png', '\\H.png', '\\L.png', '\\SS.png', '\\LB.png', '\\DS.png',
         '\\LS.png', '\\HH.png', '\\GL.png', '\\B.png', '\\T.png', '\\SAF.png', '\\MS.png']
icon = [ICON_PATH+icon1[i] for i in range(len(icon1))]


class SubmitB(View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.value1 = None
        self.value2 = None

    @discord.ui.select(placeholder="Bounty Title", min_values=1, max_values=1, options=[discord.SelectOption(label='BBQ01', value='BBQ01'), discord.SelectOption(label='BBQ02', value='BBQ02'), discord.SelectOption(label='BBQ03', value='BBQ03'), discord.SelectOption(label='BBQ04', value='BBQ04'), discord.SelectOption(label='BBQ05', value='BBQ05'), discord.SelectOption(label='BBQ06', value='BBQ06'), discord.SelectOption(label='BBQ07', value='BBQ07'), discord.SelectOption(label='BBQ08', value='BBQ08'), discord.SelectOption(label='BBQ09', value='BBQ09'), discord.SelectOption(label='BBQ10', value='BBQ10'), discord.SelectOption(label='BBQ11', value='BBQ11'), discord.SelectOption(label='BBQ12', value='BBQ12'), discord.SelectOption(label='BBQ13', value='BBQ13'), discord.SelectOption(label='BBQ14', value='BBQ14'), discord.SelectOption(label='BBQ15', value='BBQ15'), discord.SelectOption(label='BBQ16', value='BBQ16'), discord.SelectOption(label='BBQ17', value='BBQ17'), discord.SelectOption(label='BBQ18', value='BBQ18'), discord.SelectOption(label='BBQ19', value='BBQ19'), discord.SelectOption(label='BBQ20', value='BBQ20'), discord.SelectOption(label='BBQ21', value='BBQ21'), discord.SelectOption(label='BBQ22', value='BBQ22'), discord.SelectOption(label='BBQ23', value='BBQ23'), discord.SelectOption(label='SP', value='SP')])
    async def on_select(self, interaction, select):
        select.disabled = True
        await interaction.response.edit_message(view=self)
        self.value1 = select.values[0]
        if self.value2 != None:
            self.stop()

    @discord.ui.select(placeholder="Bounty Methode", min_values=1, max_values=1, options=[discord.SelectOption(
        label="solo", value="solo"), discord.SelectOption(label="solo with npc", value="npc")])
    async def on_select1(self, interaction, select):
        select.disabled = True
        await interaction.response.edit_message(view=self)
        self.value2 = select.values[0]
        if self.value1 != None:
            self.stop()

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("this button isn't for you", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        await self.ctx.followup.send("Timeout")


class SubmitC(View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.value1 = None

    @discord.ui.select(placeholder="Bounty Title", min_values=1, max_values=1, options=[discord.SelectOption(label='BBQ01', value='BBQ01'), discord.SelectOption(label='BBQ02', value='BBQ02'), discord.SelectOption(label='BBQ03', value='BBQ03'), discord.SelectOption(label='BBQ04', value='BBQ04'), discord.SelectOption(label='BBQ05', value='BBQ05'), discord.SelectOption(label='BBQ06', value='BBQ06'), discord.SelectOption(label='BBQ07', value='BBQ07'), discord.SelectOption(label='BBQ08', value='BBQ08'), discord.SelectOption(label='BBQ09', value='BBQ09'), discord.SelectOption(label='BBQ10', value='BBQ10'), discord.SelectOption(label='BBQ11', value='BBQ11'), discord.SelectOption(label='BBQ12', value='BBQ12'), discord.SelectOption(label='BBQ13', value='BBQ13'), discord.SelectOption(label='BBQ14', value='BBQ14'), discord.SelectOption(label='BBQ15', value='BBQ15'), discord.SelectOption(label='BBQ16', value='BBQ16'), discord.SelectOption(label='BBQ17', value='BBQ17'), discord.SelectOption(label='BBQ18', value='BBQ18'), discord.SelectOption(label='BBQ19', value='BBQ19'), discord.SelectOption(label='BBQ20', value='BBQ20'), discord.SelectOption(label='BBQ21', value='BBQ21'), discord.SelectOption(label='BBQ22', value='BBQ22'), discord.SelectOption(label='BBQ23', value='BBQ23'), discord.SelectOption(label='SP', value='SP')])
    async def on_select(self, interaction, select):
        select.disabled = True
        await interaction.response.edit_message(view=self)
        self.value1 = select.values[0]
        self.stop()

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("this button isn't for you", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        await self.ctx.followup.send("Timeout")


class MezFez(View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.value1 = None

    @discord.ui.select(placeholder="MezFest Minigame", min_values=1, max_values=1, options=[discord.SelectOption(label="Panic Honey", value="Panic Honey"), discord.SelectOption(label="Guuku Scoop", value="Guuku Scoop"), discord.SelectOption(label="Dokkan! Battle Cats", value="Dokkan! Battle Cats"), discord.SelectOption(label="Nyanrendo", value="Nyanrendo"), discord.SelectOption(label="Uruki Pachinko", value="Uruki Pachinko")])
    async def getone(self, interaction, select):
        select.disabled = True
        await interaction.response.edit_message(view=self)
        self.value1 = select.values[0]
        self.stop()

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.user:
            await interaction.response.send_message("this button isn't for you", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        await self.ctx.followup.send("Timeout")


class Questionnaire(Modal):
    def __init__(self, link, ch):
        super().__init__(title='Transmog Contest Form', timeout=None)
        self.link = link
        self.ch = ch
    name = TextInput(label='Transmog Title',
                     placeholder="your transmo title", required=True)
    answer = TextInput(label='Description',
                       style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Your Participation Been Submitted!', ephemeral=True)
        embed = discord.Embed(
            title=self.name, description=self.answer, color=discord.Colour.blue())
        embed.set_image(url=self.link)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"Submited by: {interaction.user.display_name}")
        msg = await self.ch.send(embed=embed)
        await msg.add_reaction('👍')


async def mcard(member, interact):
    set_up()
    char = character(check_disc(member.id))
    a = char.name
    print(a)
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
        user = member
        embed.set_author(name=user.display_name, icon_url=user.avatar)
    else:
        None
    file = discord.File(icon[char.weapon], filename='wep.png')
    embed.set_thumbnail(url='attachment://wep.png')
    embed.add_field(
        name='Account', value=f'Username : {c}\nUser ID : {b}\nLast Login : <t:{i}:R>', inline=False)
    embed.add_field(
        name='Character', value=f'Gender : {f}\nHunter Rank : {g} (unrestrained)\nGold Rank : {h}', inline=False)
    embed.add_field(
        name='Guild', value=f'Name : {d}\nGuild ID : {e}', inline=False)
    return await interact.response.send_message(file=file, embed=embed)


async def mevent(member, interact):
    now = int(dt.timestamp(dt.now()))
    user = member
    gac = gacha(member.id)
    dif = gac.bbq_time + 24*60*60
    sam = gac.bbq_time + 48*60*60
    different = f"<t:{dif}:R>"
    if dif <= now:
        different = "You can do it now"
    same = f"<t:{gac.bbq_time + 48*60*60}:R>"
    if sam <= now:
        same = "You can do it now"
    mod = moderator()
    try:
        rank = mod.disc_all().index(str(member.id))+1
    except:
        rank = "No Rank"
    x = f"<t:{gac.bbq_time}:R>"
    if gac.bbq_time == 0:
        x = "Not Yet"
    embed = discord.Embed(title="My Event Status",
                          description=f'Bounty Coin : {gac.bounty}\nGacha Ticket : {gac.ticket}\nPity Count : {gac.pity}\nLatest Bounty : {gac.bbq}\nTime Cleared : {x}\nDifferent BBQ CD: {different}\nSame BBQ CD: {same}\nBounty Rank : {rank}', color=discord.Color.red())
    embed.set_author(name=user.display_name, icon_url=user.avatar)
    await interact.response.send_message(content=None, embed=embed)


async def msubmit(msg, interact, bot):
    if interact.user.id != msg.author.id:
        return await interact.response.send_message("its not your own")
    if str(msg.attachments) == '[]':
        return await interact.response.send_message("there is no attachments/image")
    # link = msg.attachments[0].url
    views = SubmitB(interact)
    await interact.response.send_message(view=views)
    await views.wait()
    if views.value2 == "solo":
        await submit_solo_after(bot, interact, views.value1, msg.attachments[0].url, "solo")
    else:
        await submit_solo_after(bot, interact, views.value1, msg.attachments[0].url, "npc")


async def msubmit_multi(msg, interact, bot):
    if interact.user.id != msg.author.id:
        return await interact.response.send_message("its not your own")
    if str(msg.attachments) == '[]':
        return await interact.response.send_message("there is no attachments/image")
    link = msg.attachments[0].url
    did = [interact.user.id]
    for i in re.findall("<@!?([0-9]+)>", msg.content):
        did.append(int(i))
    if len(did) == 1:
        return await interact.response.send_message("no mentions detected")
    await interact.response.defer()
    text = "Multiplayer Submission With Party "
    for i in did:
        text += f"<@{i}> "
    views = SubmitC(interact)
    await interact.followup.send(content=text, view=views, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    await views.wait()
    await submit_multi_after(bot, interact, views.value1, link, msg.content)


async def transcontest(msg, interact, bot):
    channel = bot.get_channel(1024593377423011850)
    if interact.user.id != msg.author.id:
        return await interact.response.send_message("its not your own")
    if str(msg.attachments) == '[]':
        return await interact.response.send_message("there is no attachments/image")
    link = msg.attachments[0].url
    await interact.response.send_modal(Questionnaire(link, channel))


async def mezcontest(msg, interact, bot):
    channel = bot.get_channel(1024593511401668648)
    channel2 = bot.get_channel(1024593511401668648)
    if interact.user.id != msg.author.id:
        return await interact.response.send_message("its not your own")
    if str(msg.attachments) == '[]':
        return await interact.response.send_message("there is no attachments/image")
    try:
        value = int(msg.content)
    except:
        return await interact.response.send_message("points detected or invalid format")
    link = msg.attachments[0].url
    view = MezFez(interact)
    await interact.response.send_message(view=view)
    color = [discord.Colour.blue(), discord.Colour.red(
    ), discord.Colour.yellow(), discord.Colour.green(), discord.Colour.teal()]
    oke = ['Panic Honey', 'Guuku Scoop',
           'Dokkan! Battle Cats', 'Nyanrendo', 'Uruki Pachinko']
    await view.wait()
    msg = await channel2.send(embed=makefes(value, view.value1, interact.user.display_name, color[oke.index(view.value1)], link, interact.user.display_avatar.url))


def makefes(value, title, name, color, link, avatar):
    embed = discord.Embed(
        title=title, description=f'git {value} points', color=color)
    embed.set_image(url=link)
    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f"Submited by: {name}")
    return embed
