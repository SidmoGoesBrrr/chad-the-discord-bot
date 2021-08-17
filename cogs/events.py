import discord
from discord.ext import commands, tasks
from discord_components import *
from discord_components import DiscordComponents
import os
from tinydb import TinyDB, Query
def checkping(guild_id_var):
    db = TinyDB('databases/pings.json')
    query = Query()
    values = str(list(map(lambda entry: entry["pingstate"],
                          db.search(query.guild_id == str(guild_id_var))))[0])

    return values.lower()

class events(commands.Cog):
    """A couple of simple commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    @tasks.loop(seconds=20)  # repeat after every 20 seconds
    async def myLoop(self):
        dir = 'images'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        guilds = self.bot.guilds
        guild_count = 0
        member_count = 0
        for guild in guilds:
            guild_count += 1
            for member in guild.members:
                member_count += 1

        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"!help | {len(self.bot.users)} members in {guild_count} servers"))
        db = TinyDB('databases/pings.json')
        query = Query()

        for guild in self.bot.guilds:
            guild_id_var = guild.id
            try:
                db.update({'pingstate': True}, query.guild_id == str(guild_id_var))
            except:
                db.insert({'guild_id': str(guild_id_var), 'pingstate': True})

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('.....')
        self.myLoop.start()
        DiscordComponents(self.bot)
        guilds = self.bot.guilds
        guild_count = 0
        member_count = 0
        for guild in guilds:
            guild_count += 1
            for member in guild.members:
                member_count += 1

        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"!help | {len(self.bot.users)} members in {guild_count} servers"))


    


    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = member.guild.system_channel
        pos = sum(m.joined_at < member.joined_at for m in member.guild.members
                  if m.joined_at is not None)
        if member.guild.id == 869173101131337748 or member.guild.id == 819870399310594088:
            if checkping(member.guild.id) == 'true':
                membervar = member.mention

            else:
                membervar = member.display_name

            embed = discord.Embed(
                description=
                f"Welcome {membervar} to **{member.guild.name}**\nYou are the {pos}th member in the server.",
                color=0xe74c3c)
            embed.set_thumbnail(url=member.avatar_url)
            if not member.bot:
                try:
                    await member.send(f'Welcome to {member.guild.name}')
                except:
                    print("Could not DM")
                if not channel:
                    pass
                else:
                    await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_channel_create(self,channel):
        guild = channel.guild
        mutedRole = discord.utils.get(guild.roles, name="Is Muted")
        if mutedRole is None:
            perms = discord.Permissions(speak=False,
                                        send_messages=False,
                                        read_message_history=True,
                                        read_messages=True)
            try:
                await guild.create_role(name="Is Muted",
                                        color=discord.Color.dark_gray(),
                                        permissions=perms)

            except:
                print("New channel made, cant sync mute perms")
            try:
                mutedRole = discord.utils.get(guild.roles, name="Is Muted")
            except:
                print("Couldnt get role :(")
        try:
            await channel.set_permissions(mutedRole,
                                          send_messages=False,
                                          speak=False)
        except:
            print("Couldnt get role :(")


    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = member.guild.system_channel
        if member.guild.id == 869173101131337748 or member.guild.id == 819870399310594088:
            embed = discord.Embed(
                description=f"{member.name} left **{member.guild.name}**",
                color=0xe74c3c)
            embed.set_thumbnail(url=member.avatar_url)
            try:
                await channel.send(embed=embed)
            except:
                print("Could not get channel")


    


    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        db1 = TinyDB('databases/lockdown.json')
        db1.insert({'guild': guild.id, 'unaffected_channels': [], 'state': False})
        db2 = TinyDB('databases/pings.json')
        guild_id_var = guild.id
        db2.insert({'guild_id': str(guild_id_var), 'pingstate': True})

        count = 0
        for member in guild.members:
            count += 1
        embed = discord.Embed(title="Guild join",
                              description=guild.name,
                              color=0x00FF00)
        embed.add_field(name=f"Members", value=count)
        embed.add_field(name=f"Owner", value=guild.owner)
        a = self.bot.get_guild(869173101131337748)
        channel = a.get_channel(869447409237897256)
        embed.set_footer(text=f"Chad is currently in {len(self.bot.guilds)} servers")
        await channel.send(embed=embed)





    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        db1 = TinyDB('databases/lockdown.json')
        db1q = Query()
        db1.remove(db1q.guild == guild.id)
        db2 = TinyDB('databases/blacklist.json')
        db2q = Query()
        db2.remove(db2q.guild_id == guild.id)
        db3 = TinyDB('databases/warnings.json')
        db3q = Query()
        db3.remove(db3q.guild_id == guild.id)
        db4 = TinyDB('databases/prefix.json')
        db4q = Query()
        db4.remove(db4q.guild_id == guild.id)
        db5 = TinyDB('databases/pings.json')
        db5q = Query()
        db5.remove(db5q.guild_id == guild.id)
        embed = discord.Embed(title="Guild leave",
                              description=guild.name,
                              color=0xFF0000)
        count = 0
        for x in guild.members:
            count += 1

        embed.add_field(name=f"Members", value=count)
        embed.add_field(name=f"Owner", value=guild.owner)
        a = self.bot.get_guild(869173101131337748)
        channel = a.get_channel(869447409237897256)
        await channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(events(bot))
