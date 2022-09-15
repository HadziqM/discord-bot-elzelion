from direc import *
from base import *
import cv2
import urllib3
import discord
import random
import numpy as np
from discord.ext import commands

main = database()
mod_id = int(main.mod)
hertz = 455622761168109569

UR = ["Divine Excalibur", "True Kusanagi-no-Tsurugi"]
SSR1 = ["Flag of the Saint VI", "Fake Projection Spiral VII", "Nameless Dagger(Black) VII", "Nameless Dagger VII", "Ea Black Diverged Sword VII", "Ea Diverged Air Sword VII",
        "Golden Victory Sword VII", "Kanshou and Bakuya VII", "Sword of Promised Victory VII", "6921 Fate Armor Set01", "221C Fate Armor Set02"]
SSR2 = ["4339 Fate Armor Set03", "383A Fate Armor Set04",
        "393A Fate Armor Set05", "9C2C Fate Armor Set06"]
SR1 = ["Hiden Stamp Sns x5", "Hiden Stamp DS x5", "Hiden Stamp GS x5", "Hiden Stamp LS x5", "Hiden Stamp Hammer x5", "Hiden Stamp HH x5", "Hiden Stamp Lance x5",
       "Hiden Stamp GL x5", "Hiden Stamp Swaxe x5", "Hiden Stamp Tonfa x5", "Hiden Stamp MS x5", "Hiden Stamp LBG x5", "Hiden Stamp HBG x5", "Hiden Stamp Bow x5"]
SR2 = ["Divine Power Gem x200", "Shiten Tkt x100", "Upper Shiten key x10", "NP SnS Mat x50",
       "NP DS Mat x50", "NP Swaxe Mat x50"]
SR3 = ["Divine Power Gem x150", "Shiten Tkt x50", "Shiten key x10"]
R1 = ["Quick Mega Potion x25", "Ancient Potion x10"]
R2 = ["Dung x999", "Potion x10"]

rlist = [SSR1, SSR2, SR1, SR2, SR3, R1, R2]
for i in range(7):
    random.shuffle(rlist[i])


def rarity(gac):
    x = random.random()
    if x <= 0.001:
        gac.set_pity(0)
        return random.choice(UR), jpg("ur.jpg")
    elif 0.05 >= x > 0.001:
        gac.set_pity(0)
        return SSR(random.random()), jpg("ssr.jpg")
    elif 0.35 >= x > 0.05:
        return SR(random.random()), jpg("sr.jpg")
    else:
        return R(random.random()), jpg("r.jpg")


def guaranted():
    x = random.random()
    if x <= 0.02:
        return UR, jpg("ur.jpg")
    else:
        return SSR(random.random()), jpg("ssr.jpg")


def jpg(x):
    return (GACHA_PATH+"\\"+x)


def SSR(x):
    if x <= 0.167:
        return random.choice(SSR1)
    else:
        return random.choice(SSR2)


def SR(x):
    if x <= 0.167:
        return random.choice(SR1)
    elif 0.5 >= x > 0.167:
        return random.choice(SR2)
    else:
        return random.choice(SR3)


def R(x):
    if x <= 0.4:
        return random.choice(R1)
    else:
        return random.choice(R2)


async def mtest(did, ctx, bot, arg):
    user = await bot.fetch_user(did)
    gac = gacha(did)
    destiny = gac.pull()
    char = character(arg)
    if int(did) == hertz:
        text, jpg = guaranted()
    else:
        if destiny == 1:
            text, jpg = rarity(gac)
        elif destiny == 2:
            text, jpg = guaranted()
        else:
            return await ctx.send("insufficient gacha ticket")
    gac.reward(arg, text)
    bg = cv2.imread(jpg, cv2.IMREAD_UNCHANGED)
    top = 518
    left = 136
    wid = 500
    hei = 50
    d = 100
    r = int(d/2)
    center = (98, 388)
    roi = bg[(center[0]-r):(center[0]+r), (center[1]-r):(center[1]+r)]
    font = cv2.FONT_HERSHEY_DUPLEX
    size = cv2.getTextSize(text, font, 1, 1)[0]
    x = int((wid - size[0])/2 + left)
    y = int((hei + size[1])/2 + top)
    cv2.putText(bg, text, (x, y), font, 1, (255, 255, 255), 1)
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
    mask1 = cv2.circle(mask1, (r, r), r, (255, 255, 255), -1)
    mask2 = 255-mask1
    roi = cv2.bitwise_and(roi, roi, mask=mask2[:, :, 0])
    img = cv2.bitwise_and(img, img, mask=mask1[:, :, 0])
    res = cv2.add(roi, img)
    bg[(center[0]-r):(center[0]+r), (center[1]-r):(center[1]+r)] = res
    cv2.imwrite("text.jpg", bg)
    embed = discord.Embed(
        title='Congratulation', description='Reward already distributed, check in game', color=discord.Color.green())
    file = discord.File(f'text.jpg', filename='prom.jpg')
    embed.set_image(url='attachment://prom.jpg')
    embed.add_field(
        name=char.name, value=f"Remaining Ticket :{gac.ticket}\nPity Count :{gac.pity}")
    await ctx.send(file=file, embed=embed)


async def mevent(ctx, did, bot):
    user = await bot.fetch_user(did)
    gac = gacha(did)
    embed = discord.Embed(title="My Event Status",
                          description=f'Bounty Coin : {gac.bounty}\nGacha Ticket : {gac.ticket}\nPity Count : {gac.pity}', color=discord.Color.red())
    embed.set_author(name=user.display_name, icon_url=user.avatar_url)
    await ctx.channel.send(content=None, embed=embed)


class Gacha_Event(commands.Cog):
    """ Register to get free 10 try of gacha """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
        a = ctx.message.author.id
        set_up()
        try:
            arg = check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        await mtest(a, ctx, self.bot, arg)

    @commands.command()
    async def mygacha(self, ctx):
        a = ctx.message.author.id
        set_up()
        try:
            check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        await mevent(ctx, a, self.bot)

    @commands.command()
    async def buy_ticket(self, ctx, arg):
        a = ctx.message.author.id
        set_up()
        try:
            check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        gac = gacha(a)
        res = gac.buy(int(arg))
        if res == 0:
            await ctx.send("not enough bounty coin")
        else:
            await ctx.send(f"successfully bought {str(arg)} ticket ")


def setup(bot):
    bot.add_cog(Gacha_Event(bot))
