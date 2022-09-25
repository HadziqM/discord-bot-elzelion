import discord
from discord.ext import commands
from direc import *
from PIL import Image
import io


class Testing(commands.Cog):
    """ list of all guides, you can request by DM me (yes me elzelion) """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_pfp(self, ctx):
        byte = await ctx.author.display_avatar.read()
        im = Image.open(io.BytesIO(byte)).resize((200, 200))
        im2 = Image.open(f"{MISC_PATH}\\welcum.jpg")
        im2.paste(im, (100, 150))
        im2.save("hello.jpg")
        await ctx.send(file=discord.File("hello.jpg"))


async def setup(bot):
    await bot.add_cog(Testing(bot))
