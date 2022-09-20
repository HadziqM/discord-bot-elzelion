from direc import *
from base import *
import discord


icon1 = ['\\GS.png', '\\HS.png', '\\H.png', '\\L.png', '\\SS.png', '\\LB.png', '\\DS.png',
         '\\LS.png', '\\HH.png', '\\GL.png', '\\B.png', '\\T.png', '\\SAF.png', '\\MS.png']
icon = [ICON_PATH+icon1[i] for i in range(len(icon1))]


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
        name='Character', value=f'Gender : {f}\nHunter Rank : {g}\nGold Rank : {h}', inline=False)
    embed.add_field(
        name='Guild', value=f'Name : {d}\nGuild ID : {e}', inline=False)
    return await interact.response.send_message(file=file, embed=embed)


async def mevent(member, interact):
    user = member
    gac = gacha(member.id)
    mod = moderator()
    try:
        rank = mod.disc_all().index(str(member.id))+1
    except:
        rank = "No Rank"
    embed = discord.Embed(title="My Event Status",
                          description=f'Bounty Coin : {gac.bounty}\nGacha Ticket : {gac.ticket}\nPity Count : {gac.pity}\nLatest Bounty : {gac.bbq}\nTime Cleared : <t:{gac.bbq_time}:R>\nBounty Rank : {rank}', color=discord.Color.red())
    embed.set_author(name=user.display_name, icon_url=user.avatar)
    await interact.response.send_message(content=None, embed=embed)
