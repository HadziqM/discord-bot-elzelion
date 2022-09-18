import discord
import urllib3
import cv2
import numpy as np
from discord.ext import commands
from discord.utils import get
from datetime import datetime as dt
from direc import *
from base import *
from discord.ui import View

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
        for i in range(int(length/2)):
            user = await bot.fetch_user(int(a[i]))
            embed.add_field(
                name=a[i+length], value=f'Discord: {user}', inline=False)
    return await ch.send(file=file, embed=embed)


class MyView(View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def malebutton(self, interaction, button):
        await interaction.response.edit_message(view=self)
        self.value = "y"
        self.stop()

    @discord.ui.button(label="Not Approve", style=discord.ButtonStyle.red)
    async def femalebutton(self, interaction, button):
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.value = "n"
        self.stop()


class Bounty_Event(commands.Cog):
    """ Participate bounty to get generous reward """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bounty_list(self, ctx):
        chan = ctx.channel
        await mbounty(chan)

    @commands.command()
    async def test(self, ctx):
        ch = self.bot.get_channel(anc)
        set_up()
        char = character(check_disc(ctx.author.id))
        await mannounce(self.bot, ch, [ctx.author.id, char.name], ["BBQ03", "https://cdn.discordapp.com/attachments/940326599474163752/1020921647944962079/Untitled6.png"], "solo")

    @commands.hybrid_command(name="submit_solo", description="submit your bounty application to admin")
    async def submit_solo(self, ctx: commands.Context, bbq: str, picture: str):
        bot = self.bot
        ch = bot.get_channel(1020947766203129876)
        ch1 = bot.get_channel(cd)
        set_up()
        bon = bounty(bbq)
        if bon.cooldown == 0:
            await ctx.send("cooldown")
            return
        did = ctx.author.id
        try:
            cid = check_disc(did)
        except:
            await ctx.send(
                f'<@{did}> you need to register first to participate bounty')
            return
        await ctx.send("submitted your form\nwait for admin aproval")
        char = character(cid)
        bon.cooldown_now()
        await mbounty(ch1)
        await self.appoval_s(ctx, bon, ch, ch1, did, bbq, picture, char.name)

    async def appoval_s(self, ctx, bon, ch, ch1, did, bbq, picture, name):
        bot = self.bot
        await ch.send("poeple submited a bounty solo")
        confirm = await mannounce(bot, ch, [did, name], [bbq, picture], "solo")
        view = MyView(ctx)
        msg = await ch.send(view=view)
        await view.wait()
        if view.value == 'y':
            await self.announce(ctx, bbq, picture, '<@'+str(did)+'>')
            await ctx.send(f"<@{did}> your bounty had been approved")
        elif view.value == 'n':
            await ctx.send(f"<@{did}> your bounty isnt approved")
            set_up()
            bon.cooldown_set(bon.cooldown+1)
            await mbounty(ch1)
        await msg.delete()
        await confirm.delete()

    @commands.hybrid_command(name="submit_npc", description="submit your bounty application to admin")
    async def submit_npc(self, ctx, bbq: str, picture: str):
        bot = self.bot
        ch = bot.get_channel(1020947766203129876)
        ch1 = bot.get_channel(cd)
        set_up()
        bon = bounty(bbq)
        if bon.cooldown == 0:
            await ctx.send("cooldown")
            return
        did = ctx.author.id
        try:
            cid = check_disc(did)
        except:
            await ctx.send(
                f'<@{did}> you need to register first to participate bounty')
            return
        char = character(cid)
        bon.cooldown_now()
        await mbounty(ch1)
        await ch.send("poeple submited a bounty solo with npc")
        confirm = await mannounce(bot, ch, [did, char.name], [bbq, picture], "npc")
        view = MyView(ctx=ctx)
        msg = await ch.send(view=view)
        await ctx.send("submitted your form, wait for admin aproval")
        await view.wait()
        if view.value == 'y':
            await self.announce(ctx, bbq, picture, '<@'+str(did)+'>', "npc")
            await ctx.send(f"<@{did}> your bounty had been approved")
        elif view.value == 'n':
            await ctx.send(f"<@{did}> your bounty isnt approved")
            set_up()
            bon.cooldown_set(bon.cooldown+1)
            await mbounty(ch1)
        await msg.delete()
        await confirm.delete()

    @commands.hybrid_command(name="submit_multi", description="submit your bounty application to admin")
    async def submit_multi(self, ctx, bbq: str, picture: str, second_party: str, third_party: str, fourth_party: str):
        bot = self.bot
        ch = bot.get_channel(1020947766203129876)
        ch1 = bot.get_channel(cd)
        set_up()
        bon = bounty(bbq)
        if bon.cooldown == 0:
            await ctx.send("cooldown")
            return
        arg = [second_party, third_party, fourth_party]
        did = [ctx.author.id]
        cid = []
        try:
            cid.append(check_disc(did[0]))
        except:
            await ctx.send(f'<@{did[0]}> you need to register first to participate bounty')
            return
        for i in arg:
            try:
                didi = int(i[2:-1])
                did.append(didi)
                try:
                    cidi = check_disc(i)
                    cid.append(cidi)
                except:
                    await ctx.send(
                        f'<@{didi}> you need to register first to participate bounty')
                    return
            except:
                None
        if len(did) == 1:
            await ctx.send("use submit_npc instead")
            return
        bon.cooldown_now()
        await mbounty(ch1)
        anjir = [i for i in cid]
        for i in cid:
            char = character(cid)
            anjir.append(char.name)
        await ch.send("poeple submited a bounty solo with npc")
        confirm = await mannounce(bot, ch, anjir, [bbq, picture], "multi")
        view = MyView(ctx=ctx)
        msg = await ch.send(view=view)
        await ctx.send("submited your form, wait for admin aproval")
        await view.wait()
        if view.value == 'y':
            if len(did) == 2:
                await self.announce(ctx, bbq, picture, '<@'+str(did[0])+'>', '<@'+str(did[1])+'>')
            elif len(did) == 3:
                await self.announce(ctx, bbq, picture, '<@'+str(did[0])+'>', '<@'+str(did[1])+'>', '<@'+str(did[2])+'>')
            elif len(did) == 4:
                await self.announce(ctx, bbq, picture, '<@'+str(did[0])+'>', '<@'+str(did[1])+'>', '<@'+str(did[2])+'>', '<@'+str(did[3])+'>')
            await ctx.send(f"<@{did}> your bounty had been approved")
        elif view.value == 'n':
            await ctx.send(f"<@{did}> your bounty isnt approved")
            set_up()
            bon.cooldown_set(bon.cooldown+1)
            await mbounty(ch1)
        await msg.delete()
        await confirm.delete()

    @commands.command()
    @commands.has_role(mod_id)
    async def announce(self, ctx, *arg):
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
        if len(arg) == 3:
            did = int(arg[2][2:-1])
            try:
                cid = check_disc(did)
            except:
                await ctx.send(
                    f'<@{did}> you need to register first to participate bounty')
                return
            a = bon.announce_now('solo', cid)
            if a[-1] == 0:
                await ctx.send(f"<@{did}> since reward for current bounty is too much, it cant be distributed in game trough normal mean, coordinate with EVE to get your reward")
            else:
                await ctx.send(f"<@{did}> reward already distributed, claim it before bounty white day")
            await mpromote(ctx, a[-2], ctx.guild.get_member(int(a[0])), ch3, cid)
            await mannounce(bot, ch, a, [arg[0], arg[1]], "solo")
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
            if a[-1] == 0:
                await ctx.send(f"<@{user.id}> since reward for current bounty is too much, it cant be distributed in game trough normal mean, coordinate with EVE to get your reward")
            else:
                await ctx.send(f"<@{user.id}> reward already distributed, claim it before bounty white day")
            await mpromote(ctx, a[-2], ctx.guild.get_member(int(a[0])), ch3, cid)
            await mannounce(bot, ch, a, [arg[0], arg[1]], "npc")
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
            for i in range(len(cid)):
                a.append(b[i])
                if c[i] == 0:
                    await ctx.send(f"<@{a[i]}> since reward for current bounty is too much, it cant be distributed in game trough normal mean, coordinate with EVE to get your reward")
                else:
                    await ctx.send(f"<@{a[i]}> reward already distributed, claim it before bounty white day")
                await mpromote(ctx, d[i], ctx.guild.get_member(int(a[i])), ch3, cid[i])
            await mannounce(bot, ch, a, [arg[0], arg[1]], "multi")
        else:
            return
        await mbounty(ch1)
        await mleaderboard(bot, ch2, ch4)

    @commands.command()
    @commands.has_role(mod_id)
    async def cooldown(self, ctx, arg, arg2):
        set_up()
        bon = bounty(arg)
        bon.cooldown_set(arg2)
        chan = self.bot.get_channel(cd)
        await ctx.send(f"set bounty {arg} cooldown to {arg2}")
        await mbounty(chan)


async def setup(bot):
    await bot.add_cog(Bounty_Event(bot))
