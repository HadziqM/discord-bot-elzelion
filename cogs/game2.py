import random
import numpy as np
from discord.ext import commands
from direc import *
from base import *

db = database()

card = [1, 2, 3, 4, 5, 6, 7, 8, 9]
ch1 = int(db.p1)
ch2 = int(db.p2)
an = int(db.game)


def draw(deck, x):
    if len(deck)+x > 10:
        x = len(deck)+x-10
    for i in range(x):
        deck.append(random.choice(card))
    deck.sort()
    return deck


def prin(deck):
    x = []
    for i in deck:
        if i == 8:
            x.append("Redraw")
        elif i == 9:
            x.append("Draw")
        else:
            x.append(i)
    return x


def redraw(deck, throw):
    try:
        for i in throw:
            deck.remove(int(i))
        draw(deck, len(throw))
        deck.sort()
        return deck
    except:
        deck.sort()
        return deck


def forward(deck, select):
    for i in select:
        deck.remove(i)
    deck.sort()
    return deck


def result(attack, defense):
    if attack-defense >= 0:
        return attack-defense
    else:
        return 0


async def turn1(bot, channel1, ann, deck1):
    while True:
        def check1(channel, deck):
            def inner_check(message):
                if message.channel != channel:
                    return False
                else:
                    if message.content == '&draw' and 9 in deck:
                        return True
                    elif '&redraw' in message.content.lower() and 8 in deck:
                        for i in message.content[8:].split(','):
                            if int(i) in deck:
                                None
                            else:
                                return False
                        return True
                    elif '&go' in message.content.lower():
                        if len(message.content[4:].split(',')) > 3:
                            return False
                        for i in message.content[4:].split(','):
                            if int(i) in deck:
                                None
                            else:
                                return False
                        return True
            return inner_check

        tp1 = await bot.wait_for('message', check=check1(channel1, deck1))
        if '&draw' in tp1.content.lower():
            deck1.remove(9)
            await ann.send("p1 draw 3 cards")
            await channel1.send(prin(draw(deck1, 3)))
        elif '&redraw' in tp1.content.lower():
            deck1.remove(8)
            await ann.send(f"p1 redraw {len(tp1.content[8:].split(','))} cards")
            await channel1.send(prin(redraw(deck1, tp1.content[8:].split(','))))
        else:
            await ann.send("p1 end turn")
            a = [int(i) for i in tp1.content[4:].split(',')]
            await channel1.send(prin(forward(deck1, a)))
            break
    return sum(a)


async def turn2(bot, channel2, ann, deck2):
    while True:
        def check2(channel, deck):
            def inner_check(message):
                if message.channel != channel:
                    return False
                else:
                    if message.content == '&draw' and 9 in deck:
                        return True
                    elif '&redraw' in message.content.lower() and 8 in deck:
                        for i in message.content[8:].split(','):
                            if int(i) in deck:
                                None
                            else:
                                return False
                        return True
                    elif '&go' in message.content.lower():
                        if len(message.content[4:].split(',')) > 3:
                            return False
                        for i in message.content[4:].split(','):
                            if int(i) in deck:
                                None
                            else:
                                return False
                        return True
            return inner_check
        tp2 = await bot.wait_for('message', check=check2(channel2, deck2))
        if '&draw' in tp2.content.lower():
            deck2.remove(9)
            await ann.send("p2 draw 3 cards")
            await channel2.send(prin(draw(deck2, 3)))
        elif '&redraw' in tp2.content.lower():
            deck2.remove(8)
            await ann.send(f"p2 redraw {len(tp2.content[8:].split(','))} cards ")
            await channel2.send(prin(redraw(deck2, tp2.content[8:].split(','))))
        else:
            await ann.send("p2 end turn")
            a = [int(i) for i in tp2.content[4:].split(',')]
            await channel2.send(prin(forward(deck2, a)))
            break
    return sum(a)


class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def game(self, ctx):
        await ctx.send("tested")

    @commands.command()
    async def match(self, ctx, arg):
        p1 = ctx.message.author
        p2 = ctx.guild.get_member(int(arg[2:-1]))
        hp1 = 40
        hp2 = 40
        deck1 = []
        deck2 = []
        channel1 = self.bot.get_channel(ch1)
        channel2 = self.bot.get_channel(ch2)
        announce = self.bot.get_channel(an)
        await announce.send("begin match")
        if random.random() >= 0.5:
            await announce.send(f"<@{p1.id}> attcaking first")
        else:
            await announce.send(f"<@{p2.id}> attcaking first")
            p3 = p1
            p1 = p2
            p2 = p3
        await channel1.send(f'your turn now **attack**\n{prin(draw(deck1,6))}\n HP = {hp1}')
        await channel2.send(f'{prin(draw(deck2,6))}\n HP = {hp2}')
        while True:
            attacker = await turn1(self.bot, channel1, announce, deck1)
            await channel2.send("your turn now **defense**")
            defense = await turn2(self.bot, channel2, announce, deck2)
            dmg = result(attacker, defense)
            hp2 = result(hp2, dmg)
            await announce.send(f"p1 inflicted {dmg} damage, p2 has {hp2} HP remaining")
            if hp2 == 0:
                await announce.send(f"winner is <@{p1.id}>")
                break
            await channel1.send(f'your turn now **defense**\n{prin(draw(deck1,2))}\n HP = {hp1}')
            await channel2.send(f'{prin(draw(deck2,2))}\n HP = {hp2}')
            defense = await turn1(self.bot, channel1, announce, deck1)
            await channel2.send("your turn now **attack**")
            attacker = await turn2(self.bot, channel2, announce, deck2)
            dmg = result(attacker, defense)
            hp1 = result(hp1, dmg)
            await announce.send(f"p2 inflicted {dmg} damage, p1 has {hp1} HP remaining")
            if hp1 == 0:
                await announce.send(f"winner is <@{p1.id}>")
                break
            await channel1.send(f'your turn now **attack**\n{prin(draw(deck1,2))}\n HP = {hp1}')
            await channel2.send(f'{prin(draw(deck2,2))}\n HP = {hp2}')


async def setup(bot):
    await bot.add_cog(GameCog(bot))
