import discord
import random
from discord.ext import commands
from discord.utils import get
from direc import *
from base import *
from discord import app_commands
main = database()
mod_id = int(main.mod)


class Mod_Only_Command(commands.Cog):
    """ only specified role can use this command """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(mod_id)
    async def upload(self, ctx, arg):
        try:
            int(arg)
        except:
            did = int(arg[2:-1])
            set_up()
            arg = check_disc(did)
        char = character(arg)
        char.upload_save()
        char.upload_part()
        await ctx.channel.send(f'uploaded ID:{arg} file to server')

    @app_commands.command(name="reset_boost_all", description="reset all player boost to active")
    @commands.has_role(mod_id)
    async def upload(self, interaction: discord.Interaction):
        await interaction.response.defer()
        mod = moderator()
        mod.log_ton_all()
        await interaction.followup.send("success")

    @commands.command()
    @commands.has_role(mod_id)
    async def add_gcp(self, ctx, arg, arg2):
        try:
            int(arg)
        except:
            did = int(arg[2:-1])
            set_up()
            arg = check_disc(did)
        char = character(arg)
        char.add_gcp(int(arg2))
        await ctx.channel.send(f'{char.name} added gcp by {arg2}')

    @commands.command()
    @commands.has_role(mod_id)
    async def add_bounty(self, ctx, arg, arg2):
        try:
            int(arg)
        except:
            did = int(arg[2:-1])
            set_up()
            arg = check_disc(did)
        char = character(arg)
        char.add_bounty(int(arg2))
        await ctx.channel.send(f'{char.name} added bounty by {arg2}')

    @commands.command()
    @commands.has_role(mod_id)
    async def set_bounty(self, ctx, arg, arg2):
        try:
            int(arg)
        except:
            did = int(arg[2:-1])
            set_up()
            arg = check_disc(did)
        char = character(arg)
        char.set_bounty(int(arg2))
        await ctx.channel.send(f'set {char.name} bounty by {arg2}')

    @commands.command()
    @commands.has_role(mod_id)
    async def add_ticket(self, ctx, arg, arg2):
        try:
            int(arg)
        except:
            did = int(arg[2:-1])
            set_up()
            arg = check_disc(did)
        gac = gacha(did)
        gac.add_gacha(int(arg2))
        char = character(arg)
        await ctx.channel.send(f'{char.name} added ticket by {arg2}')

    @commands.command()
    @commands.has_role(mod_id)
    async def set_gacha(self, ctx, arg, arg2):
        try:
            int(arg)
        except:
            did = int(arg[2:-1])
            set_up()
            arg = check_disc(did)
        char = character(arg)
        gac = gacha(did)
        gac.set_gacha(int(arg2))
        await ctx.channel.send(f'set {char.name} ticket by {arg2}')

    @commands.command()
    @commands.has_role(mod_id)
    async def add_gcp_all(self, ctx, arg):
        set_up()
        mod = moderator()
        mod.gcp_add(int(arg))
        await ctx.channel.send(f'sended {arg} gcp to all player')

    @commands.command()
    @commands.has_role(mod_id)
    async def transmog_all(self, ctx):
        set_up()
        mod = moderator()
        mod.mog_all()
        await ctx.channel.send('sended all transmog to all player')

    @commands.command()
    @commands.has_role(mod_id)
    async def unreg(self, ctx, arg):
        set_up()
        try:
            a = int(arg[2:-1])
        except:
            char = character(arg)
            a = char.discord
        try:
            arg = check_disc(a)
        except:
            await ctx.send("you are not registered")
            return
        char = character(arg)
        user = await ctx.guild.fetch_member(char.discord)
        role = get(ctx.message.guild.roles, id=1017643913667936318)
        await user.remove_roles(role)
        char.unreg()
        await ctx.channel.send('success')

    @commands.command()
    @commands.has_role(mod_id)
    async def add_registered_role_all(self, ctx):
        set_up()
        mod = moderator()
        a = mod.registered_disc_all()
        role = get(ctx.message.guild.roles, id=1017643913667936318)
        for i in a:
            try:
                user = await ctx.guild.fetch_member(int(i))
                await user.add_roles(role)
            except:
                await ctx.send(f"discord id {i} has left server")
        await ctx.send("success")

    @commands.command()
    @commands.has_role(mod_id)
    async def del_registered_role_all(self, ctx):
        set_up()
        mod = moderator()
        a = mod.registered_all()
        for i in a:
            try:
                role = get(ctx.message.guild.roles, name=f'ID:{i}')
                await role.delete()
            except:
                None
        await ctx.send("success")

    @commands.command()
    @commands.has_role(mod_id)
    async def f_reg(self, ctx, arg, arg2, arg1):
        arg2 = int(arg2)
        did = int(arg[2:-1])
        set_up()
        char = character(arg2)
        user = await ctx.guild.fetch_member(did)
        role = get(ctx.message.guild.roles, id=1017643913667936318)
        await user.add_roles(role)
        char.add_data(did, arg1)
        await ctx.channel.send(f'now {user} are registered to {char.name}')

    @commands.command()
    @commands.has_role(mod_id)
    async def distribution(self, ctx, *arg):
        set_up()
        bon = bounty(arg[0])
        if len(arg) == 2:
            did = int(arg[1][2:-1])
            cid = check_disc(did)
            char = character(cid)
            bon.bounty_rw(cid, 'S')
            await ctx.send(f'sended {bon.title} solo reward to {char.name} <@{did}>')
        elif arg[2] == 'npc':
            did = int(arg[1][2:-1])
            cid = check_disc(did)
            char = character(cid)
            bon.bounty_rw(cid, 'M')
            await ctx.send(f'sended {bon.title} multiplayer reward to {char.name} <@{did}>')
        elif len(arg) >= 3:
            for i in range(len(arg)-1):
                did = int(arg[i+1][2:-1])
                cid = check_disc(did)
                char = character(cid)
                bon.bounty_rw(cid, 'M')
                await ctx.send(f'sended {bon.title} multiplayer reward to {char.name} <@{did}>')

    @commands.command()
    @commands.has_role(mod_id)
    async def add_ticket_all(self, ctx, arg):
        set_up()
        mod = moderator()
        mod.add_ticket_all(int(arg))
        await ctx.send("success")

    @commands.command()
    @commands.has_role(mod_id)
    async def set_ticket_all(self, ctx, arg):
        set_up()
        mod = moderator()
        mod.set_ticket_all(int(arg))
        await ctx.send("success")

    @commands.command()
    @commands.has_role(mod_id)
    async def ravi_restart(self, ctx):
        set_up()
        mod = moderator()
        mod.rav_trunc()
        await ctx.channel.send('cleared ravi table')

    @commands.command()
    @commands.has_role(mod_id)
    async def random_move(self, ctx, arg, arg1, arg2):
        set_up()
        try:
            int(arg1)
            int(arg2)
        except:
            arg1 = guild_check(arg1)
            arg2 = guild_check(arg2)
        mod = moderator()
        a = mod.guild_mem_id(arg1)
        try:
            a.remove(mod.leader_id(arg1))
        except:
            await ctx.send("leader is invalid on guild")
            return
        random.shuffle(a)
        b = []
        for i in range(int(arg)):
            char = character(a[i])
            char.transfer_guild(arg2)
            b.append(char.name)
        await ctx.send(f" {b} in Guild ID {arg1} randomly selected to be transferred to Guild ID {arg2}")

    @commands.command()
    @commands.has_role(mod_id)
    async def bounty_end(self, ctx):
        set_up()
        mod = moderator()
        mod.del_dist()
        await ctx.channel.send('deleted all bounty reward')

    @commands.command()
    @commands.has_role(mod_id)
    async def purge(self, ctx, arg):
        a = int(arg)
        async for message in ctx.channel.history(limit=a):
            await message.delete()

    @commands.command()
    @commands.has_role(mod_id)
    async def send_newb(self, ctx, arg, arg1):
        set_up()
        try:
            a = int(arg[2:-1])
            try:
                arg = check_disc(a)
                char = character(arg)
            except:
                await ctx.send("you are not registered")
                return
        except:
            char = character(arg)
            if char.discord == None:
                await ctx.send("you are not registered")
                return
        try:
            char.newbie_rw(arg1)
            await ctx.send(f"sended newbie reward to {char.name}")
        except:
            await ctx.send(f"cant send reward, check your spelling")


async def setup(bot):
    await bot.add_cog(Mod_Only_Command(bot))
