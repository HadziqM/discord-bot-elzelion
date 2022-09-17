import discord
from discord.ext import commands
from data import *
from pretty_help import PrettyHelp, DefaultMenu
import asyncio

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

if __name__ == '__main__':
    asyncio.run(main())

# app = Quart(__name__)

# @app.route("/")
# async def index():
#     return await render_template('index.html')

# bot.loop.create_task(app.run_task('127.0.0.1'))
