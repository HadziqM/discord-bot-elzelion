import discord
import urllib3
import cv2
import numpy as np
from discord.ext import commands
from discord.utils import get
from datetime import datetime as dt
from direc import *
from base import *

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
    url = str(user.avatar_url)
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
    embed.set_thumbnail(url=user.avatar_url)
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
    embed.set_thumbnail(url=aser.avatar_url)
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
    road = get(ctx.guild.roles, id=int(main.road))
    elze = get(ctx.guild.roles, id=int(main.elze))
    champion = get(ctx.guild.roles, id=int(main.champion))
    master = get(ctx.guild.roles, id=int(main.master))
    expert = get(ctx.guild.roles, id=int(main.expert))
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
        await chan.send(f"congratulation <@{user.id}> you are promoted to **Bounty Master** for reaching 200k bounty point")
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


class Bounty_Event(commands.Cog):
    """ Participate bounty to get generous reward """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(mod_id)
    async def test(self, ctx):
        set_up()
        char = character('843')
        await ctx.send(char.title)

    @commands.command()
    async def bounty_list(self, ctx):
        chan = ctx.channel
        await mbounty(chan)

    @commands.command()
    @commands.has_role(mod_id)
    async def announce(self, ctx, *arg):
        async for message in ctx.channel.history(limit=1):
            await message.delete()
        date = int(dt.timestamp(dt.now()))
        bot = self.bot
        ch = bot.get_channel(anc)
        ch1 = bot.get_channel(cd)
        ch2 = bot.get_channel(lead)
        ch3 = bot.get_channel(promo)
        ch4 = bot.get_channel(1009415908927733811)
        set_up()
        bon = bounty(arg[0])
        if bon.cooldown == 0:
            await ctx.send("cooldown")
            return
        if len(arg) <= 2:
            await ctx.send('missing argument')
        embed = discord.Embed(title=arg[0], color=discord.Color.green())
        file = discord.File(
            f'{BOUNTY_PATH}\\{arg[0]}.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        embed.set_image(url=arg[1])
        if len(arg) == 3:
            did = int(arg[2][2:-1])
            try:
                cid = check_disc(did)
            except:
                await ctx.send(
                    f'<@{did}> you need to register first to participate bounty')
                return
            a = bon.announce_now('solo', cid)
            user = await bot.fetch_user(int(a[0]))
            embed.set_author(name=user.display_name, icon_url=user.avatar_url)
            embed.add_field(name=a[1], value=f'Cleared: Solo \n<t:{date}:F>')
            if a[-1] == 0:
                await ctx.send(f"<@{user.id}> since reward for current bounty is too much, it cant be distributed in game trough normal mean, coordinate with EVE to get your reward")
            else:
                await ctx.send(f"<@{user.id}> reward already distributed, claim it before bounty white day")
            await mpromote(ctx, a[-2], ctx.guild.get_member(int(a[0])), ch3, cid)
        elif arg[3] == 'npc':
            did = int(arg[2][2:-1])
            try:
                cid = check_disc(did)
            except:
                await ctx.send(
                    f'<@{did}> you need to register first to participate bounty')
                return
            a = bon.announce_now('cat', cid)
            user = await bot.fetch_user(int(a[0]))
            embed.set_author(name=user.display_name, icon_url=user.avatar_url)
            embed.add_field(
                name=a[1], value=f'Cleared: Multiplayer With NPC \n<t:{date}:F>')
            if a[-1] == 0:
                await ctx.send(f"<@{user.id}> since reward for current bounty is too much, it cant be distributed in game trough normal mean, coordinate with EVE to get your reward")
            else:
                await ctx.send(f"<@{user.id}> reward already distributed, claim it before bounty white day")
            await mpromote(ctx, a[-2], ctx.guild.get_member(int(a[0])), ch3, cid)
        elif len(arg) >= 4:
            cid = []
            for i in range(len(arg)-2):
                did = int(arg[i+2][2:-1])
                try:
                    cidi = check_disc(did)
                except:
                    ctx.send(
                        f'<@{did}> you need to register first to participate bounty')
                    return
                cid.append(cidi)
            a, b, c, d = bon.announce_now('multi', cid)
            embed.add_field(
                name='TEAM', value=f'Cleared: Multiplayer \n<t:{date}:F>', inline=False)
            for i in range(len(cid)):
                user = await bot.fetch_user(int(a[i]))
                embed.add_field(
                    name=b[i], value=f'Discord: {user}', inline=False)
                if c[i] == 0:
                    await ctx.send(f"<@{user.id}> since reward for current bounty is too much, it cant be distributed in game trough normal mean, coordinate with EVE to get your reward")
                else:
                    await ctx.send(f"<@{user.id}> reward already distributed, claim it before bounty white day")
                await mpromote(ctx, d[i], ctx.guild.get_member(int(a[i])), ch3, cid[i])
        else:
            return
        await ch.send(file=file, embed=embed)
        await mbounty(ch1)
        await mleaderboard(bot, ch2, ch4)

    @commands.command()
    @commands.has_role(mod_id)
    async def debt(self, ctx):
        set_up()
        mod = moderator()
        a = mod.bounty_all()
        embed = discord.Embed(title="Debt list", color=discord.Color.green())
        file = discord.File(
            f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        for i in range(len(a)):
            bon = bounty(a[i])
            embed.add_field(
                name=a[i], value=f'Solo: {bon.solo_debt()} \nMulti: {bon.multi_debt()}')
        await ctx.channel.send(file=file, embed=embed)

    @commands.command()
    @commands.has_role(mod_id)
    async def cooldown(self, ctx, arg, arg2):
        set_up()
        bon = bounty(arg)
        bon.cooldown_set(arg2)
        chan = self.bot.get_channel(cd)
        await ctx.send(f"set bounty {arg} cooldown to {arg2}")
        await mbounty(chan)


def setup(bot):
    bot.add_cog(Bounty_Event(bot))
