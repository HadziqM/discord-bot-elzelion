import discord
from discord.ext import commands
from data import *
from pretty_help import PrettyHelp, DefaultMenu
import asyncio
from base import *
from cogs.ctxmenu import *

db = database()
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.messages = True
menu = DefaultMenu(page_left="◀️", page_right="▶️", remove="❌")
bot = commands.Bot(command_prefix=db.command,
                   intents=intents, help_command=PrettyHelp(color=discord.Colour.teal(), menu=menu))
print('start')


async def main():
    extension = ['cogs.general', 'cogs.server', 'cogs.char', 'cogs.gacha',
                 'cogs.mod', 'cogs.bounty_cog', 'cogs.game', 'cogs.guide']
    for i in extension:
        await bot.load_extension(i)
    print('confirming token')
    await bot.start(db.token)


@bot.tree.context_menu(name="card", guild=discord.Object(937230168223789066))
async def mycard(interaction: discord.Interaction, member: discord.Member):
    await mcard(member, interaction)


@bot.tree.context_menu(name="event", guild=discord.Object(937230168223789066))
async def mycard1(interaction: discord.Interaction, member: discord.Member):
    await mevent(member, interaction)


@bot.tree.context_menu(name="bounty_submit", guild=discord.Object(937230168223789066))
async def mycard2(interaction: discord.Interaction, msg: discord.Message):
    await msubmit(msg, interaction, bot)


@bot.tree.context_menu(name="bounty_submit_multi", guild=discord.Object(937230168223789066))
async def mycard3(interaction: discord.Interaction, msg: discord.Message):
    await msubmit_multi(msg, interaction, bot)


@bot.tree.context_menu(name="Transmog Contest", guild=discord.Object(937230168223789066))
async def mycard4(interaction: discord.Interaction, msg: discord.Message):
    await transcontest(msg, interaction, bot)


if __name__ == '__main__':
    discord.utils.setup_logging()
    asyncio.run(main())
