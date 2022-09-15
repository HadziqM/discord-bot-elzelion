import discord
from discord.ext import commands
from direc import *


class Guide_Help(commands.Cog):
    """ list of all guides, you can request by DM me (yes me elzelion) """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register_guide(self, ctx):
        embed = discord.Embed(title='Register Guide',
                              color=discord.Color.green())
        file = discord.File(
            f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        embed.set_image(
            url='https://media.discordapp.net/attachments/1009291538733482055/1009300004894162984/register.gif')
        embed.add_field(name='Info', value='register feature allow us to bind our discord profile to our charachter in game,\nby registering you could get access to varius feature available in our discord server and in game', inline=False)
        embed.add_field(name='Requirements', value='before you could use register you need to have an account on the rain server and make charachter on it untill successfully enter mezeporta', inline=False)
        embed.add_field(name='How to', value='first serach your character id on <#965634820367601714> by using command\n*!rain id <your character name>*.\nkeep note that character name is the name of your character in game and not your username used to login into launcher\n\nafter you know your character id you could register by using command\n*!rain register <your character id> <gender>*.\n gender refer to your character gender in game, use m for male and f for female', inline=False)
        await ctx.channel.send(file=file, embed=embed)

    @commands.command()
    async def transfer_guide(self, ctx):
        embed = discord.Embed(title='Save Transfer Guide',
                              color=discord.Color.green())
        file = discord.File(
            f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        embed.set_image(
            url='https://media.discordapp.net/attachments/1009291538733482055/1009299962225508452/savefile.gif')
        embed.add_field(
            name='Info', value='save transfer allow us to resume your progression in another server by transfering your savedata', inline=False)
        embed.add_field(
            name='Requirements', value='this feature only accessable for registered player, use *!rain register_guide* to see how to register', inline=False)
        embed.add_field(name='How to', value='first you need to locate your savedata and partner data (optional), if youare playing on local server, the backup save is located on C:\\Erupe\savedata\<your character name>, get the latest date modified savedata.bin and partner.bin.\n\nafter that rename those file to our format\n\n*savedata_rain.bin*\n*partner_rain.bin*\n\nafter that DM <@999140410783957002> your file one by one.\nbot will reply if the transfer is success', inline=False)
        await ctx.channel.send(file=file, embed=embed)

    @commands.command()
    async def bounty_guide(self, ctx):
        embed = discord.Embed(title='Bounty Guide',
                              color=discord.Color.green())
        file = discord.File(
            f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        embed.add_field(
            name='Info', value='bounty is our server main event, there are various bounty quest you can take with really generous reward', inline=False)
        embed.add_field(
            name='Requirements', value='you need to be registered on server', inline=False)
        embed.add_field(name='How to Participate', value='first you need to know our bounty rules that stated on <#962864233371021342>.\n you can see various quest you can take on <#962712664180654090>, pick one that suit you but please read the requirement carefully before deciding\n\ncheck if bounty is still availabe to take on <#1004686730479292447>.\nafter that just do the quest in game, after you successfully beat the main objectives, screensoot your equipment on quest completion then send it to <#940326599474163752>.\ndont forget to ping <@&937306936939020309> and state the bounty title you take\n\nafter that just let us judge your bonty, if its valid then bot will ping you about the reward.\n\nto see your reward just hop into game and talk to guide lady near enterance', inline=False)
        embed.add_field(name='Bounty Coin', value='beside ingame reward you also got bounty coin which is separated from game feature.\n\nbounty coin will be usefull for upcoming server event and you could also participate bounty leaderboard with it.\ndepending on your achievement you could get promoted and given title at <#1005816626425380944>.\n\nthe title will further boost your bounty coin gain depending on title you had', inline=False)
        await ctx.channel.send(file=file, embed=embed)

    @commands.command()
    async def lucky7_guide(self, ctx):
        embed = discord.Embed(title='Lucky7 Guide',
                              color=discord.Color.green())
        file = discord.File(
            f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        embed.add_field(
            name='Info', value='in this minigame you need to guess card to play', inline=False)
        embed.add_field(
            name='Requirements', value='you need to have 10 gacha ticket to play', inline=False)
        embed.add_field(name='How to Play', value='Use\n*!rain lucky7*\nto play the game\n\nFirst bot will shuffle card and put 9 flipped card at deck, pick one of the flipped card\n\n> If the card you pick is 7, congrats you win 77 ticket\n\n> If the card you pick is 1-6, you lose the game, but you got corresponding ticket, eg. Card with value 1 will give you 1 ticket, 2 for two ticket etc.\n\n> If the card you pick is special card R its a retry card, you got 5 gacha ticket and can retry the game for free\n\n> If the card you pick is special card D its destiny card, you got your 10 ticket back and you can retry the game for free, also deck number will be lowered by 1 by removing lowest number card, eg. First time pick **D** will remove 1 ftom deck, second time is 2, etc.', inline=False)
        await ctx.channel.send(file=file, embed=embed)

    @commands.command()
    async def gamble_guide(self, ctx):
        embed = discord.Embed(title='Gamble Guide',
                              color=discord.Color.green())
        file = discord.File(
            f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        embed.add_field(
            name='Info', value='in this minigame you need to guess 2 card to play and got double amount of bet', inline=False)
        embed.add_field(
            name='Requirements', value='you need pay exact amount of gacha ticket you bet', inline=False)
        embed.add_field(name='How to Play', value='You can bet any amount of gacha ticket, eg. \n*!rain gamble 100*\nto bet 100 ticket\n\nBot will suffle card and place 2 flipped card on board, pick one of the flipped card\n\n> if you pick D card, congrats you will get double amount of ticket you bet\n\n> if you pick R card, sorry you lose the ticket you bet', inline=False)
        await ctx.channel.send(file=file, embed=embed)

    @commands.command()
    async def destiny_guide(self, ctx):
        embed = discord.Embed(title='Destiny Guide',
                              color=discord.Color.green())
        file = discord.File(
            f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        embed.add_field(
            name='Info', value='in this minigame you need to play with minimum of 2 poople and maximum of 10 poeple', inline=False)
        embed.add_field(
            name='Requirements', value='you need pay exact amount of gacha ticket you bet', inline=False)
        embed.add_field(name='How to Play', value='You can challange minimum of one people and maximum of 9 (its 10 player max including challanger) and make sure all people have sufficient amount of ticket bet \neg.\n*!rain destiny @a @b 100*\nTo play with @a nad @b with 100 ticket bet\n\n(Pingging yourself didnt work, i know what youare thinking hehehe)\n\n> Bot will shuffle card and place flipped card on board, the amount of card is depending on player joined on game, pick one of the flipped card,\n\n> first come first serve, the one reply first got the choice taken first, if all player already pick the card available then its reveal time\n\n> if the card you pick is D card you are the winner amongs all player and you got all the ticket bet, eg. Play with 3 people will give you 3 times bet for the winner\n\n> if the card you pick is R, sorry you lose the ticket you bet', inline=False)
        await ctx.channel.send(file=file, embed=embed)

    @commands.command()
    async def feature_guide(self, ctx):
        embed = discord.Embed(
            title='List of feature', description='again, this feature only accessable for registered player', color=discord.Color.green())
        file = discord.File(
            f'{MISC_PATH}\\Rain_Server.png', filename='serv.png')
        embed.set_thumbnail(url='attachment://serv.png')
        embed.add_field(
            name='!rain mysave', value='you can use this command to make bot send your backup savedata on our server trough DM', inline=False)
        embed.add_field(name='!rain transmog',
                        value='use this to automatically make transmog unlocked in your character', inline=False)
        embed.add_field(name='!rain mycurrency',
                        value='this command let you see currency owned by you including bounty coin and Gcp', inline=False)
        embed.add_field(name='!rain join_guild <guild>',
                        value='input guild id or guid name after on <guild> to automatically join selected guild if its not full and youare not in any guild\nuse !rain guild to see guild that existed on rain server', inline=False)
        embed.add_field(name='!rain myboost', value='you could see the status of your login boost with this\n available mean its available to take\nactive mean its currently active\ncooldown mean its on cooldown or already used', inline=False)
        embed.add_field(name='!rain myboost_on',
                        value='this command will make all your login boost to available', inline=False)
        embed.add_field(name='!rain myboost_off',
                        value='this command will make all your login boost to cooldown', inline=False)
        await ctx.channel.send(file=file, embed=embed)

    @commands.command()
    async def game_guide(self, ctx):
        await ctx.channel.send('this is fist website guide')
        await ctx.channel.send('https://drive.google.com/drive/folders/1jTu0T3G_BH34vZud5z7_t8I6KcDRELzr')

    @commands.command()
    async def item_guide(self, ctx):
        await ctx.channel.send('search how to get your item in item index')
        await ctx.channel.send('https://xl3lackout.github.io/MHFZ-Ferias-English-Project/')

    @commands.command()
    async def weapon_guide(self, ctx):
        await ctx.channel.send('read this french guide')
        await ctx.channel.send('https://monsterhunterfrance-forumactif-com.translate.goog/f84-armes-mhfrontier?_x_tr_sl=fr&_x_tr_tl=en&_x_tr_hl=fr')
        await ctx.channel.send('watch this youtube channel')
        await ctx.channel.send('https://www.youtube.com/channel/UC75HC4hteGxmqMrs1j-jIUQ')

    @commands.command()
    async def poogie_guide(self, ctx):
        await ctx.channel.send(file=discord.File(f'{MISC_PATH}\\poogie.png'))

    @commands.command()
    async def diva_guide(self, ctx):
        await ctx.channel.send('this speadsheet about Diva, Hunter Guide, Halk Skills and My Mission')
        await ctx.channel.send('https://docs.google.com/spreadsheets/d/1nv-DrciRf3oNlcMgVzTXP-SLMNzU7yh09Oq0YWnfZRM/')

    @commands.command()
    async def monster_hp(self, ctx):
        await ctx.channel.send('this speadsheet of monster hunter current patch Health Bar')
        await ctx.channel.send('https://docs.google.com/spreadsheets/d/1U0A5oTth1aNYIu_5tlawzLBAC4447KGthpl5uMmyQm0/edit#gid=0')

    @commands.command()
    async def seph_guide(self, ctx):
        different = '''
```
Huge Change is the GRP Gains. If you look at the vanilla state then you notice that the highest GRP per quest you can get oustide of special event quests is 6000 for a Musou Hunt. That 6000 is not even 1 GR level beyond GR 31 so you probably see what a massive grind leveling was when you need to level 15 times to level 999 to have the full unlocked setup. this is obviously another huge MMORPG grind System left over and i changed all GRP gains on all G Rank quests. You will reach naturally by just playing through the G Rank unlock everything a High GR Level without the need of Boosting or killing x1000 Dyuraugaua for a few levels of GR or GSR
```
'''

        quest = '''
            ```
            The G Rank quests are divided by GR levels in each Rank to emulate the sense of progression and unlocking more content step by step. I asked a bunch of people in the community about their opinion and let them vote what feels better to them or sounds better i simply gone with the one with the most Votes even tho theres was always a tight gap between 2 options out of the 3. So some of you might not be happy with it others will.
            ```
            '''
        order = '''
```
How you do the quests is completly up to you the intended way is pretty much doing atleast every quests once means all 4 quests in GR1 for example to introduce you technically to all G rank fights and content avaible. But you obviously can choose to just do x4 Times Velocidrome or x2 Velocidrome and then x2 Iodromes etc... and will just have the same effect. So if you dont like a Monster quests take another from the current GR level Tier.
```

'''
        permit = '''
```
Permits are the way to try to Enforce the Artifical Urgents in G Rank. Each Rank and Origin, Exotic and Zenith have their own permit needed to take on the quests. The Permits are new Items and requirements to do G Rank quests, you will get a Bunch of Permits from the Artifical Urgent in each Rank as Sub A Reward. And then when you reach the Last GR Level Tier on the next Rank you will Unlock Permits to be Purchasable at the RoadShop in packs of x100 for 10 Points. Obviously this is easly abusable when you just take the time to grind the previous rank GRP to be in line with that level to Skip the Urgents technically no way to prevent that at the current time sorry your responsibility again..
```
'''
        zenith = '''
```
Well with all the Lists Organized Zenith is the only one i cant Maniuplate at the moment in terms of Order so the Zenith categorys for each Monster is the same but the GR Level Tiers are different obviously but i will give you a little List here how it is Organized so you can use this as Guideline.
```
'''
        notes = '''
```
The Event quests for GRP Gain were moved to the end of G rank progression since they are not needed for that and are more purely used for Endgame grind like GSR for different Weapons. Also the Netcafe Requirement for the 2 Netcafe Quests were removed. You unlock the 2 Lower Tier Quests with GR 800 and the Higher 2 with GR 999. Later down the line i want to edit those quests to make them more difficult and interesting for the fun of it.
```
'''
        await ctx.channel.send('> ** WHAT CHANGES**')
        await ctx.channel.send(different)
        await ctx.channel.send('> ** ABOUT G RANK**')
        await ctx.channel.send(quest)
        await ctx.channel.send('> ** WHAT QUEST SHOULD I TAKE?**')
        await ctx.channel.send(order)
        await ctx.channel.send(file=discord.File(f'{MISC_PATH}\\urgent.png'))
        await ctx.channel.send('> ** ABOUT ZENITH**')
        await ctx.channel.send(zenith)
        await ctx.channel.send(file=discord.File(f'{MISC_PATH}\\zenith.png'))
        await ctx.channel.send('> ** QUEST CHANGES**')
        await ctx.channel.send(notes)


def setup(bot):
    bot.add_cog(Guide_Help(bot))
