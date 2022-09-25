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
    extension = ['cogs.testing', 'cogs.test', "cogs.server", "cogs.bounty_cog"]
    for i in extension:
        await bot.load_extension(i)
    print('confirming token')
    await bot.start(db.token)


@bot.tree.context_menu(name="card", guild=discord.Object(937230168223789066))
async def mycard(interaction: discord.Interaction, member: discord.Member):
    await mcard(member, interaction)


@bot.tree.context_menu(name="event", guild=discord.Object(937230168223789066))
async def mycard(interaction: discord.Interaction, member: discord.Member):
    await mevent(member, interaction)


if __name__ == '__main__':
    discord.utils.setup_logging()
    asyncio.run(main())
