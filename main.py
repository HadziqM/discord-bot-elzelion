import discord
from discord.ext import commands
from data import *
from pretty_help import PrettyHelp, DefaultMenu
# from routes.utils import app
# from quart import Quart, redirect, url_for, render_template, request

db = database()


intents = discord.Intents.default()
intents.members = True

menu = DefaultMenu(page_left="◀️", page_right="▶️", remove="❌")
bot = commands.Bot(command_prefix=db.command,
                   intents=intents, help_command=PrettyHelp(color=discord.Colour.teal(), menu=menu))
# ,help_command=None
print('start')

extension = ['cogs.char', 'cogs.guide', 'cogs.gacha', 'cogs.game',
             'cogs.server', 'cogs.bounty', 'cogs.mod', 'cogs.test']
if __name__ == '__main__':
    for i in extension:
        bot.load_extension(i)

# app = Quart(__name__)


# @app.route("/")
# async def index():
#     return await render_template('index.html')

# bot.loop.create_task(app.run_task('127.0.0.1'))

print('confirming token')
bot.run(db.token)
