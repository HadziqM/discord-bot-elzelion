import discord
from discord.ext import commands
from discord import app_commands
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
    extension = ['cogs.char', 'cogs.guide', 'cogs.gacha', 'cogs.game',
                 'cogs.server', 'cogs.bounty', 'cogs.mod', 'cogs.test']
    for i in extension:
        await bot.load_extension(i)
    print('confirming token')
    await bot.start(db.token)


@bot.tree.context_menu(name="mycard", guild=discord.Object(937230168223789066))
async def mycard(interaction: discord.Interaction, member: discord.Member):
    await mcard(member, interaction)


if __name__ == '__main__':
    asyncio.run(main())
    discord.utils.setup_logging()
