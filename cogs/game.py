import random
import discord
import numpy as np
from discord.ext import commands
from direc import *
from base import *
from board import *

db = database()

card = [1, 2, 3, 4, 5, 6, 7, 8, 9]
ch1 = int(db.p1)
ch2 = int(db.p2)
an = int(db.game)
role1 = int(db.rolep1)
role2 = int(db.rolep2)


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
            x.append("redraw")
        elif i == 9:
            x.append("draw")
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
                            try:
                                if int(i) in deck:
                                    None
                                else:
                                    return False
                            except:
                                return False
                        return True
                    elif '&go' in message.content.lower():
                        if len(message.content[4:].split(',')) > 3:
                            return False
                        for i in message.content[4:].split(','):
                            try:
                                if int(i) in deck:
                                    None
                                else:
                                    return False
                            except:
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
                            try:
                                if int(i) in deck:
                                    None
                                else:
                                    return False
                            except:
                                return False
                        return True
                    elif '&go' in message.content.lower():
                        if len(message.content[4:].split(',')) > 3:
                            return False
                        for i in message.content[4:].split(','):
                            try:
                                if int(i) in deck:
                                    None
                                else:
                                    return False
                            except:
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


async def purge(a, channel):
    async for message in channel.history(limit=a):
        await message.delete()


class Minigame_Event(commands.Cog):
    """ Next Minigame Event WIP """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def game(self, ctx):
        role1 = await ctx.guild.create_role(name='player1')
        role2 = await ctx.guild.create_role(name='player2')
        await ctx.message.author.remove_roles(role1)
        await ctx.message.author.remove_roles(role2)
        await ctx.send("removed")

    @commands.command()
    async def lucky7(self, ctx, arg):
        a = ctx.message.author.id
        set_up()
        try:
            cid = check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        char = character(cid)
        if char.bounty < int(arg):
            await ctx.send("you dont have enough bounty coin")
            return
        bg = cv2.imread(CARD_PATH+"\\board.jpg", cv2.IMREAD_UNCHANGED)
        bg = cv2.cvtColor(bg, cv2.COLOR_BGRA2BGR)
        board = put_text(arg, bg)
        brd = board.copy()
        remain = 7
        deck = [3, 4, 5, 6, 7, 8, 9]
        while True:
            brd = board.copy()
            for i in range(remain):
                brd = card_slot(brd, card_list[9], card_pos(i))
            cv2.imwrite("board.jpg", brd)
            await ctx.send(file=discord.File("board.jpg"))
            await ctx.send(f"pick one 1-{remain}")

            def check(author, remain):
                def inner_check(message):
                    if message.author != author:
                        return False
                    else:
                        try:
                            x = int(message.content)
                            if 0 < x <= remain:
                                return True
                            else:
                                return False
                        except:
                            return False
                return inner_check
            msg = await self.bot.wait_for('message', check=check(ctx.author, remain))
            random.shuffle(deck)
            choice = int(msg.content) - 1
            brd = card_slot(brd, card_list[deck[choice]-1], card_pos(choice))
            cv2.imwrite("board.jpg", brd)
            await ctx.send(file=discord.File("board.jpg"))
            if deck[choice] == 9:
                remain -= 1
                if remain == 2:
                    await ctx.send("sorry you lose the game but you didnt lose coin since your insane luck to draw d card 7 times lol")
                    brd = card_slot(brd, card_list[6], card_pos(deck.index(7)))
                    cv2.imwrite("board.jpg", brd)
                    await ctx.send(file=discord.File("board.jpg"))
                    break
                deck.remove(9-remain)
                await ctx.send(f"you got another try with {remain} card\nand you got {int(arg)} bounty coin as bonus for getting **D** card")
                char.add_bounty(int(arg))
            elif deck[choice] == 8:
                await ctx.send(f"you got another try with {remain} card\nand you got {int(arg)*2} bounty coin as bonus for getting **R** card")
                char.add_bounty(int(arg)*2)
            elif deck[choice] == 7:
                await ctx.send(f"congrats you won the game, you win {int(arg)*7} Bounty Coin")
                char.add_bounty(int(arg)*7)
                break
            else:
                await ctx.send(f"sorry you lose the game, you lose {arg} Bounty Coin")
                brd = card_slot(brd, card_list[6], card_pos(deck.index(7)))
                cv2.imwrite("board.jpg", brd)
                await ctx.send(file=discord.File("board.jpg"))
                char.set_bounty(char.bounty-int(arg))
                break

    @commands.command()
    async def match(self, ctx, arg):
        p1 = ctx.message.author
        p2 = ctx.guild.get_member(int(arg[2:-1]))
        role1 = await ctx.guild.create_role(name='player1')
        role2 = await ctx.guild.create_role(name='player2')
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
        await p1.add_roles(role1)
        await p2.add_roles(role2)
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
        await p1.remove_roles(role1)
        await p2.remove_roles(role2)
        await purge(200, channel1)
        await purge(200, channel2)


def setup(bot):
    bot.add_cog(Minigame_Event(bot))
