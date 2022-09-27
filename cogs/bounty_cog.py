import discord
import urllib3
import cv2
import re
import numpy as np
from discord.ext import commands
from discord.utils import get
from datetime import datetime as dt
from direc import *
from base import *
from discord.ui import View
from typing import Literal
from discord import app_commands

main = database()
anc = int(main.announce)
cd = int(main.cd)
mod_id = int(main.mod)
lead = int(main.leaderboard)
promo = int(main.promotion)

jpg = ['rain_demolizer.jpg', 'road_champion.jpg',
       'bounty_champion.jpg', 'bounty_master.jpg', 'bounty_expert.jpg']
jpg = [f'{TITLE_PATH}\\'+jpg[i] for i in range(len(jpg))]
top = [35, 154, 145, 145, 145]
left = [420, 445, 600, 600, 600]
bonus = ['**50%**', '**40%**', '**30%**', '**20%**', '**10%**']
bonus = ['you got '+bonus[i] +
         ' bonus point every time you complete bounty' for i in range(len(bonus))]


async def mtest(chan, user, cid, state):
    top1 = top[state]
    left1 = left[state]
    jpg1 = jpg[state]
    bg = cv2.imread(jpg1, cv2.IMREAD_UNCHANGED)
    d = 160
    botom = top1+d
    rg = left1+d
    url = str(user.avatar)
    http = urllib3.PoolManager()
    req = http.request('GET', url, preload_content=False)
    req.release_conn()
    byte = req.read()
    arr = np.asarray(bytearray(byte), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    try:
        if img == None:
            open('test.gif', 'wb').write(byte)
            cap = cv2.VideoCapture('test.gif')
            ret, frame = cap.read()
            img = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    except:
        None
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    img = cv2.resize(img, (d, d), interpolation=cv2.INTER_AREA)
    mask1 = np.zeros_like(img, dtype='uint8')
    mask1 = cv2.circle(mask1, (80, 80), 80, (255, 255, 255), -1)
    mask2 = 255-mask1
    roi = bg[top1:botom, left1:rg]
    roi = cv2.bitwise_and(roi, roi, mask=mask2[:, :, 0])
    img = cv2.bitwise_and(img, img, mask=mask1[:, :, 0])
    res = cv2.add(roi, img)
    bg[top1:botom, left1:rg] = res
    cv2.imwrite(f'{TITLE_PATH}\\oke.png', bg)
# msg = await chan.send(file = discord.File(f'{TITLE_PATH}\\oke.png'))
    embed = discord.Embed(
        title='Congratulation on Promotion', color=discord.Color.green())
    file = discord.File(f'{TITLE_PATH}\\oke.png', filename='prom.png')
    embed.set_image(url='attachment://prom.png')
    char = character(cid)
    set_up()
    op = char.overpower()
    if state == 4 or state == 3 or state == 2:
        if op == True:
            # await chan.send('your bounty point boost didnt change since you have other dominant title')
            embed.add_field(
                name=char.name, value='your bounty point boost didnt change since you have other dominant title')
        else:
            # await chan.send(bonus[state])
            embed.add_field(name=char.name, value=bonus[state])
    else:
        # await chan.send(bonus[state])
        embed.add_field(name=char.name, value=bonus[state])
    msg = await chan.send(file=file, embed=embed)
    await msg.add_reaction('\U0001f973')


async def mbounty(chan):
    set_up()
    mod = moderator()
    a = mod.bounty_all()
    c = mod.bounty_ex()
    embed = discord.Embed(title='AVAILABLE BOUNTY',
                          color=discord.Color.green())
    file = discord.File(f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
    embed.set_thumbnail(url='attachment://serv.png')
    for i in range(len(a)):
        bon = bounty(a[i])
        b = bon.cooldown
        embed.add_field(name=a[i], value=f'{c[i]}\nAvailable= {b}')
    await chan.send(file=file, embed=embed)


async def mleaderboard(bot, chan, chan1):
    set_up()
    mod = moderator()
    a = mod.bounty_pt()
    b = mod.char_all()
    c = mod.disc_all()
    aser = await bot.fetch_user(int(c[0]))
    embed = discord.Embed(title='BOUNTY LEADERBOARD',
                          color=discord.Color.blue())
    file = discord.File(f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
    embed.set_thumbnail(url=aser.avatar)
    embed.set_author(name="Rain Server", icon_url='attachment://serv.png')
    g = int(len(c))
    backup = '```'
    for i in range(g):
        user = await bot.fetch_user(int(c[i]))
        char = character(b[i])
        d = char.name
        e = ','.join(char.title)
        if i >= 6:
            backup = backup + '\n' + f'{user} = {str(a[i])}'
        elif i <= 5:
            backup = backup + '\n' + f'{user} = {str(a[i])}'
            embed.add_field(
                name=d, value=f'Point : {str(a[i])}\n'+f'Discord : {user}\n'+f'Title: {e}', inline=False)
    backup = backup + '\n```'
    await chan.send(file=file, embed=embed)
    await chan1.send(backup)


async def mpromote(ctx, state, user, chan, cid):
    road = get(ctx.roles, id=int(main.road))
    elze = get(ctx.roles, id=int(main.elze))
    champion = get(ctx.roles, id=int(main.champion))
    master = get(ctx.roles, id=int(main.master))
    expert = get(ctx.roles, id=int(main.expert))
    if state == 1:
        await user.add_roles(expert)
        await chan.send(f"congratulation <@{user.id}> you are promoted to **Bounty Expert** for reaching 25k bounty point")
        await mtest(chan, user, cid, 4)
    elif state == 2:
        await user.add_roles(master)
        await chan.send(f"congratulation <@{user.id}> you are promoted to **Bounty Master** for reaching 50k bounty point")
        await mtest(chan, user, cid, 3)
    elif state == 3:
        await user.add_roles(champion)
        await chan.send(f"congratulation <@{user.id}> you are promoted to **Bounty Champion** for reaching 200k bounty point")
        await mtest(chan, user, cid, 2)
    elif state == 4:
        await user.add_roles(road)
        await chan.send(f"congratulation <@{user.id}> you are promoted to **Road Champion** for reaching 200 floor road")
        await mtest(chan, user, cid, 1)
    elif state == 5:
        await user.add_roles(elze)
        await chan.send(f"congratulation <@{user.id}> you are promoted to **Rain Demolizer** for for defeating musou elzelion")
        await mtest(chan, user, cid, 0)
    else:
        return


async def mannounce(bot, ch, a, arg, methode):
    date = int(dt.timestamp(dt.now()))
    embed = discord.Embed(title=arg[0], color=discord.Color.green())
    file = discord.File(
        f'{BOUNTY_PATH}\\{arg[0]}.png', filename='serv.png')
    embed.set_thumbnail(url='attachment://serv.png')
    embed.set_image(url=arg[1])
    if methode == "solo":
        user = await bot.fetch_user(int(a[0]))
        embed.set_author(name=user.display_name, icon_url=user.avatar)
        embed.add_field(name=a[1], value=f'Cleared: Solo \n<t:{date}:F>')
    elif methode == "npc":
        user = await bot.fetch_user(int(a[0]))
        embed.set_author(name=user.display_name, icon_url=user.avatar)
        embed.add_field(
            name=a[1], value=f'Cleared: Multiplayer With NPC \n<t:{date}:F>')
    else:
        embed.add_field(
            name='TEAM', value=f'Cleared: Multiplayer \n<t:{date}:F>', inline=False)
        length = len(a)
        print(length)
        print(a)
        for i in range(int(length/2)):
            user = await bot.fetch_user(int(a[i]))
            embed.add_field(
                name=a[i+int(length/2)], value=f'Discord: {user}', inline=False)
    return await ch.send(file=file, embed=embed)


class MyView(View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def malebutton(self, interaction, button):
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.uss = interaction.user
        self.value = "y"
        self.stop()

    @discord.ui.button(label="Not Approve", style=discord.ButtonStyle.red)
    async def femalebutton(self, interaction, button):
        button.disabled = True
        self.uss = interaction.user
        await interaction.response.edit_message(view=self)
        self.value = "n"
        self.stop()


async def appoval_s(interaction, ch, ch1, did, bbq, picture, name, mt, time, bot):
    confirm = await mannounce(bot, ch, [did, name], [bbq, picture], mt)
    view = MyView(interaction)
    msg = await ch.send(view=view)
    await view.wait()
    if view.value == 'y':
        ch_an = bot.get_channel(anc)
        arg = [bbq, picture, [did], mt]
        await msg.delete()
        await confirm.delete()
        await interaction.followup.send(f"<@{did}> your bounty had been approved by {view.uss}")
        if mt == "solo":
            await mannounce(bot, ch_an, [did, name], [bbq, picture], mt)
            await announce(bot, interaction, arg)
        else:
            await mannounce(bot, ch_an, [did, name], [bbq, picture], mt)
            await announce(bot, interaction, arg)
    elif view.value == 'n':
        await msg.delete()
        await confirm.delete()
        await interaction.followup.send(f"<@{did}> your bounty isnt approved by {view.uss}")
        set_up()
        bon = bounty(bbq)
        bon.cooldown_set(bon.cooldown+1)
        gac = gacha(did)
        gac.set_bbq_time(time)
        await mbounty(ch1)


async def approve_m(interaction, ch, ch1, bbq, picture, anjir, lgt, time, bot, did):
    confirm = await mannounce(bot, ch, anjir, [bbq, picture], "multi")
    view = MyView(ctx=interaction)
    msg = await ch.send(view=view)
    await view.wait()
    if view.value == 'y':
        ch_an = bot.get_channel(anc)
        arg = [bbq, picture, did, "multi"]
        await msg.delete()
        await confirm.delete()
        await interaction.followup.send(f"<@{anjir[0]}> submision and co. had been approved by {view.uss}")
        await mannounce(bot, ch_an, anjir, [bbq, picture], "multi")
        await announce(bot, interaction, arg)
    elif view.value == 'n':
        await interaction.followup.send(f"<@{anjir[0]}> submision and co. isnt approved by {view.uss}")
        await msg.delete()
        await confirm.delete()
        set_up()
        for i in range(lgt):
            gacha(anjir[i]).set_bbq_time(time[i])
        bon = bounty(bbq)
        bon.cooldown_set(bon.cooldown+1)
        await mbounty(ch1)


async def announce(bot, ctx, arg):
    ch2 = bot.get_channel(lead)
    ch3 = bot.get_channel(promo)
    ch4 = bot.get_channel(1009415908927733811)
    set_up()
    bon = bounty(arg[0])
    if arg[3] == "solo":
        gac = gacha(arg[2][0])
        gac.set_bbq(arg[0])
        cid = check_disc(arg[2][0])
        a = bon.announce_now('solo', cid)
        if a[-1] == 0:
            await ctx.followup.send(f"<@{arg[2][0]}> since reward for current bounty is too much, it cant be distributed in game trough normal mean, coordinate with EVE to get your reward")
        else:
            await ctx.followup.send(f"<@{arg[2][0]}> reward already distributed, claim it before bounty white day")
        await mpromote(ctx.guild, a[-2], ctx.guild.get_member(int(a[0])), ch3, cid)
    elif arg[3] == 'npc':
        gac = gacha(arg[2][0])
        gac.set_bbq(arg[0])
        cid = check_disc(arg[2][0])
        cid = check_disc(arg[2][0])
        a = bon.announce_now('cat', cid)
        if a[-1] == 0:
            await ctx.followup.send(f"<@{arg[2][0]}> since reward for current bounty is too much, it cant be distributed in game trough normal mean, coordinate with EVE to get your reward")
        else:
            await ctx.followup.send(f"<@{arg[2][0]}> reward already distributed, claim it before bounty white day")
        await mpromote(ctx.guild, a[-2], ctx.guild.get_member(int(a[0])), ch3, cid)
    else:
        cid = []
        for i in arg[2]:
            did = i
            gac = gacha(did)
            gac.set_bbq(arg[0])
            cidi = check_disc(did)
            cid.append(cidi)
        a, b, c, d = bon.announce_now('multi', cid)
        for i in range(len(cid)):
            a.append(b[i])
            if c[i] == 0:
                await ctx.followup.send(f"<@{a[i]}> since reward for current bounty is too much, it cant be distributed in game trough normal mean, coordinate with EVE to get your reward")
            else:
                await ctx.followup.send(f"<@{a[i]}> reward already distributed, claim it before bounty white day")
            await mpromote(ctx.guild, d[i], ctx.guild.get_member(int(a[i])), ch3, cid[i])
    await mleaderboard(bot, ch2, ch4)


async def submit_solo_after(bot, interaction, bbq, picture_link, methode):
    now = int(dt.timestamp(dt.now()))
    gac = gacha(interaction.user.id)
    if gac.bbq == bbq and now < (gac.bbq_time + 60*60*48):
        return await interaction.followup.send(f"sorry you cant take same bounty before <t:{gac.bbq_time+60*60*48}:R>")
    elif gac.bbq != bbq and now < (gac.bbq_time + 60*60*24):
        return await interaction.followup.send(f"sorry you cant take this bounty before <t:{gac.bbq_time+60*60*24}:R>")
    time = gac.bbq_time
    gac.set_bbq_time(int(dt.timestamp(dt.now())))
    ch = bot.get_channel(1020947766203129876)
    ch1 = bot.get_channel(cd)
    set_up()
    try:
        bon = bounty(bbq)
    except:
        return await interaction.followup.send("wrong input")
    if bon.cooldown == 0:
        await interaction.followup.send("cooldown")
        return
    did = interaction.user.id
    try:
        cid = check_disc(did)
    except:
        await interaction.followup.send(
            f'<@{did}> you need to register first to participate bounty')
        return
    await interaction.followup.send("submitted your form\nwait for admin aproval")
    char = character(cid)
    bon.cooldown_now()
    await mbounty(ch1)
    await appoval_s(interaction, ch, ch1, did, bbq, picture_link, char.name, methode, time, bot)


async def submit_multi_after(bot, interaction, bbq, picture_link, mentions):
    now = int(dt.timestamp(dt.now()))
    ch = bot.get_channel(1020947766203129876)
    ch1 = bot.get_channel(cd)
    set_up()
    try:
        bon = bounty(bbq)
    except:
        return await interaction.followup.send("wrong input")
    if bon.cooldown == 0:
        await interaction.followup.send("cooldown")
        return
    did = [interaction.user.id]
    for i in re.findall("<@!?([0-9]+)>", mentions):
        if interaction.user.id == i:
            return await interaction.followup.send("you cant ping yourself")
        did.append(int(i))
    cid = []
    for i in did:
        try:
            try:
                cidi = check_disc(i)
                cid.append(cidi)
            except:
                await interaction.followup.send(
                    f'<@{i}> you need to register first to participate bounty')
                return
        except:
            None
    if len(did) == 1:
        await interaction.followup.send("use submit_npc instead")
        return
    time = []
    for i in did:
        gac = gacha(i)
        if gac.bbq == bbq and now < (gac.bbq_time + 60*60*48):
            return await interaction.followup.send(f"sorry <@{i}> cant take same bounty before <t:{gac.bbq_time+60*60*48}:R>")
        elif gac.bbq != bbq and now < (gac.bbq_time + 60*60*24):
            return await interaction.followup.send(f"sorry <@{i}> cant take this bounty before <t:{gac.bbq_time+60*60*24}:R>")
        time.append(gac.bbq_time)
    for i in did:
        gac.set_bbq_time(int(dt.timestamp(dt.now())))
    await interaction.followup.send("sent your team submission to admin")
    bon.cooldown_now()
    await mbounty(ch1)
    anjir = [i for i in did]
    for i in cid:
        char = character(i)
        anjir.append(char.name)
    lgt = len(cid)
    print(anjir)
    await approve_m(interaction, ch, ch1, bbq, picture_link, anjir, lgt, time, bot, did)


class Bounty_Event(commands.Cog):
    """ Participate bounty to get generous reward """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bounty_list(self, ctx):
        chan = ctx.channel
        await mbounty(chan)

    @app_commands.command(name="submit_solo", description="submit your bounty application, input please input picture link with actual link (dont use ')")
    async def submit_solo(self, interaction: discord.Interaction, bbq: Literal["BBQ01", "BBQ02", "BBQ03", "BBQ04", "BBQ05", "BBQ06", "BBQ07", "BBQ08", "BBQ09", "BBQ10", "BBQ11", "BBQ12", "BBQ13", "BBQ14", "BBQ15", "BBQ16", "BBQ17", "BBQ18", "BBQ19", "BBQ20", "BBQ21", "BBQ22", "BBQ23", "SP"], picture_link: str):
        await interaction.response.defer()
        await submit_solo_after(self.bot, interaction, bbq, picture_link, "solo")

    @app_commands.command(name="submit_npc", description="submit your bounty application, input please input picture link with actual link (dont use ')")
    async def submit_npc(self, interaction: discord.Interaction, bbq: Literal["BBQ01", "BBQ02", "BBQ03", "BBQ04", "BBQ05", "BBQ06", "BBQ07", "BBQ08", "BBQ09", "BBQ10", "BBQ11", "BBQ12", "BBQ13", "BBQ14", "BBQ15", "BBQ16", "BBQ17", "BBQ18", "BBQ19", "BBQ20", "BBQ21", "BBQ22", "BBQ23", "SP"], picture_link: str):
        await interaction.response.defer()
        await submit_solo_after(self.bot, interaction, bbq, picture_link, "npc")

    @app_commands.command(name="submit_multi", description="submit your bounty application, input please input picture link with actual link (dont use ')")
    async def submit_multi(self, interaction: discord.Interaction, bbq: Literal["BBQ01", "BBQ02", "BBQ03", "BBQ04", "BBQ05", "BBQ06", "BBQ07", "BBQ08", "BBQ09", "BBQ10", "BBQ11", "BBQ12", "BBQ13", "BBQ14", "BBQ15", "BBQ16", "BBQ17", "BBQ18", "BBQ19", "BBQ20", "BBQ21", "BBQ22", "BBQ23", "SP"], picture_link: str, mentions: str):
        await interaction.response.defer()
        await submit_multi_after(self.bot, interaction, bbq, picture_link, mentions)

    @commands.command()
    @commands.has_role(mod_id)
    async def cooldown(self, ctx, arg, arg2):
        set_up()
        bon = bounty(arg)
        bon.cooldown_set(arg2)
        chan = self.bot.get_channel(cd)
        await ctx.send(f"set bounty {arg} cooldown to {arg2}")
        await mbounty(chan)

    @commands.hybrid_command(name="sunday_routine", description="refresh bounty cd and distribution reward")
    @commands.has_role(mod_id)
    async def sunday_routine(self, ctx):
        ch = self.bot.get_channel(cd)
        set_up()
        mod = moderator()
        mod.bounty_refresh()
        mod.del_dist()
        await mbounty(ch)
        ctx.send("bounty refreshed and whipe up distribution reward")

    @commands.hybrid_command(name="refresh_bounty", description="refresh bounty cd")
    @commands.has_role(mod_id)
    async def refresh_bounty(self, ctx):
        await ctx.interaction.response.defer()
        ch = self.bot.get_channel(cd)
        set_up()
        mod = moderator()
        mod.bounty_refresh()
        await mbounty(ch)
        await ctx.send("bounty refreshed")

    @commands.hybrid_command(name="reset_person_bounty", description="refresh one person cd bounty")
    @commands.has_role(mod_id)
    async def reset_cd(self, ctx, player: str):
        await ctx.interaction.response.defer()
        did = re.findall("<@!?([0-9]+)>", player)[0]
        gac = gacha(did)
        gac.set_bbq_time(0)
        await ctx.send(f"succesfully change last clear for <@{did}> to None")

    @commands.hybrid_command(name="reset_cd_bounty_all", description="refresh all person cd bounty")
    @commands.has_role(mod_id)
    async def reset_cd_all(self, ctx):
        await ctx.interaction.response.defer()
        for i in moderator.disc_all():
            gac = gacha(i)
            gac.set_bbq_time(0)
        await ctx.send(f"succesfully change all player last clear to None")


async def setup(bot):
    await bot.add_cog(Bounty_Event(bot))
