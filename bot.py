import asyncio
import time
import discord
import urbandict
from discord.utils import get
import discord
from discord.ext import commands, tasks
import random
import wikipedia
import os
import requests
import re
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math
import pyfiglet
from io import BytesIO
from tinydb import TinyDB, Query
from PyDictionary import PyDictionary
from modules import encrypt as enc, decrypt as dec, languages
from keep_alive import keep_alive
from discord.ext.commands import MissingPermissions
from googletrans import Translator, constants
from pprint import pprint
import typing
from discord.ext.commands import cooldown, BucketType
intents = discord.Intents().all()
from discord_components import *
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
import aiohttp
import giphy_client
from giphy_client.rest import ApiException
async def determine_prefix(bot, message):
    if message.guild:
        db = TinyDB('databases/prefix.json')
        if message is not None:
            guild_id = message.guild.id
        query = Query()
        if db.search(query['guild_id'] == str(guild_id)):
            values = list(map(lambda entry: entry["prefix"], db.search(query.guild_id == str(guild_id))))
            return values
        return '!'

    else:
        return '!'


bot = commands.Bot(command_prefix=determine_prefix, intents=intents)

emojiLetters = [
    "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"]


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening,
                                                                                    name="!help"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    myLoop.start()
    DiscordComponents(bot)


@bot.event
async def on_message(message):
    db = TinyDB('databases/blacklist.json')
    member = message.author.id
    try:
        query = Query()
        blacklisted_guild = db.search(query['guild_id'] == message.guild.id)
        blacklisted_peeps = None
        for i in range(0, len(blacklisted_guild)):
            if str(member) in str(blacklisted_guild[i]):
                blacklisted_peeps = blacklisted_guild[i]
        if blacklisted_peeps is not None:
            return
    except:
        print("It's a DM")

    await bot.process_commands(message=message)


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    db = TinyDB("databases/people_who_know.json")
    pos = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)
    embed = discord.Embed(
        description=f"Welcome {member.name} to **{member.guild.name}**\nYou are the {pos}th member in the server.",
        color=0xe74c3c)
    embed.set_thumbnail(url=member.avatar_url)
    if not member.bot:
        try:
          await member.send(f'Welcome to {member.guild.name}')
        except:
          pass
        if str(member.id) not in str(db):
            db.insert({'name': member.id})
        if not channel:
            pass
        else:
            await channel.send(embed=embed)


@bot.event
async def on_guild_channel_create(channel):
    guild = channel.guild
    mutedRole = discord.utils.get(guild.roles, name="Is Muted")
    if mutedRole is None:
        perms = discord.Permissions(speak=False, send_messages=False, read_message_history=True, read_messages=True)
        await guild.create_role(name="Is Muted", color=discord.Color.dark_gray(), permissions=perms)
        mutedRole = discord.utils.get(guild.roles, name="Is Muted")

    await channel.set_permissions(mutedRole, send_messages=False, speak=False)


@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    pos = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)
    embed = discord.Embed(
        description=f"{member.name} left **{member.guild.name}**",
        color=0xe74c3c)
    embed.set_thumbnail(url=member.avatar_url)
    try:
        await channel.send(embed=embed)
    except:
        print("Could not get channel")


@tasks.loop(seconds=20)  # repeat after every 20 seconds
async def myLoop():
    dir = 'images'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


@bot.event
async def on_guild_join(guild):
    db = TinyDB('databases/people_who_know.json')
    db1 = TinyDB('databases/lockdown.json')
    db1.insert({'guild': guild.id, 'unaffected_channels': [], 'state': False})
    count=0
    for x in guild.members:
        if not x.bot and str(x.id) not in str(db.all()):
            db.insert({'name': x.id})
        count += 1
    embed = discord.Embed(title="Guild join", description=guild.name, color=0x00FF00)
    placehold = 'We do be popular boi'
    embed.add_field(name=f"Members", value=count)
    embed.add_field(name=f"Owner", value=guild.owner)
    a = bot.get_guild(869173101131337748)
    channel = a.get_channel(869447409237897256)
    embed.set_footer(text=f"Chad is currently in {len(bot.guilds)} servers")
    await channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    db = TinyDB("databases/people_who_know.json")
    pos = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)
    embed = discord.Embed(
        description=f"Welcome {member.mention} to **{member.guild.name}**\nYou are the {pos}th member in the server.",
        color=0xe74c3c)
    embed.set_thumbnail(url=member.avatar_url)
    if not member.bot:
        await member.send(f'Welcome to {member.guild.name}')
        if str(member.id) not in str(db):
            db.insert({'name': member.id})
        if not channel:
            pass
        else:
            await channel.send(embed=embed)


@bot.event
async def on_guild_remove(guild):
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

    embed = discord.Embed(title="Guild leave", description=guild.name, color=0xFF0000)
    count = 0
    for x in guild.members:
        count += 1
  
    embed.add_field(name=f"Members", value=count)
    embed.add_field(name=f"Owner", value=guild.owner)
    a = bot.get_guild(869173101131337748)
    channel = a.get_channel(869447409237897256)
    await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    await asyncio.sleep(180)
    try:
        del snipe_message_author[message.channel.id]
        del snipe_message_content[message.channel.id]
    except:

        print("Could not delete")


time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)([smhd])")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        matches = time_regex.findall(argument.lower())
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k] * float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


@bot.command()
async def prefix(ctx, *, prefix=None):
    if ctx.author.guild_permissions.administrator:
        db = TinyDB('databases/prefix.json')
        query = Query()
        guild_id_var = ctx.guild.id
        if prefix is None:
            await ctx.send(embed=discord.Embed(title=f"My prefix is `{ctx.prefix}`"))

        else:
            if db.search(query.guild_id == str(guild_id_var)):
                db.update({'prefix': prefix}, query.guild_id == str(guild_id_var))
                await ctx.send(embed=discord.Embed(title=f"Updated prefix of \"{ctx.guild.name}\" to {prefix}"))
            else:
                db.insert({'guild_id': str(guild_id_var), 'prefix': str(prefix)})
                await ctx.send(embed=discord.Embed(title=f"Changed prefix of \"{ctx.guild.name}\" to {prefix}"))

    else:
        embed = discord.Embed(title="Hold up",
                              description="You can't do that, your not an admin!",
                              color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="PING",
                          description=f"Ping is {round(bot.latency * 1000)}ms",
                          color=discord.Color.green())
    await ctx.send(embed=embed)


@bot.command()
async def invite(ctx):
    embed = discord.Embed(
        title="Invite",
        description=f"To invite me to your own server [click here](https://discord.com/api/oauth2/authorize?client_id=864010316424806451&permissions=4227997759&scope=applications.commands%20bot)")
    
    embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.color = discord.Colour.green()
    await ctx.send(embed=embed)


@bot.command()
async def robmoji(ctx, emoji: discord.PartialEmoji, *, Name=None):
  if ctx.author.guild_permissions.manage_emojis:
    emoji_url=emoji.url
    if Name is None:
      Name=emoji.name

    async with aiohttp.ClientSession() as session:
        async with session.get(str(emoji_url)) as response:
            img = await response.read()
    new_emoji=await ctx.guild.create_custom_emoji(name=Name, image=img)
    embed=discord.Embed(title="Emoji Added Pog!",description=f"Name is:\"{Name}\", your emoji is {new_emoji}",color=discord.Color.random())
    await ctx.send(embed=embed)
  else:
    await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require to have manage emojis permission!",
                                color=discord.Color.red()))


@bot.command()
async def userinfo(ctx, target: discord.Member):
    if ctx.author.guild_permissions.administrator:
        x = ctx.guild.members
        if target in x:
            roles = [role for role in target.roles if role != ctx.guild.default_role]
            if roles == []:
                roles = None
            embed = discord.Embed(title="User information", colour=discord.Color.gold(),
                                  timestamp=datetime.datetime.utcnow())

            embed.set_author(name=target.name, icon_url=target.avatar_url)

            embed.set_thumbnail(url=target.avatar_url)

            embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                             icon_url=ctx.author.avatar_url)

            if roles is None:
                fields = [("Name", str(target), False),
                          ("ID", target.id, False),
                          ("Status", str(target.status).title(), False),
                          (f"Roles", "No roles", False),
                          ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
                          ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), False)]

            else:
                fields = [("Name", str(target), False),
                          ("ID", target.id, False),
                          ("Status", str(target.status).title(), False),
                          (f"Roles ({len(roles)})", " ".join([role.mention for role in roles]), False),
                          ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
                          ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'You have to ping someone from this server')
    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require to be an admin!",
                                color=discord.Color.red()))


format = "%a, %d %b %Y | %H:%M:%S %ZGMT"


@bot.command()
async def about(ctx):
    about_embed = discord.Embed(title="About ME!", color=discord.Color.green())
    about_embed.add_field(name="Bot Developed by:", value=f"ZeroAndOne, [My epic devs!](https://zeroandone.ml)")
    about_embed.add_field(name="Created to:", value=f"Make discord a better place. :angel:")
    about_embed.add_field(name="Features:", value=f"Use !help", inline=True)
    about_embed.add_field(name="Give me feedback and complains here. Help me improve myself!\nAlso useful for finding out about the latest Chad updates!!",
                          value=f"[Support Server](https://discord.gg/5ABvVwKGCF)", inline=True)
    user = bot.get_user(864010316424806451)
    about_embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=about_embed)


@bot.command()
async def website(ctx):
    embed = discord.Embed(title="Link for our website",
                          color=discord.Color.dark_magenta(),
                          description="This is our main [website](https://zeroandone.ml)\nClick [here](https://www.youtube.com/channel/UCF0DZYNiHcIGZKBoPWfc0lg) to see our YouTube Channel.")
    embed.set_footer(text=f"Website requested by {ctx.author.name}")
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
async def support(ctx):
    embed = discord.Embed(title="Support Server",
                          description="To visit our support server, click [here](https://discord.gg/EmvXgYyV).\nNow you can complain all you want!!",
                          color=discord.Color.random())
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
@commands.guild_only()
async def serverinfo(ctx):
    format = "%a, %d %b %Y | %H:%M:%S %ZGMT"
    embed = discord.Embed(
        color=ctx.guild.owner.top_role.color
    )
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels
    embed.set_thumbnail(url=str(ctx.guild.icon_url))
    embed.add_field(name=f"Information About **{ctx.guild.name}**: ",
                    value=f":white_small_square: ID: **{ctx.guild.id}** \n:white_small_square: Owner: **{ctx.guild.owner}** \n:white_small_square: Location: **{str(ctx.guild.region).capitalize()}** \n:white_small_square: Creation: **{ctx.guild.created_at.strftime(format)}** \n:white_small_square: Members: **{ctx.guild.member_count}** \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(ctx.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \n:white_small_square: Splash: {ctx.guild.splash}")
    await ctx.send(embed=embed)


@bot.command()
async def servers(ctx):
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        active_servers = bot.guilds
        i = 0
        embed = discord.Embed(title="Servers i am in......", color=discord.Color.random())
        for guild in active_servers:
            i += 1
            embed.add_field(name=f"{i}.", value=guild, inline=False)

        embed.set_footer(text="Someone be getting popular :)")
        await ctx.send(embed=embed)

    else:
        await ctx.send(embed=discord.Embed(title="Imagine trying to see stats of someone else's bot",
                                           color=discord.Color.random()))


@bot.command()
async def makerole(ctx, *, rolename):
    color = discord.Color.random()
    if ctx.author.guild_permissions.manage_roles:
        guild = ctx.guild
        perms = discord.Permissions(send_messages=True, read_messages=True)
        role = await guild.create_role(name=rolename, color=color, permissions=perms)
        embed1 = discord.Embed(title="Role Created!",
                               description=f"Added role {role.mention} to the server!",
                               color=color)
        embed1.set_footer(text=f"Tip: Do {ctx.prefix}addrole to add your newly created role to users!")
        await ctx.send(embed=embed1)

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!",
                                description="You require the Manage Roles permission.",
                                color=color))


@bot.command()
async def addrole(ctx, member: discord.Member, *, role: discord.Role = None):
    if ctx.author.guild_permissions.manage_roles:
        embed = discord.Embed(
            title=f"Role Added",
            description=f"{role} has been added to {member.name}."
        )
        embed.color = discord.Color.random()
        embed.set_footer(text="Gamers = Poggers but why is this here???")
        await member.add_roles(role)
        await ctx.send(embed=embed)

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the Manage Roles permission.",
                                color=discord.Color.green()))


@bot.command()
async def editrole(ctx, from_role: discord.Role, *, to_role):
    if ctx.author.guild_permissions.manage_roles:
        guild = ctx.guild
        from_role = str(from_role)
        role = discord.utils.get(guild.roles, name=from_role)
        embed = discord.Embed(
            title="Role has been edited.",
            description=f"Role name changed from {role} to {to_role}.",
            color=discord.Color.random()
        )
        await role.edit(name=to_role)
        await ctx.send(embed=embed)



    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!",
                                description="You require the Manage Roles permission.",
                                color=discord.Color.green()))


@bot.command()
async def removerole(ctx, member: discord.Member, *, role: discord.Role = None):
    if ctx.author.guild_permissions.manage_roles:
        print(member.mention)
        embed = discord.Embed(
            title=f"Role Removed",
            description=f"{role} has been removed from {member.name}."
        )
        embed.color = 0x0000ff
        embed.set_footer(text=f"")
        await member.remove_roles(role)
        await ctx.send(embed=embed)

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the Manage Roles permission.",
                                color=discord.Color.green()))


@bot.command()
async def deleterole(ctx, rolename: discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        await rolename.delete()
        embed = discord.Embed(
            title=f"Role {rolename} has been deleted",
            description=f"GET EM OUTTA HERE", color=discord.Color.random()
        )
        await ctx.send(embed=embed)

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!",
                                description="You require the Manage Roles permission.",
                                color=discord.Color.green()))


@bot.command()
async def nick(ctx, member: discord.Member, *, nick=None):
    if ctx.author.guild_permissions.manage_nicknames:
        if nick is None:
            await member.edit(nick=member.name)
            embed = discord.Embed(title=f"Nickname removed from {member.name}",
                                  description=f"His name has been changed back to {member.name}",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

        elif len(nick) > 32:
            embed = discord.Embed(title=f"That nickname is TOO LONG",
                                  description=f" I'd probably get bored changing it\nTry a nickname that has less then 32 characters",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)

        else:
            await member.edit(nick=nick)
            embed = discord.Embed(title=f"Nickname changed for {member.name}",
                                  description=f" His name is now {member.nick}",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)

    else:
        await ctx.send(
            embed=discord.Embed(title="I refuse", description="You require the manage nicknames permission.",
                                color=discord.Color.red()))


@bot.command()
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(title=f"Last deleted message in #{channel.name}",
                           description=snipe_message_content[channel.id], color=discord.Color.red())

        em.set_footer(text=f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed=em)

    except:
        em = discord.Embed(description=f"There are no recently deleted messages in channel {channel.name}",
                           color=discord.Color.dark_gray())
        await ctx.send(embed=em)


@bot.command()
async def slowmode(ctx, seconds: int):
    if ctx.author.guild_permissions.administrator:
        
        if seconds <= 21600:
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(
                title="Slowmode Enabled!",
                description=f"There is a {seconds} seconds slowmode on this channel now."
            )
        else:
            embed = discord.Embed(title="Did you know?",
                                  description=f"Discord allows slowmodes upto 21600 seconds on its channels, which is equal to 360m, which is 6h!",
                                  color=discord.Color.random())
            embed.set_footer(text="Point being, you can't set a slowmode above that")
        await ctx.send(embed=embed)

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the Administrators permission.",
                                color=discord.Color.green()))
    

@bot.command()
async def blacklist(ctx, member: discord.Member):
    db = TinyDB('databases/blacklist.json')
    guild_id_var = ctx.guild.id
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        db.insert({'guild_id': guild_id_var, 'blacklisted': str(member.id)})
        await ctx.send(embed=discord.Embed(title=f"I'm Sorry, but my boss wants you blacklisted"))
        return

    elif ctx.author.guild_permissions.administrator:
        if not member:
            await ctx.send(embed=discord.Embed(title="Please provide a member to blacklist smh"))
            return

        if member == ctx.author:
            embed = discord.Embed(title="Bruh why are you trying to blacklist yourself.",
                                  description="I refuse to let your stupidity get the better of you.",
                                  color=discord.Color.random())
            embed.set_footer(text="Users these days...")
            await ctx.send(embed=embed)
            return

        elif member.id == 815555652780294175 or member.id == 723032217504186389:
            await ctx.send(
                embed=discord.Embed(title="Buddy you can't blacklist the boss <a:ZO_BlobCool:866263738545078302>"))
            return

        elif member.guild_permissions.administrator:
            await ctx.send(
                embed=discord.Embed(title="Halt! (lmao)",
                                    description="You cannot just go ahead and stop your fellow admins from using me!",
                                    color=discord.Color.red()))
            return

        elif {"guild_id": guild_id_var, "blacklisted": str(member.id)} in db.all():
            await ctx.send(embed=discord.Embed(title=f"{member.display_name} is already blacklisted...",
                                               description="Jeez why do you hate him so much",
                                               color=discord.Color.teal()))
            return

        else:
            db.insert({'guild_id': guild_id_var, 'blacklisted': str(member.id)})
            await ctx.send(embed=discord.Embed(title=f"{member.display_name} is blacklisted",
                                               description="He can no longer use me :cry:",
                                               color=discord.Color.teal()))
            return

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the administrator permission.",
                                color=discord.Color.red()))


@bot.command()
async def unblacklist(ctx, member: discord.Member):
    db = TinyDB('databases/blacklist.json')
    guild_id_var = ctx.guild.id
    if ctx.author.guild_permissions.administrator or ctx.author.id == 815555652780294175 or \
            ctx.author.id == 723032217504186389:
        if not member:
            await ctx.send("Please provide a member to unblacklist")
            return
        query = Query()
        try:
            db.remove(query.blacklisted == str(member.id))
            if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
                await ctx.send(embed=discord.Embed(title=f"{member.display_name} is unblacklisted",
                                                   description="My boss asked me to do so... :joy:",
                                                   color=discord.Color.random()))

            else:
                await ctx.send(embed=discord.Embed(title=f"{member.display_name} is unblacklisted",
                                                   description="He can now use me! :joy:",
                                                   color=discord.Color.random()))
        except:
            await ctx.send(embed=discord.Embed(title="Nope!",
                                               description=f"{member.display_name} is not blacklisted in this server."))
    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the administrator permission.",
                                color=discord.Color.red()))


@bot.command()
async def clear(ctx, times: int, hide=None):
    if ctx.author.guild_permissions.manage_messages:
        if hide is None:
            await ctx.channel.purge(limit=times + 1)
            await ctx.send(embed=discord.Embed(title=f"{times} messages deleted"))
        elif hide == 'hide':
            await ctx.channel.purge(limit=times + 1)
            print('Pog')
        else:
            await ctx.send(embed=discord.Embed(title=f"Oops! Wrong Command... :sweat_smile:"))

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the Manage Messages permission.",
                                color=discord.Color.green()))


@bot.command()
async def warn(ctx, member: discord.Member, *, reason: str):
    db = TinyDB('databases/warnings.json')
    guild_id_var = ctx.guild.id
    if ctx.author != member:
        if ctx.author.guild_permissions.administrator:
            if member.guild_permissions.administrator:
                await ctx.send(embed=discord.Embed(title="ALERT! ALERT! :dizzy_face:",
                                                   description="Warning fellow admins is a no-no, kids!",
                                                   color=discord.Color.random()))
                return
            elif not reason:
                await ctx.send(embed=dsicrod.Embed(title="Please provide a reason",
                                                   color=discord.Color.random()))
                return

            elif len(reason) > 150:
                await ctx.send(
                    embed=discord.Embed(title=f"The reason for warning cannot be more then 150 characters long!",
                                        description=f"You are {len(reason) - 150} characters over the limit!",
                                        color=discord.Color.random()))
                return
            else:
                await ctx.send(embed=discord.Embed(title=f"{member.display_name} has been warned", description=reason,
                                                   color=discord.Color.random()))
                db.insert({'guild_id': guild_id_var, 'member': str(member), 'reason': reason})


        else:
            await ctx.send(
                embed=discord.Embed(title="Stop right there!", description="You require the administrator permission.",
                                    color=discord.Color.red()))
    else:
        await ctx.send(embed=discord.Embed(title="Stop trying to warn yourself.",
                                           description="IT. IS. A. BAD. THING.",
                                           color=discord.Color.random()))


@bot.command()
async def userwarn(ctx, member: discord.Member):
    db = TinyDB('databases/warnings.json')
    guild_id_var = ctx.guild.id
    query = Query()
    tht_member_warnings = db.search(query['member'] == str(member))
    a = db.search((query['guild_id'] == guild_id_var) & (query['member'] == str(member)))
    embed = discord.Embed(title=f"Here are the warnings for {member.mention}:", description="Warnings")
    if len(a) == 0:
        embed = discord.Embed(title="This user has a MIND BLOWING number of warnings!!",
                              description="0, to be exact",
                              color=discord.Color.green())
        embed.set_footer(text="Clean record for now, eh?")
    else:
        i = 0
        for a in a:
            i += 1
            b = a.get('reason')
            embed.add_field(name=f"{i}. ", value=b, inline=False)
        embed.set_footer(text="Someone's been a naughty boi. Unless you're a girl.")
        embed.color = 0xa6ff00

    await ctx.send(embed=embed)


@bot.command()
async def lockdown(ctx, state):
    db = TinyDB('databases/lockdown.json')
    query = Query()
    if ctx.author.guild_permissions.administrator:
        guild = ctx.guild
        everyone = discord.utils.get(guild.roles)
        unaffected_channels = []
        if state.lower() == 'true':
            if db.search(query.guild == ctx.guild.id)[0]['state'] is False:
                embed = discord.Embed(
                    title="Turned on lockdown. No one gets in or out <a:ZOWumpusTongue:865559251764903946>")
                embed.set_footer(text="Corona is ONLINE")
                embed.color = discord.Color.red()
                await ctx.send(embed=embed)
                for channel in guild.text_channels:
                    perms = channel.overwrites_for(ctx.guild.default_role)
                    if perms.send_messages is False or perms.view_channel is False:
                        unaffected_channels.append(channel.id)
                    else:
                        await channel.set_permissions(everyone, send_messages=False)

                for channel in guild.voice_channels:
                    perms = channel.overwrites_for(ctx.guild.default_role)
                    if perms.speak is False or perms.view_channel is False:
                        unaffected_channels.append(channel.id)
                    else:
                        await channel.set_permissions(everyone, speak=False)
                db.update({'unaffected_channels': unaffected_channels}, query.guild == ctx.guild.id)
                db.update({'state': True}, query.guild == ctx.guild.id)
            else:
                await ctx.send(embed = discord.Embed(title="This channel is ALREADY under lockdown",
                                                     description="You can be arrested by law if you place a lockdown TWICE.",
                                                     color=discord.Color.random()))

        elif state.lower() == 'false':
            if db.search(query.guild == ctx.guild.id)[0]['state'] is True:
                unaffected_channels = db.search(query.guild == ctx.guild.id)[0]['unaffected_channels']
                for channel in guild.text_channels:
                    if channel.id in unaffected_channels:
                        print(channel)
                    else:
                        await channel.set_permissions(everyone, send_messages=None)
                for channel in guild.voice_channels:
                    if channel.id in unaffected_channels:
                        print(channel)
                    else:
                        await channel.set_permissions(everyone, speak=None)
                db.update({'state': False}, query.guild == ctx.guild.id)
                embed = discord.Embed(title="Lockdown has been lifted.... Enjoy Suckas <a:ZOPepeRave:865560322966421514>")
                embed.set_footer(text="Corona go poof ")
                embed.color = discord.Color.green()
                await ctx.send(embed=embed)

            else:
                await ctx.send(embed = discord.Embed(title="This channel is ALREADY free",
                                                     description="Don't give too much freedom. It will lead to chaos.",
                                                     color=discord.Color.random()))

        else:
            embed = discord.Embed(title=f"Please give a valid state, True or false", description="Try `{ctx.prefix}lockdown true` or `{ctx.prefix}lockdown false`",
                                  color=discord.Color.random())
            await ctx.send(embed=embed)
    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the Manage roles permission. :expressionless:\nJk lol U need admin perms.",
                                color=discord.Color.red()))

@bot.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Is Muted")
        await member.remove_roles(mutedRole)
        guild = ctx.guild
        if mutedRole in member.roles:
            embed = discord.Embed(title=f"{member.display_name} has now been unmuted!!", color=discord.Color.blurple())
            embed.set_footer(text="Rejoice son, don't make this mistake again")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="This user isn't even muted.", description="Forgiveness maybe a good thing.\nBut you're still WASTING MY TIME.", color=discord.Color.random())
            embed.set_footer(text="If only the world had a bit of common sense...")
            await ctx.send(embed=embed)
            return
      
    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require to be an admin!",
                                color=discord.Color.red()))


@bot.command()
async def tempmute(ctx, duration: TimeConverter, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Is Muted")
    if duration != 0:
        if member == ctx.author:
            embed = discord.Embed(title="Why would you even DO that?",
                                  description=f"Did you really just try to mute yourself? :person_facepalming:",
                                  color=discord.Color.random())
            embed.set_footer(text="Sometimes I just wonder...")
            await ctx.send(embed=embed)
            return

        if mutedRole in member.roles:
          embed=discord.Embed(title="Already muted idiot", description="How many times do you wish to mute this dude?", color=discord.Color.random())
          embed.set_footer(text="I feel sorry for my bro")
          await ctx.send(embed=embed)
          return


        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Nuh uh not happening",
                                  description="You can't just mute your fellow admins.",
                                  color=discord.Color.random())
            await ctx.send(embed=embed)
            return

        if reason is None:
            reason = "no reason specified"

        if mutedRole is None:
            perms = discord.Permissions(speak=False, send_messages=False, read_message_history=True,
                                        read_messages=True)
            await guild.create_role(name="Is Muted", color=discord.Color.dark_gray(), permissions=perms)
            mutedRole = discord.utils.get(guild.roles, name=" Is Muted")

        message = f"You have been muted in {ctx.guild.name} for {reason}"
        try:
          await member.send(message)

        except:
          print("Could not DM him")
        await member.add_roles(mutedRole, reason=reason)
        embed = discord.Embed(title=f"{member.display_name} has now been muted for {duration}s.!!",
                              color=discord.Color.blurple())
        embed.set_footer(text="Waiting for that to end...")
        await ctx.send(embed=embed)

        await asyncio.sleep(duration)
        message2 = f"You have been unmuted in {ctx.guild.name}."
        await member.remove_roles(mutedRole)
        try:
          await member.send(message2)

        except:
          print("Could not DM him")

        embed = discord.Embed(title=f"{member.display_name} has now been unmuted!!", color=discord.Color.blurple())
        embed.set_footer(text="Rejoice son, don't make this mistake again")
        await ctx.send(embed=embed)




    else:
        await ctx.send(
            embed=discord.Embed(title="Cannot tempmute user", description="Invalid time given",
                                color=discord.Color.random()))


@bot.command()
async def mute(ctx, member: discord.Member, *, reason="No reason given"):
    if ctx.author.guild_permissions.administrator:
        if member == ctx.author:
            embed = discord.Embed(title="Why would you even DO that?",
                                  description=f"Did you really just try to mute yourself? :person_facepalming:",
                                  color=discord.Color.random())
            embed.set_footer(text="Sometimes I just wonder...")
            await ctx.send(embed=embed)
            return

        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Nuh uh not happening",
                                  description="You can't just mute your fellow admins.",
                                  color=discord.Color.random())
            await ctx.send(embed=embed)
            return

        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Is Muted")
        if mutedRole in member.roles:
          embed=discord.Embed(title="Already muted idiot", description="How many times do you wish to mute this dude?", color=discord.Color.random())
          embed.set_footer(text="I feel sorry for my bro")
          await ctx.send(embed=embed)
          return


        if mutedRole is None:
            perms = discord.Permissions(speak=False, send_messages=False, read_message_history=True, read_messages=True)
            await guild.create_role(name="Is Muted", color=discord.Color.dark_gray(), permissions=perms)
            mutedRole = discord.utils.get(guild.roles, name=" Is Muted")

        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted.",
                              colour=discord.Colour.random())
        embed.add_field(name="reason:", value=reason, inline=True)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, send_messages=False,
                                          speak=False)
        try:
          await member.send(f" You have been muted in: {guild.name} reason: {reason}")
        except:
          print("Oops Could not dm user")
    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require to be an admin!",
                                color=discord.Color.red()))


@bot.command()
async def kick(ctx, member: discord.Member):
    if ctx.author.guild_permissions.kick_members:
        if member == ctx.author:
            embed = discord.Embed(title="Why would you even DO that?",
                                  description=f"Did you really just try to kick yourself? :person_facepalming:",
                                  color=discord.Color.random())
            embed.set_footer(text="Sometimes I just wonder...")
            await ctx.send(embed=embed)
            return

        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Nuh uh not happening",
                                  description="You can't just kick your fellow admins.",
                                  color=discord.Color.random())

            await ctx.send(embed=embed)
            return
        message = f"You have been kicked from {ctx.guild.name}"
        try:
          await member.send(message)

        except:
          print("Could not DM him")
        await ctx.guild.kick(member)
        await ctx.channel.send(embed=discord.Embed(title=f"{member} is kicked!"), color=discord.Color.random())

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the Kick Member permission.",
                                color=discord.Color.green()))


@bot.command()
async def unban(ctx, member: discord.User = None):
    if ctx.author.guild_permissions.ban_members:
        if member is None or member == ctx.message.author:
            await ctx.channel.send("You cannot unban yourself")
            return
        await ctx.guild.unban(member)
        await ctx.channel.send(embed=discord.Embed(title=f"{member} is unbanned!", color=discord.Color.random()))

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the Ban Member permission.",
                                color=discord.Color.green()))


@bot.command()
async def tempban(ctx, duration: TimeConverter, member: discord.Member, *, reason=None):
    if duration != 0:
        if member == ctx.author:
            embed = discord.Embed(title="Why would you even DO that?",
                                  description=f"Did you really just try to ban yourself? :person_facepalming:\nEven temporarily, that's just stupid.",
                                  color=discord.Color.random())
            embed.set_footer(text="Sometimes I just wonder...")
            await ctx.send(embed=embed)
            return

        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Nuh uh not happening",
                                  description="You can't just ban your fellow admins temporarily!",
                                  color=discord.Color.random())
            await ctx.send(embed=embed)
            return

        if ctx.author.guild_permissions.ban_members:
            banned_gifs = ["https://media.tenor.com/images/d41f93e7538f0afb56ad1450fed9c02e/tenor.gif",
                           "https://media.tenor.com/images/048b3da98bfc09b882d3801cb8eb0c1f/tenor.gif",
                           "https://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif",
                           "https://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif",
                           "https://media.tenor.com/images/1a84c478d1073757cf8929a89e47bbfc/tenor.gif"]

            if member is None or member == ctx.message.author:
                await ctx.channel.send("You cannot ban yourself")
                return

            if reason is None:
                reason = "no reason in particular, I guess they just hate you..."

            invite = await ctx.channel.create_invite()
            embed = discord.Embed(
                title=f"You have been banned from {ctx.guild.name} for {reason}",
                description=f"Use this {str(invite)} to join after {duration}s",
                color=discord.Color.random()
            )
            embed.set_image(url=random.choice(banned_gifs))
            try:
              await member.send(embed=embed)
            except:
              print("Could not DM him")
            
            await ctx.guild.ban(member)
            embed1 = discord.Embed(
                title=f"{member.display_name} has been banned for {reason}",
                description=f"They will be allowed to return in {duration}s",
                color=discord.Color.random()
            )
            embed1.set_image(url=random.choice(banned_gifs))
            await ctx.send(embed=embed1)
            await asyncio.sleep(duration)
            await ctx.guild.unban(member)
            await ctx.channel.send(embed=discord.Embed(
                title=f"{member.display_name} has been unbanned.",
                description=f"They will be here soon enough...",
                color=discord.Color.random()
            ))

        else:
            await ctx.send(
                embed=discord.Embed(title="Stop right there!", description="You require the Ban Member permission.",
                                    color=discord.Color.green()))


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        banned_gifs = ["https://media.tenor.com/images/d41f93e7538f0afb56ad1450fed9c02e/tenor.gif",
                       "https://media.tenor.com/images/048b3da98bfc09b882d3801cb8eb0c1f/tenor.gif",
                       "https://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif",
                       "https://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif",
                       "https://media.tenor.com/images/1a84c478d1073757cf8929a89e47bbfc/tenor.gif"]

        if member == ctx.message.author:
            if member == ctx.author:
                embed = discord.Embed(title="Why would you even DO that?",
                                      description=f"Did you really just try to ban yourself? :person_facepalming: ",
                                      color=discord.Color.random())
                embed.set_footer(text="Sometimes I just wonder...")

                await ctx.send(embed=embed)
                return
        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Nuh uh not happening",
                                  description="You can't just ban your fellow admins.",
                                  color=discord.Color.random())
            await ctx.send(embed=embed)
            return

        if reason is None:
            reason = "No reason specified"
        message = discord.Embed(title=f"You have been banned from {ctx.guild.name} for {reason}", color=discord.Color.random())
        try:
          await member.send(embed=message)

        except:
          print("Could not DM him")
        await ctx.guild.ban(member)
        await ctx.channel.send(f"{member} is banned!")
        embed1 = discord.Embed(
            title=f"{member.display_name} has been banned for {reason}",
            description=f"Their mouth has been perma-shut",
        )
        embed1.set_image(url=random.choice(banned_gifs))
        await ctx.send(embed=embed1)

    else:
        await ctx.send(
            embed=discord.Embed(title="Stop right there!", description="You require the Ban Member permission.",
                                color=discord.Color.green()))


@bot.command()
async def dictionary(ctx, *, keyword):
    dictionary = PyDictionary()

    def check(what_to_do):
        return ctx.author == what_to_do.author and what_to_do.channel == ctx.channel

    await ctx.send(embed=discord.Embed(title="What would you like to find?", color=discord.Color.random()))
    what_to_do = await bot.wait_for("message", check=check)

    try:
        if "meaning" in str(what_to_do.content).lower():
            try:
                meaning = dictionary.meaning(keyword)
                embed = discord.Embed(title=f"The Meaning of {keyword}.", color=discord.Color.random())

                if meaning.get('Noun') is not None:
                    for i in range(0, len(meaning['Noun'])):
                        embed.add_field(name=f"Meaning {i + 1}:", value=f"{(meaning['Noun'])[i]}")
                if meaning.get('Verb') is not None:
                    for i in range(0, len(meaning['Verb'])):
                        embed.add_field(name=f"Meaning {i + 1}:", value=f"{(meaning['Verb'])[i]}")
                await ctx.send(embed=embed)
            except:
                print('Meaning not found')

        if "synonym" in str(what_to_do.content).lower():
            try:
                synonym_list = dictionary.synonym(keyword)
                string = ""
                for i in range(0, len(synonym_list)):
                    string += f"{i + 1}. {synonym_list[i]}\n"
                embed = discord.Embed(title=f"The Synonyms of {keyword}.", description=string, color=discord.Color.random())
                await ctx.send(embed=embed)
            except:
                print('Synonym not found')

        if "antonym" in str(what_to_do.content).lower():
            try:
                antonym_list = dictionary.antonym(keyword)
                string = ""
                for i in range(0, len(antonym_list)):
                    string += f"{i + 1}. {antonym_list[i]}\n"
                embed = discord.Embed(title=f"The Antonyms of the {keyword}.", description=string, color=discord.Color.random())
                await ctx.send(embed=embed)
            except:
                print('Antonym not found')

    except:
        embed = discord.Embed(title="Error could not find")
        await ctx.send(embed=embed)


@bot.command()
async def translate(ctx, *, keyword):
    translator = Translator()

    def check(translate_to):
        return ctx.author == translate_to.author and translate_to.channel == ctx.channel

    await ctx.send(embed=discord.Embed(title="Choose your language"))
    translate_to = await bot.wait_for("message", check=check)
    translate_to = translate_to.content
    translate_to = languages.translate(str(translate_to))
    translation = translator.translate(keyword, dest=translate_to)
    if translate_to == "Undetected":
        embed = discord.Embed(title="Translate", description="This language is not supported by us.")
        embed.add_field(name="Possible Issues",
                        value=f"1. You have typed an invalid language.\n2. We don't support this language (if this is the case, come to our support server)")
    else:
        embed = discord.Embed(title="Translate",
                              description=f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
    embed.color = discord.Color.random()

    await ctx.send(embed=embed)


@bot.command()
async def wiki(ctx, *, question):
    try:
        wiki = wikipedia.summary(question, 2)
        embed = discord.Embed(
            title="According to Wikipedia: ",
            description=f"{wiki}"
        )
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        embed.color = 0x0000ff
        await ctx.send(embed=embed)
    except:
        await ctx.send(f"Could not find wikipedia results for: {question}")


@bot.command()
async def weather(ctx, *, place):
    api_key = "6d7ac869f461ec0dc59fdf3a7da78262"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + place
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature_kelvin = y["temp"]
        current_temperature_fahrenheit = round((current_temperature_kelvin - 273.15) * 9 / 5 + 32)
        current_temperature_celsius = round(current_temperature_kelvin - 273.15)
        current_pressure = round(y["pressure"])
        current_humidiy = round(y["humidity"])
        z = x["weather"]
        weather_description = z[0]["description"]
        embed = discord.Embed(
            title=f"Weather in {place}",
            description=" Temperature (in fahrenheit) = " +
                        str(current_temperature_fahrenheit) +
                        "\n Temperature (in celsius) = " +
                        str(current_temperature_celsius) +
                        "\n Atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
                        "\n Humidity (in percentage) = " +
                        str(current_humidiy) +
                        "\n Description = " +
                        str(weather_description)
        )
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        embed.color = 0x0000ff
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title=f"Sorry could not find the weather in {place}", color=discord.Color.dark_teal())
        await ctx.send(embed=embed)


@bot.command()
async def urban(ctx, *, keyword: str):
    try:
        list = (urbandict.define(keyword))
        embed = discord.Embed(title=f"Meaning of {keyword} in urban dict.")
        for i in range(0, len(list) - 1):
            embed.add_field(name=f"Type {i + 1}:",
                            value=f"Word: {(list[i])['word']}\n Definition: {(list[i])['def']}\n Examples: {(list[i])['example']}",
                            inline=False,
                            color=discord.Color.random())
        await ctx.send(embed=embed)
    except:
        await ctx.send(embed=discord.Embed(title=f"Sorry mate i couldn't find sh*t for", description=f"```{keyword}```",
                                           color=discord.Color.random()))


@bot.command()
async def ask(ctx, *, question):
    message = ctx.message.content.lower()
    list = ["will", "how", "why", "is",
            "when", "where", "who", "whom", "I", "@", "can", "am", "should", "are", "were", "if", "did", "does", "do",
            "has", "was"]

    bool = False
    for x in list:
        if x in message.split():
            bool = True
    if bool == False:
        return await ctx.send(embed=discord.Embed(title="Invalid question format.",color=discord.Color.random()))

    question=await commands.clean_content().convert(ctx,question)
    question=question.replace('@',"")
    embed = discord.Embed(title=question, description=
    random.choice([
        "It is certain :8ball:", "It is decidedly so :8ball:",
        "Without a doubt :8ball:", "Yes, definitely :8ball:",
        "You may rely on it :8ball:", "As I see it, yes :8ball:",
        "Most likely :8ball:", "Outlook good :8ball:", "Yes :8ball:",
        "Signs point to yes :8ball:", "Reply hazy try again :8ball:",
        "Ask again later :8ball:", "Better not tell you now :8ball:",
        "Cannot predict now :8ball:", "Concentrate and ask again :8ball:",
        "Don't count on it :8ball:", "My reply is no :8ball:",
        "My sources say no :8ball:", "Outlook not so good :8ball:",
        "Very doubtful :8ball:"
    ]), color=discord.Color.blue())
    await ctx.send(embed=embed)


@bot.command()
async def gif(ctx, *, q="random"):

    api_key = os.environ['giphy_api']
    api_instance = giphy_client.DefaultApi()
    try: 
    # Search Endpoint
        
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=q)
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb)
    except ApiException as e:
        emb = discord.Embed(title=q,description="Sorry could not find anything matching that",color=discord.Color.random())
        await(ctx.send(embed=emb))


@commands.cooldown(1, 30, commands.BucketType.guild)
@bot.command()
async def repeat(ctx, times, *, msg):
    try:
        times = int(times)
        if '@' in str(msg):
          await ctx.send(embed=discord.Embed(title="Imagine spam pinging someone",color=discord.Color.random()))
          return
        if 0 < times <= 70:
            for times in range(0, times):
                await ctx.send(msg)
        elif times < 0:
            await ctx.send(embed=discord.Embed(title="I don't spam a negative number of times."),
                           color=discord.Color.random())
        elif times == 0:
            await ctx.send(embed=discord.Embed(title="Done -_-"),
                           color=discord.Color.random())
        else:
            await ctx.send(
                embed=discord.Embed(title="That is too much for me to handle, try a number below 70",
                                    color=discord.Color.random()))
    except:
        await ctx.send(embed=discord.Embed(title="I need a NUMBER"),
                       color=discord.Color.random())


@bot.command()
async def dice(ctx):
    digit = random.randint(1, 6)
    embed = discord.Embed(title=f"I rolled a dice and got {digit}", color=discord.Color.orange())
    if digit == 1:
        embed.set_image(url="https://www.calculator.net/img/dice1.png")
    if digit == 2:
        embed.set_image(url="https://www.calculator.net/img/dice2.png")

    if digit == 3:
        embed.set_image(url="https://www.calculator.net/img/dice3.png")

    if digit == 4:
        embed.set_image(url="https://www.calculator.net/img/dice4.png")

    if digit == 5:
        embed.set_image(url="https://www.calculator.net/img/dice5.png")

    if digit == 6:
        embed.set_image(url="https://www.calculator.net/img/dice6.png")

    await ctx.send(embed=embed)


@bot.command()
async def epicgamerrate(ctx, member: discord.Member = None):
    num = random.randint(1, 100)
    if member is None:
        member = ctx.author

    embed = discord.Embed(
        title=f"Epic Gamer Rate :sunglasses:",
        description=f"{member.mention} is {num}% epic gamer."
    )
    embed.color = 0x0000ff
    embed.set_footer(text="Gamers = Poggers")
    await ctx.send(embed=embed)


@bot.command()
async def simprate(ctx, member: discord.Member = None):
    num = random.randint(1, 100)
    if member is None:
        member = ctx.author
    embed = discord.Embed(
        title=f"Simp Rate :blush:",
        description=f"{member.mention} is {num}% simp."
    )
    embed.color = 0x0000ff
    embed.set_footer(text="Their favourite show be the SIMPsons")
    await ctx.send(embed=embed)


@bot.command()
async def poll(ctx, duration: TimeConverter, *, argument: str):
    if duration != 0:
        voters = []
        vote_counts = {}

        if ':' in argument:
            split_question = argument.split(':', maxsplit=1)
            question = split_question[0]
        else:
            await ctx.send(embed=discord.Embed(title="You must put a colon(:) after your poll question.", color=discord.Color.random()))
            return

        if ',' in split_question[1]:
            options = split_question[1].split(',')

        else:
            await ctx.send(embed=discord.Embed(title="You must put a comma(,) after each poll options.", color=discord.Color.random()))
            return

        react_to_option = {}
        description = ""
        for i, option in enumerate(options):
            option = options[i]
            description += emojiLetters[i] + " " + option + "\n"
            react_to_option[emojiLetters[i]] = option
        print(react_to_option)
        # Initialize vote_counts dictionary
        for option in options:
            vote_counts[option] = 0
        print(vote_counts)
        my_poll = discord.Embed(
            title=question,
            description=description, color=0x00e6b8
        )
        creator = ctx.author
        message = await ctx.send(embed=my_poll)
        start_time = datetime.datetime.now()

        for i, option in enumerate(options):
            await message.add_reaction(emojiLetters[i])
        # TODO: Create poll object using PollManager

        # Get votes
        reaction = None

        def check(reaction, user):
            return reaction.message.id == message.id and user.id != 861828663958831185

        while True:  # Exit after a certain time
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=1.0, check=check)
                if not user.bot:
                    await message.remove_reaction(reaction, user)
                # Check if the user has already voted
                if user not in voters:
                    voters.append(user)

                    vote_counts[react_to_option[reaction.emoji]] += 1
                    print(vote_counts)

            except asyncio.TimeoutError:
                if datetime.datetime.now() > start_time + datetime.timedelta(seconds=duration):
                    break

        # Send messages of results
        print("done")
        results = ""
        for option in vote_counts:
            results += option + ": " + str(vote_counts[option]) + "\n"

        # Check if the user has already voted

        results_message = discord.Embed(
            title="Results of " + question,
            description=results, color=discord.Color.random()
        )
        print(vote_counts)
        await message.clear_reactions()
        await ctx.send(embed=results_message)


    else:
        await ctx.send(embed=discord.Embed(title="Please mention a valid duration!"), color=discord.Color.random())


@bot.command()
async def ascii(ctx, *, txt: str):
    txt = await commands.clean_content().convert(ctx, txt)
    split_text = txt.split(' ', maxsplit=1)
    if split_text[0].lower() == 'remove':
        await ctx.message.delete()
        result = pyfiglet.figlet_format(split_text[1])
    else:
        result = pyfiglet.figlet_format(txt)
    await ctx.send("```" + result + "```")


@bot.command()
async def act(ctx, member: discord.Member, *, message=None):
        
        if message == None:
                await ctx.send(embed=discord.Embed(title= f'Please provide a message with that!',color=discord.Color.random()))
                return

        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=member.name)
        await webhook.send(
            message, username=member.display_name, avatar_url=member.avatar_url)
        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
                 await webhook.delete()


@bot.command()
async def encrypt(ctx, *, text_to_encrypt: str):
    valid_reactions = ['<:trash:867001275634417714>']
    embed = discord.Embed(title="Encoding your message <a:zo_typing:873129455483256832>",
                          description="This stays in between us. :wink:\n Keep this a secret. :zipper_mouth:")
    embed.color = discord.Color.dark_blue()
    embed.set_footer(text="You all saw NOTHING")
    embed.add_field(name="Encrypted Text", value='```' + enc.encrypt_text(text_to_encrypt) + '```')
    message = await ctx.send(embed=embed)
    await message.add_reaction('<:trash:867001275634417714>')

    def check(reaction, user):
        return reaction.message == message and str(
            reaction.emoji) == '<:trash:867001275634417714>' and user == ctx.author

    await bot.wait_for('reaction_add', check=check)

    await message.delete()


@bot.command()
async def decrypt(ctx, *, text_to_decrypt: str):
    embed = discord.Embed(title="Decoding your message <a:zo_typing:873129455483256832>",
                          description="This is your message. :face_with_monocle:\n Hope you have what you need. :slight_smile:")
    embed.color = discord.Color.dark_blue()

    embed.add_field(name="Encrypted Text", value='```' + dec.decrypt_text(text_to_decrypt) + '```')
    message = await ctx.send(embed=embed)
    await message.add_reaction('<:trash:867001275634417714>')

    def check(reaction, user):
        return reaction.message == message and str(
            reaction.emoji) == '<:trash:867001275634417714>' and user == ctx.author

    await bot.wait_for('reaction_add', check=check)
    await message.delete()


def toBinary(a):
    l, m = [], []
    for i in a:
        l.append(ord(i))
    for i in l:
        m.append(int(bin(i)[2:]))
    return m


@bot.command()
async def binary(ctx, *, string: str):
    def toBinary(a):
        l, m = [], []
        for i in a:
            l.append(ord(i))
        for i in l:
            m.append(int(bin(i)[2:]))

        return m

    a = toBinary(string)
    b = ' '.join(str(e) for e in a)
    embed = discord.Embed(title=f"Your text converted to binary.",
                          description="My devs are Zero And One.\nObviously I have a binary feature.",
                          color=discord.Color.random())
    embed.add_field(name=string, value=f"{b}", inline=False)
    embed.set_footer(text="I respect my devs")
    await ctx.send(embed=embed)


@bot.command()
async def choose(ctx, *choices: str):
    embed = discord.Embed(
        title=f"I choose...",
        description=f"{random.choice(choices)}"
    )
    embed.color = discord.Color.random()
    embed.set_footer(
        text=f"It is better and I am awesome")
    await ctx.send(embed=embed)


@bot.command()
async def coinflip(ctx, *, option=None):
    if option != None:
        choice = option.lower()
        r = random.randint(1, 2)
        if r == 1:
            r = 'heads'
        elif r == 2:
            r = 'tails'
        boolean = False

        if choice == r:
            result = f'You win! :grin:'
            boolean = False
        elif choice != r and choice == 'heads' or choice == 'tails':
            result = f'You lose. :cry:'
            boolean = False
        else:
            result = 'Invalid option. :rolling_eyes:'
            boolean = True

        if boolean is False:
            embed = discord.Embed(
                title=f"{result}",
                description=f"It was {r}."
            )
            embed.color = 0x0000ff

        elif boolean is True:
            embed = discord.Embed(
                title=f"{result}",
                description=f"Please enter either heads or tails next time. \nIt was {r}."
            )
            embed.color = 0x0000ff
    else:
        embed = discord.Embed(
            title=f"Your kidding. :angry:",
            description="You gotta choose an option. \nIf you don't wanna play then go away.\n Don't bother me.",
        )
        embed.color = 0x0000ff
        embed.set_footer(text=f"The Freeloaders are here")

    await ctx.send(embed=embed)


@bot.command()
async def guess(ctx, lower, upper):
    boolean = False
    lower = int(lower)
    upper = int(upper)
    if upper < lower:
        embed = discord.Embed(title="Nope :satisfied:",
                              description="Your upper limit CANNOT BE less then your lower limit smh")
        embed.set_footer(text="Like, wth dude")
        embed.color = discord.Color.random()
        await ctx.send(embed=embed)
        return
    if upper == lower:
        embed = discord.Embed(title="Nope :satisfied:",
                              description="Think about it.\nIf your lower limit is the same as the upper limit, you can't really guess anything.")
        embed.set_footer(text=f"Basically, its obviously {upper} rn")
        embed.color = discord.Color.random()
        await ctx.send(embed=embed)
        return
    if lower < 0:
        embed = discord.Embed(title="Nope :satisfied:",
                              description="Your limits can only be positive numbers.")
        embed.set_footer(text="Dont' even THINK about it")
        await ctx.send(embed=embed)
        embed.color = discord.Color.random()
        return
    if upper > 10000:
        embed = discord.Embed(title="Nope :satisfied:",
                              description="Your upper limit can only be equal to or less than 10000.")
        embed.set_footer(text="Dont' even THINK about it")
        embed.color = discord.Color.random()
        await ctx.send(embed=embed)
        return
    x = random.randint(lower, upper)
    embed = discord.Embed(
        title=f"You have {round(math.log(upper - lower + 1, 2))} chances to guess the number!",
        description="Good Luck :thumbsup:"
    )
    embed.color = discord.Color.random()
    await ctx.send(embed=embed)
    count = 1

    while count <= round(math.log(upper - lower + 1, 2)):
        count += 1

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await bot.wait_for("message", check=check)
        guess = int(str(msg.content))

        if x == guess:
            embed = discord.Embed(
                title=f"You did it! :partying_face:",
                description=f"You have guessed the number!\n It was {x}"
            )
            embed.color = discord.Color.random()
            await ctx.send(embed=embed)
            boolean = True
            break

        elif x > guess:
            if (round(math.log(upper - lower + 1, 2)) - count + 1) == 0:
                break
            embed = discord.Embed(
                title=f"You guessed too low! :arrow_down:",
                description=f"You have {round(math.log(upper - lower + 1, 2)) - count + 1} remaining!"
            )
            embed.color = discord.Color.random()
            await ctx.send(embed=embed)

        elif x < guess:
            if (round(math.log(upper - lower + 1, 2)) - count + 1) == 0:
                break
            embed = discord.Embed(
                title=f"You guessed too high! :arrow_up:",
                description=f"You have {round(math.log(upper - lower + 1, 2)) - count + 1} remaining!"
            )
            embed.color = discord.Color.random()
            await ctx.send(embed=embed)

        if round(math.log(upper - lower + 1, 2)) - count + 1 == 0:
            break

    if boolean is False:
        embed = discord.Embed(title="Better luck next time!",
                              description=f"The number was {x}")
        embed.color = discord.Color.random()
        await ctx.send(embed=embed)


@bot.command()
async def hack(ctx, member: discord.User):
    extensions_list = ["au", "in", "us", "uk", "fr"]
    emails_list = [f"{str(member.name)}@gmail.com",
                   f"{str(member.name)}@yahoo.co.{extensions_list[random.randint(0, 4)]}",
                   f"{str(member.name)}_is_cool@smallppmail.com",
                   f"{member.name}{str(random.randint(1, 100))}{str(random.randint(1, 100))}{str(random.randint(1, 100))}@gmail.com",
                   f"{str(member.name)}@oogamail.{random.choice(extensions_list)}"]
    passwords_list = [f"Deadpool{str(random.randint(1, 20))}{str(random.randint(1, 20))}{str(random.randint(1, 20))}",
                      "Ineedfriends123", "ChamakChalo!@", "OogaBooga69", "@d****isaqt", "IluvCoffinDance2020"]
    dms_list = ["Yo i got ignored by her again", "Yup it's 3 inches", "Man i wanna punch you", "I really need friends",
                "Sure k", "THATS WHAT SHE SAID", "OOH GET REK'D", "lmao", "ooga", "That's cool",
                "NOOO DONT FRIENDZONE ME PLSSSSSSS"]
    common_words = ["mom", "cringe", "LOL", "bOb", "pp", "yes", "ooga"]
    IPS = ["46.193.82.45",
           "19.139.7.84",
           "237.16.92.184",
           "230.23.100.200",
           "100.234.227.192",
           "146.202.187.26",
           "237.6.170.85",
           "122.236.83.78",
           "207.95.203.62",
           "133.217.120.204",
           "237.36.146.217",
           "176.49.159.213",
           "64.171.92.234",
           "36.19.97.53",
           "199.12.190.203",
           "82.91.235.250",
           "39.21.236.178",
           "228.181.137.57",
           "7.51.143.121",
           "100.96.194.206"]
    hack_embed_1 = discord.Embed(title=f"Hacking {member.display_name}.....",
                                 description=f"Brute-forcing passwords and emails....")
    hack_embed_2 = discord.Embed(title=f"Login Credentials of {member.display_name}")
    hack_embed_2.add_field(name="Email", value=f"`{random.choice(emails_list)}`", inline=False)
    hack_embed_2.add_field(name="Password", value=f"`{random.choice(passwords_list)}`", inline=False)
    hack_embed_3 = discord.Embed(name="Fetching last DMs....")
    hack_embed_3.add_field(name="Last DMs", value=f"{random.choice(dms_list)}")
    hack_embed_4 = discord.Embed(title="Finding most commonly used word......")
    hack_embed_4.add_field(name=f"`Const_Commonly_used word=discord.Query(WordList[{member.display_name}])`",
                           value=random.choice(common_words))
    hack_embed_5 = discord.Embed(
        title=f"Inserting Virus into Discriminator: {member.discriminator} <a:ZO_IconLoadingGreen:866710482328485908>")
    hack_embed_6 = discord.Embed(title=f"Grabbing IP address of {member.display_name}......")
    hack_embed_6.add_field(name="IP Address", value=random.choice(IPS))
    hack_embed_7 = discord.Embed(title=f"Done hacking {member}",
                                 description="It was totally real and flipping accurate")
    hack_embed_5.set_thumbnail(url=member.avatar_url)
    hack_embed_7.set_thumbnail(url=member.avatar_url)
    hack_embed_6.set_thumbnail(url=member.avatar_url)
    hack_embed_4.set_thumbnail(url=member.avatar_url)
    hack_embed_3.set_thumbnail(url=member.avatar_url)
    hack_embed_2.set_thumbnail(url=member.avatar_url)
    hack_embed_1.set_thumbnail(url=member.avatar_url)
    hack_embed_1.color = discord.Color.random()
    hack_embed_2.color = discord.Color.random()
    hack_embed_3.color = discord.Color.random()
    hack_embed_4.color = discord.Color.random()
    hack_embed_5.color = discord.Color.random()
    hack_embed_6.color = discord.Color.random()
    hack_embed_7.color = discord.Color.random()
    message = await ctx.send(embed=hack_embed_1)
    await asyncio.sleep(5)
    await message.edit(embed=hack_embed_2)
    await asyncio.sleep(5)
    await message.edit(embed=hack_embed_3)
    await asyncio.sleep(5)
    await message.edit(embed=hack_embed_4)
    await asyncio.sleep(5)
    await message.edit(embed=hack_embed_5)
    await asyncio.sleep(5)
    await message.edit(embed=hack_embed_6)
    await asyncio.sleep(5)
    await message.edit(embed=hack_embed_7)


def adjust_text(text, draw, font):
    bits = []
    bit = ""
    for n, c in enumerate(text):
        bit += c
        if draw.textsize(bit, font=font)[0] > 305:
            bits.append(bit)
            bit = ""
        elif n == len(text) - 1:
            bits.append(bit)
    text = "\n".join(bits)
    if draw.textsize(text, font=font)[1] > 199 - 70:
        while draw.textsize(text, font=font)[1] > 199 - 70:
            text = text[:-1]
    return text


@bot.command()
async def imagememes(ctx):
    embed = discord.Embed(title="Image Memes List",
                          description="Here is the list of POG image memes you can use.",
                          inline=False)
    embed.add_field(name="List", value=f"1. {ctx.prefix}worthless\n2. {ctx.prefix}wanted\n3. {ctx.prefix}rip\n4. {ctx.prefix}chad")
    await ctx.send(embed=embed)


@bot.command()
async def worthless(ctx, *, worthless_text):
    img = Image.open('templates/worthless_template.jpg')
    draw = ImageDraw.Draw(img)
    txt = await commands.clean_content().convert(ctx, worthless_text)
    font = ImageFont.truetype("fonts/Roboto-Regular.ttf", size=21)
    text = adjust_text(txt, draw, font)
    draw.text((70, 70), text, (0, 0, 0), font=font)
    guild_id = str(ctx.guild.id)
    author_id = str(ctx.author.id)
    time1 = str(time.time())
    img.save(f'images/{guild_id + author_id + time1}.png')
    await ctx.send(file=discord.File(f'images/{guild_id + author_id + time1}.png'))


@bot.command()
async def wanted(ctx, user: discord.Member = None):
    if not user:
        user = ctx.author

    wanted = Image.open('templates/wanted_template.jpg')
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((224, 224))

    wanted.paste(pfp, (116, 216))
    guild_id = str(ctx.guild.id)
    author_id = str(ctx.author.id)
    time1 = str(time.time())
    wanted.save(f'images/{guild_id + author_id + time1}.png')
    await ctx.send(file=discord.File(f'images/{guild_id + author_id + time1}.png'))


@bot.command()
async def rip(ctx, user: discord.Member = None):
    if not user:
        user = ctx.author

    rip = Image.open('templates/rip_template.jpg').convert("RGBA")
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((240, 211))
    pfp = pfp.convert('RGB')

    mask = Image.new("L", pfp.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
    rip.paste(pfp, (82, 235), mask=mask)
    guild_id = str(ctx.guild.id)
    author_id = str(ctx.author.id)
    time1 = str(time.time())
    rip.save(f'images/{guild_id + author_id + time1}.png')
    await ctx.send(file=discord.File(f'images/{guild_id + author_id + time1}.png'))


@bot.command()
async def chad(ctx, user: discord.Member = None):
    if not user:
        user = ctx.author

    chad = Image.open('templates/chad_template.jpg').convert("RGBA")
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((298, 335))
    pfp = pfp.convert('RGB')
    mask = Image.new("L", pfp.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
    chad.paste(pfp, (105, 2), mask=mask)
    guild_id = str(ctx.guild.id)
    author_id = str(ctx.author.id)
    time1 = str(time.time())
    chad.save(f'images/{guild_id + author_id + time1}.png')
    await ctx.send(file=discord.File(f'images/{guild_id + author_id + time1}.png'))


@bot.command()
async def vcmeme(ctx, *, meme: str):
    if meme != None:
        try:
            channel = ctx.message.author.voice.channel
            print(channel)
        except:
            ctx.send("JOIN A CHANNEL FIRST!!!!")
            return
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
            if "20th century" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/20th Century.mp3'))
            elif "airhorn" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/AirHorn.mp3'))
                print("Airhorn.....")
            elif "big pew pew" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Big pew pew.mp3'))

            elif "censor" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/CENSOR BEEP.mp3'))

            elif "denied" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/DENIED.mp3'))

            elif "drum roll" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/DRUM ROLL.mp3'))

            elif "dun dun dun" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/DUN DUN DUN.mp3'))

            elif "elevator music" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Elevator Music.mp3'))

            elif "headshot" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Headshot.mp3'))

            elif "explosion" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/EXPLOSION.mp3'))
            elif "hidden agenda" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/HIDDEN AGENDA.mp3'))

            elif "huh" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Huh.mp3'))

            elif "illuminati confirmed" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Illuminati Confirmed.mp3'))

            elif "investigations" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/INVESTIGATIONS.mp3'))

            elif "oof" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Oof.mp3'))

            elif "pew" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/pew.mp3'))

            elif "pew pew" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/pew pew.wav'))

            elif "reee" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/REEEEE.m4a'))

            elif "sad music" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/SAD MUSIC.mp3'))

            elif "say what" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/SAY WHAT.mp3'))

            elif "sneaky snitch" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/SNEAKY SNITCH.mp3'))

            elif "stop right there" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/STOP RIGHT THERE.m4a'))

            elif "surprise mf" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Surprise Mf.mp3'))

            elif "why are you running" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Why are you running.mp3'))

            elif "why you bully me" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Why you bully me.mp3'))

            elif "wow" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/WOW.m4a'))

            elif "yeet" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/YEET.m4a'))
            elif "yay" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/YAY.mp3'))
            elif "you got it dude" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/You got it dude.mp3'))
            else:
                embed2 = discord.Embed(title=f"The meme {meme} was not found!",
                                       description="Thanks for wasting my time!",
                                       color=discord.Color.Red())
                embed2.add_field(
                    f"If you would like the owners to add a voice meme, [click here](https://zeroandone.ml/contact/)")
                await ctx.send(embed=embed2)
                voice.disconnect()

        else:
            voice = await channel.connect()
            if "20th century" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/20th Century.mp3'))
            elif "airhorn" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/AirHorn.mp3'))
                print("Airhorn.....")
            elif "big pew pew" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Big pew pew.mp3'))

            elif "censor" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/CENSOR BEEP.mp3'))

            elif "denied" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/DENIED.mp3'))

            elif "drum roll" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/DRUM ROLL.mp3'))

            elif "dun dun dun" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/DUN DUN DUN.mp3'))

            elif "elevator music" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Elevator Music.mp3'))

            elif "headshot" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Headshot.mp3'))

            elif "explosion" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/EXPLOSION.mp3'))
            elif "hidden agenda" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/HIDDEN AGENDA.mp3'))

            elif "huh" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Huh.mp3'))

            elif "illuminati confirmed" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Illuminati Confirmed.mp3'))

            elif "investigations" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/INVESTIGATIONS.mp3'))

            elif "oof" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Oof.mp3'))

            elif "pew" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/pew.mp3'))

            elif "pew pew" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/pew pew.wav'))

            elif "reee" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/REEEEE.m4a'))

            elif "sad music" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/SAD MUSIC.mp3'))

            elif "say what" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/SAY WHAT.mp3'))

            elif "sneaky snitch" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/SNEAKY SNITCH.mp3'))

            elif "stop right there" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/STOP RIGHT THERE.m4a'))

            elif "surprise mf" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Surprise Mf.mp3'))

            elif "why are you running" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Why are you running.mp3'))

            elif "why you bully me" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/Why you bully me.mp3'))

            elif "wow" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/WOW.m4a'))

            elif "yeet" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/YEET.m4a'))
            elif "yay" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/YAY.mp3'))
            elif "you got it dude" in meme.lower():
                voice.play(discord.FFmpegPCMAudio(
                    source='sounds/You got it dude.mp3'))
            else:
                embed2 = discord.Embed(title=f"The meme {meme} was not found!",
                                       description="Thanks for wasting my time!",
                                       color=discord.Color.Red())
                embed2.add_field(
                    f"If you would like the owners to add a voice meme, [click here](https://zeroandone.ml/contact/)")
                await ctx.send(embed=embed2)
                voice.disconnect()


@vcmeme.error
async def vcmeme_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Here is the list of all VC MEMES", color=discord.Color.gold())
        embed.add_field(name="1", value=f"20th Century", inline=False)
        embed.add_field(name="2", value=f"AirHorn", inline=False)
        embed.add_field(name="3", value=f"Big pew pew", inline=False)
        embed.add_field(name="4", value=f"Bye", inline=False)
        embed.add_field(name="5", value=f"CENSOR BEEP", inline=False)
        embed.add_field(name="6", value=f"DENIED", inline=False)
        embed.add_field(name="7", value=f"DRUM ROLL", inline=False)
        embed.add_field(name="8", value=f"DUN DUN DUN", inline=False)
        embed.add_field(name="9", value=f"Elevator Music", inline=False)
        embed.add_field(name="10", value=f"EXPLOSION", inline=False)
        embed.add_field(name="11", value=f"Headshot", inline=False)
        embed.add_field(name="12", value=f"HIDDEN AGENDA", inline=False)
        embed.add_field(name="13", value=f"Huh", inline=False)
        embed.add_field(name="14", value=f"Illuminati Confirmed", inline=False)
        embed.add_field(name="15", value=f"INVESTIGATIONS", inline=False)
        embed.add_field(name="16", value=f"OH HELLO THERE", inline=False)
        embed.add_field(name="17", value=f"Oof", inline=False)
        embed.add_field(name="18", value=f"pew", inline=False)
        embed.add_field(name="19", value=f"REEEEE", inline=False)
        embed.add_field(name="20", value=f"pew pew", inline=False)
        embed.add_field(name="21", value=f"SAD MUSIC", inline=False)
        embed.add_field(name="22", value=f"SAY WHAT", inline=False)
        embed.add_field(name="23", value=f"SNEAKY SNITCH", inline=False)
        embed.add_field(name="24", value=f"STOP RIGHT THERE", inline=False)
        embed.add_field(name="25", value=f"Surprise Mf", inline=False)
        embed2 = discord.Embed(title="Here is the list of all VC MEMES(continued)", color=discord.Color.gold())
        embed2.add_field(name="26", value=f"Why are you running", inline=False)
        embed2.add_field(name="27", value=f"Why you bully me", inline=False)
        embed2.add_field(name="28", value=f"WOW", inline=False)
        embed2.add_field(name="29", value=f"YAY", inline=False)
        embed2.add_field(name="30", value=f"YEET", inline=False)
        embed2.add_field(name="31", value=f"You got it dude", inline=False)
        embed2.set_footer(text="Don't worry this is not case sensitive")
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)


    else:
        raise (error)


@bot.command()
async def shoo(ctx):
    try:
        channel = ctx.message.author.voice.channel
        await ctx.voice_client.disconnect()
        await ctx.send(f"Left {channel}")

    except:
        await ctx.send("You are not connected to a voice channel")


snipe_message_author = {}
snipe_message_content = {}


@bot.command()
async def quote(ctx, quoter, *, quote):
    embed = discord.Embed(
        description=f"\"*{quote}*\""
    )
    embed.color = discord.Color.random()
    quote = await commands.clean_content().convert(ctx, quoter)
    embed.set_footer(text=f"- {quote.replace('@', '')}")
    await ctx.send(embed=embed)


@bot.command()
async def rps(ctx, *, msg=None):
    if msg is None:
        await ctx.send(embed=discord.Embed(title="You might wanna", description="CHOOSE SOMETHING!!",
                                           color=discord.Color.random()))

        return

    if '@' in msg:
        msg = await commands.MemberConverter().convert(ctx, msg)

    if isinstance(msg, str):
        t = ["rock", "paper", "scissors"]
        computer = t[random.randint(0, 2)]
        player = msg.lower()
        if player == computer:
            embed = discord.Embed(
                title="Tie",
                description=f"I played {player} too!")
            embed.color = 0x000fff
            embed.set_footer(text="Its not over yet...")
            await ctx.send(embed=embed)

        elif player == "rock" or player == "r":
            if computer == "paper":
                embed = discord.Embed(
                    title="You lose!",
                    description=f"{t[1]} covers {t[0]}".format(computer, player))
                embed.color = 0x000fff
                embed.set_footer(text="Sad life 4 u...")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="You win!",
                    description=f"{t[1]} breaks {t[2]}".format(player, computer))
                embed.color = 0x000fff
                embed.set_footer(text="GG")
                await ctx.send(embed=embed)

        elif player == "paper" or player == "p":
            if computer == "scissors":
                embed = discord.Embed(
                    title="You lose!",
                    description=f"{t[2]} cut {t[1]}".format(computer, player))
                embed.color = 0x000fff
                embed.set_footer(text="Sad life 4 u...")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="You win!",
                    description=f"{t[1]} covers {t[0]}".format(player, computer))
                embed.color = 0x000fff
                embed.set_footer(text="GG")  # dont test yet im almost done too
                await ctx.send(embed=embed)

        elif player == "scissors" or player == "s" or player == "s":
            if computer == "rock":
                embed = discord.Embed(
                    title="You lose!",
                    description=f"{t[0]} breaks {t[2]}".format(computer, player))
                embed.color = 0x000fff
                embed.set_footer(text="Sad life 4 u...")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="You win!",
                    description=f"{t[2]} cut {t[1]}".format(player, computer))
                embed.color = 0x000fff
                embed.set_footer(text="GG")
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="What the hell bruh",
                description=f"You have managed to put an invalid option in rock paper scissors. :rolling_eyes:")
            embed.color = 0x000fff
            embed.set_footer(text="Imagine having just 3 brain cells")
            await ctx.send(embed=embed)


    elif isinstance(msg, discord.Member):
        embed1 = discord.Embed(title=f"Hello!! So you have challenged {msg.name} to an epic rock paper scissor battle!",
                               description="Enter your choice from Rock,Paper,Scissors here",
                               color=discord.Color.random())
        embed2 = discord.Embed(
            title=f"Hello! So you have been challenged by {ctx.author.name} to an epic rock paper scissor battle!",
            description="Enter your choice from Rock, Paper or Scissors here (if you wanna play)",
            color=discord.Color.random())
        embed2.set_footer(text="Otherwise just ignore me like everyone else (SOB SOB)")
        await ctx.send("<a:ZO_DMS:871341236236193792>")
        await ctx.author.send(embed=embed1)
        await msg.send(embed=embed2)

        def check1(message):
            return message.author == ctx.author and str(message.channel.type) == "private"
            print(message.type)

        def check2(message):
            return message.author == msg and str(message.channel.type) == "private"

        try:
            reply1 = await bot.wait_for('message', check=check1, timeout=60)
            reply2 = await bot.wait_for('message', check=check2, timeout=60)
            player = reply2.content.lower()
            challenger = reply1.content.lower()
            playerName = msg.name
            challengerName = ctx.author.name
            if player == challenger:
                embed = discord.Embed(
                    title="Tie",
                    description=f"Both played {player}!")
                embed.color = 0x000fff
                embed.set_footer(text="Its not over yet...")
                await ctx.send(embed=embed)

            elif player == "rock":
                if challenger == "paper":
                    embed = discord.Embed(
                        title=f"{challengerName} wins!",
                        description=f"Paper[{challengerName}] covers Rock[{playerName}]!!")
                    embed.color = 0x000fff
                    embed.set_footer(text=f"Sad life {playerName}...")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"{playerName} wins!",
                        description=f"Rock[{playerName}] breaks Scissors[{challengerName}]!!")
                    embed.color = 0x000fff
                    embed.set_footer(text=f"Sad life {challengerName}...")
                    await ctx.send(embed=embed)

            elif player == "paper":
                if challenger == "scissors":
                    embed = discord.Embed(
                        title=f"{challengerName} wins!",
                        description=f"Scissors[{challengerName}] cut paper[{playerName}]!!")
                    embed.color = 0x000fff
                    embed.set_footer(text=f"Sad life {playerName}...")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"{playerName} wins!",
                        description=f"Paper[{playerName}] covers rock[{challengerName}]!!")
                    embed.color = 0x000fff
                    embed.set_footer(text=f"Sad life {challengerName}...")
                    await ctx.send(embed=embed)

            elif player == "scissors":
                if challenger == "rock":
                    embed = discord.Embed(
                        title=f"{challengerName} wins!",
                        description=f"Rock[{challengerName}] breaks scissors[{playerName}]!!")
                    embed.color = 0x000fff
                    embed.set_footer(text=f"Sad life {playerName}...")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"{playerName} wins!",
                        description=f"Scissors[{playerName}] cut paper[{challengerName}]!!")
                    embed.color = 0x000fff
                    embed.set_footer(text=f"Sad life {challengerName}...")
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="Well either you dont want to play or you have not spelled correctly",
                    description=f"Why are you like this.... :rolling_eyes:")
                embed.color = 0x000fff
                embed.set_footer(text="Imagine being such a spoil sport")
                await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(title="That kid didn't answer in time",
                                               description="THEY IGNORED MEEEEE <a:ZO_Cry:871340549725102081>"))

    else:
        await ctx.send(embed=discord.Embed(title="You might wanna", description="CHOOSE SOMETHING USEFUL",
                                           color=discord.Color.random()))


@bot.command()
async def oddeve(ctx, *, msg=None):
    if msg is None:
        await ctx.send(embed=discord.Embed(title="You might wanna", description="CHOOSE SOMETHING!!\n try odd or even",
                                           color=discord.Color.random()))
        return

    if '@' in msg:
        msg = await commands.MemberConverter().convert(ctx, msg)

    if isinstance(msg, str):
        if msg.lower() == "odd":
            euro = "odd"

        elif msg.lower() == "even":
            euro = "even"

        else:
            embed = discord.Embed(
                title="What the hell bruh",
                description=f"You have managed to put an invalid option in odd n even.\nIts either odd or even :rolling_eyes:",
                color=discord.Color.random()
            )
            embed.color = 0x000fff
            embed.set_footer(text="Imagine having just 3 brain cells")
            await ctx.send(embed=embed)
            return

        await ctx.send(embed=discord.Embed(title="Please select a number for 0 to 9", color=discord.Color.random()))

        def check1(message):
            return message.author == ctx.author

        msg1 = await bot.wait_for('message', check=check1, timeout=60)
        num1 = int(msg1.content)
        if num1 >= 10 or num1 < 0:
            await ctx.send(
                embed=discord.Embed(title="WHAT PART OF 1 TO 9 DO YOU NOT UNDERSTAND", color=discord.Color.random()))
            return

        n = i = 0
        while i < 1:
            n = random.randint(0, 9)
            i += 1

        sum = int(num1) + int(n)
        await ctx.send(embed=discord.Embed(title=f"I played {n} and you played {num1} and it adds up to {sum}",
                                           color=discord.Color.random()))

        if (sum % 2 == 0):
            if euro == "even":
                await ctx.send(embed=discord.Embed(title="Result is even", description="You win! \n GGs",
                                                   color=discord.Color.random()))

            else:
                await ctx.send(embed=discord.Embed(title="Result Is even", description="You lose! \n sed leef",
                                                   color=discord.Color.random()))

        else:
            if euro == "even":
                await ctx.send(embed=discord.Embed(title="Result Is Odd", description="You lose! \n sed leef",
                                                   color=discord.Color.random()))

            else:
                await ctx.send(embed=discord.Embed(title="Result Is Odd", description="You win! \n GGs",
                                                   color=discord.Color.random()))




    elif isinstance(msg, discord.Member):
        player = ""
        challenger = ""

        def check3(message):
            return message.author == ctx.author

        def check1(message):
            return message.author == ctx.author and str(message.channel.type) == "private"

        def check2(message):
            return message.author == msg and str(message.channel.type) == "private"

        embed3 = discord.Embed(
            title=f"Hey {ctx.author.display_name}, as you have started the match, you get to choose....",
            description="Choose whether you want \"odd\" or \"even\"", color=discord.Color.random())
        await ctx.send(embed=embed3)
        try:
            reply3 = await bot.wait_for('message', check=check3, timeout=60)
            author_choice = reply3.content.lower()

            if author_choice == "odd":
                challenger = "odd"
                player = "even"
                await ctx.send(f"Alright you have chosen {challenger} so that makes {msg.display_name} {player}")

            elif author_choice == "even":
                challenger = "even"
                player = "odd"
                await ctx.send(f"Alright you have chosen {challenger} so that makes {msg.display_name} {player}")

            else:
                embed = discord.Embed(
                    title="What the hell bruh",
                    description=f"You have managed to put an invalid option in odds n evens Its either odd or even :rolling_eyes:",
                    color=discord.Color.random())
                embed.color = 0x000fff
                embed.set_footer(text="Imagine having just 3 brain cells")
                await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(title="You didn't answer in time",
                                               description="HOW DARE YOU IGNORED ME <a:ZO_Cry:871340549725102081>"))
            return

        embed1 = discord.Embed(title=f"Hello!! So you have challenged {msg.name} to an epic odds and evens battle!",
                               description=f"Enter your number from 0 to 9 here\n And remember, you are {challenger}",
                               color=discord.Color.random())

        embed2 = discord.Embed(
            title=f"Hello!! So you have been challenged by {ctx.author.name} to an odds and evens battle!!",
            description=f"Enter your number from 0 to 9 here(if you wanna play)\n And remember, you are {player}",
            color=discord.Color.random())
        embed2.set_footer(text="Otherwise just ignore me like everyone else (SOB SOB)")
        await ctx.send("<a:ZO_DMS:871341236236193792>")
        await ctx.author.send(embed=embed1)
        await msg.send(embed=embed2)

        try:

            reply1 = await bot.wait_for('message', check=check1, timeout=60)
            reply2 = await bot.wait_for('message', check=check2, timeout=60)
            playerno = int(reply2.content)
            challengerno = int(reply1.content)
            playerName = msg.name
            challengerName = ctx.author.name

            if playerno >= 10 or playerno <= 0 or challengerno >= 10 or challengerno <= 0:
                await ctx.send(embed=discord.Embed(title="WHAT PART OF 1 TO 9 DO YOU NOT UNDERSTAND",
                                                   description="You ruined the game man", color=discord.Color.random()))
                return

            sum = int(challengerno) + int(playerno)
            await ctx.send(embed=discord.Embed(
                title=f"{challengerName} played {challengerno} and {playerName} played {playerno} and it adds up to {sum}",
                color=discord.Color.random()))

            if (sum % 2 == 0):
                if player == "even":
                    await ctx.send(
                        embed=discord.Embed(title="Result is even", description=f"{playerName} wins! \n Poggers",
                                            color=discord.Color.random()))

                else:
                    await ctx.send(
                        embed=discord.Embed(title="Result Is even", description=f"{challengerName} wins! \n Poggers",
                                            color=discord.Color.random()))

            else:
                if player == "odd":
                    await ctx.send(
                        embed=discord.Embed(title="Result Is Odd", description=f"{playerName} wins! \n Poggers",
                                            color=discord.Color.random()))

                else:
                    await ctx.send(
                        embed=discord.Embed(title="Result Is Odd", description=f"{challengerName} wins! \n Poggers",
                                            color=discord.Color.random()))


        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(title="That kid didn't answer in time",
                                               description="THEY IGNORED MEEEEE <a:ZO_Cry:871340549725102081>"))

    else:
        await ctx.send(embed=discord.Embed(title="You might wanna", description="CHOOSE SOMETHING USEFUL",
                                           color=discord.Color.random()))


@bot.command()
async def button(ctx):
    await ctx.send(
        "Hello, World!",
        components=[
            Button(label="WOW button!")
        ]
    )
    interaction = await bot.wait_for("button_click", check=lambda i: i.component.label.startswith("WOW"))

    await interaction.respond(content="Button clicked!")


@bot.command()
async def select(ctx):
    await ctx.send(

        "Hello, World!",

        components=[

            Select(placeholder="select something!",
                   options=[SelectOption(label="a", value=f"A"), SelectOption(label="b", value=f"B")])

        ]

    )

    interaction = await bot.wait_for("select_option", check=lambda i: i.component[0].value == "A")

    await interaction.respond(content=f"{interaction.component[0].label} selected!")


@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):

        if ctx.channel.slowmode_delay==0:
          await ctx.send("Slowmode disabled already dumbass")
          return


        if ctx.author.guild_permissions.administrator:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send(embed=discord.Embed(title="Slowmode disabled!", color=discord.Color.dark_magenta(),
                                               description="Now y'all can talk your heart out"))

        else:
            await ctx.send(
                embed=discord.Embed(title="Stop right there!", description="You require the Administrators permission.",
                                    color=discord.Color.green()))

    if isinstance(error, commands.BadArgument):
        await ctx.send(
            embed=discord.Embed(title="How hard is it to set a slowmode :rolling_eyes: ", color=discord.Color.magenta(),
                                description=f"Do {ctx.prefix}slowmode to disable it and {ctx.prefix}slowmode 10 to set slowmode of 10 secs"))


@hack.error
async def hack_error(ctx, error, ):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title="Your kidding right?",
                                           description=f"{member.mention} please mention a user to hack\n That way, I won't need to hack thin air!!",
                                           color=discord.Color.random()))

    elif isinstance(error, commands.UserNotFound):
        await ctx.send(embed=discord.Embed(title="This is ridiculous",
                                           description=f"<:ZO_Bruh:866252668225585152> {member.mention} have the brain cells to mention the target smh.\n How are you unable to MENTION SOMEONE"))

    else:
        raise (error)


@robmoji.error
async def rob_moji_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title="You're kidding right?",
                                           description=f"{member.mention} please mention an emojito steal\n That way, I won't need to steal thin air!!",
                                           color=discord.Color.random()))

    elif isinstance(error, commands.errors.PartialEmojiConversionFailure):
        error = getattr(error, "original", error)
        the_error_arg = error.argument 
        embed=discord.Embed(title="Whoops",
                                           description=f"Could not convert {the_error_arg} to an emoji",color=discord.Color.random())
        embed.set_footer(text="If this is not you being dumb and a genuine error in the code,let us know here (https://discord.gg/TeRyp9JWbg)")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send(embed=discord.Embed(title="You're kidding right?",
                                           description=f"{member.mention} give it a name from 2 to 32 characters **ONLY**\nAnd NO SPACES PLS \n this is an emoji name not a train",
                                           color=discord.Color.random()))

    else:
        raise (error)


@userinfo.error
async def userinfo_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="Did you know...",
                              description="That it is an EXCELLENT idea to actually mention the user whose info you want?",
                              color=discord.Color.random())
        embed.set_footer(text="I mean, common sense people")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="At least try to...",
                              description="Wish you'd actually try to tell me who to get info from.",
                              color=discord.Color.random())
        embed.set_footer(text="Sigh")
        await ctx.send(embed=embed)

    else:
        raise (error)


@makerole.error
async def make_role_error(ctx, error):
    member = ctx.author

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Hmmmm...",
                              description="Why haven't you mentioned the NAME OF THE ROLE YOU WANT TO CREATE\nA role with the name ___ is pretty stupid.",
                              color=discord.Color.random())
        embed.set_footer(text="Think about it")
        await ctx.send(embed=embed)

    else:
        raise (error)


@addrole.error
async def add_role_error(ctx, error):
    member = ctx.author

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="How do you do these things...",
                              description="You gotta mention both the user and the role.\nI can't just randomly place roles!",
                              color=discord.Color.random())
        embed.set_footer(text="Not in my job description")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="I couldn't find this member",
                              description="How have you tried to add roles to someone not in the server??",
                              color=discord.Color.random())
        embed.set_footer(text="Common sense just ain't common anymore...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title="I didn't find this role.",
                              description=f"Apparently this role doesn't even EXIST in your server.\nTry making the role with {ctx.prefix}makerole first.",
                              color=discord.Color.random())
        embed.set_footer(text="That would be great")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title="I can't do that!",
                              description=f"{member.mention} you will have to place my role above that role.",
                              color=discord.Color.random())
        embed.set_footer(text="It is a necessity")
        await ctx.send(embed=embed)


    else:
        raise (error)


@editrole.error
async def edit_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="I didn't find this role.",
                              description=f"{member.mention} please mention the role to edit **AND** the new role.",
                              color=discord.Color.random())
        embed.set_footer(text="Imagine being able to write bot commands properly...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title="I didn't find this role.",
                              description=f"{member.mention} Mentioning a valid role couldn't HURT you know...",
                              color=discord.Color.random())
        embed.set_footer(text="The validity check never ends...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title="I can't do that!",
                              description=f"{member.mention} you will have to place my role above that role.",
                              color=discord.Color.random())
        embed.set_footer(text="It is a necessity")
        await ctx.send(embed=embed)

    else:
        raise (error)


@removerole.error
async def remove_role_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="I didn't find this role. (Again...)",
                              description=f"{member.mention} please mention the role to edit **AND** the new role. (Again)",
                              color=discord.Color.random())
        embed.set_footer(text="Imagine being able to write bot commands properly... (Again...)")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title="I didn't find this role.",
                              description=f"{member.mention}Mentioning a valid role couldn't HURT you know...\nBut its sad I gotta repeat stuff I said be4.\n Didn't you guys see this is in the mistake of role edits?",
                              color=discord.Color.random())
        embed.set_footer(text="Once again, the validity check never ends...")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="That username... is not in this server?",
                              description=f"{member.mention} I didn't find this so-called user name you mentioned.",
                              color=discord.Color.random())
        embed.set_footer(text="I can only remove the role of people who exist in the server.")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title="I do not have the permission!",
                              description=f"{member.mention} my place is currently BELOW that role.\nTry placing me above.",
                              color=discord.Color.random())
        embed.set_footer(text="It is a necessity")
        await ctx.send(embed=embed)

    else:
        raise (error)


@deleterole.error
async def delete_role_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Ok cool",
                              description=f"**Intense Concentration** There!\nI have deleted a non-existent role.",
                              color=discord.Color.random())
        embed.set_footer(text="No need to thank me...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title=f"Dear {member.mention}",
                              description=f"I assure you that I will do my best to delete a role that I couldn't find in this server.",
                              color=discord.Color.random())
        embed.set_footer(text="I exist to serve")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title="I do not have the permission!",
                              description=f"{member.mention} my place is currently BELOW that role.\nTry placing me above.",
                              color=discord.Color.random())
        embed.set_footer(text="It is a necessity")
        await ctx.send(embed=embed)


    else:
        raise (error)


@nick.error
async def nick_error(ctx, error):
    member = ctx.author
    from discord import errors
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"What are you playing at?",
                              description=f"Stop giving me half the info I need\nYou must tell me both, the User and his new nickname.",
                              color=discord.Color.random())
        embed.set_footer(text="Its not really that hard you know...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"People say they hate their job",
                              description=f"I say my jobs easy.\nChanging nicknames of non-existent users.",
                              color=discord.Color.random())
        embed.set_footer(text="Now all I need is payment...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Nope, the member is more powerful than me",
                              description=f"Maybe put my role above him :pleading_face:",
                              color=discord.Color.random())
        embed.set_footer(text="I feel weak")
        await ctx.send(embed=embed)

    else:
        raise (error)


@blacklist.error
async def blacklist_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"C'mon dude",
                              description=f"I don't really want to stop people from using me\nBut if you really want me too, then at least tell me who to stop?",
                              color=discord.Color.random())
        embed.set_footer(text="The least you can do")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.UserNotFound):
        embed = discord.Embed(title=f"Please stop making this hard for me...",
                              description=f"Just mention who I must stop.\nRandom names won't really do",
                              color=discord.Color.random())
        embed.set_footer(text="Is this necessary")
        await ctx.send(embed=embed)
    else:
        raise (error)


@unblacklist.error
async def unblacklist_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Are u serious?",
                              description=f"Reminding you the blacklisting thin air is NOT possible",
                              color=discord.Color.random())
        embed.set_footer(text="I mean, isn't it obvious?")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.UserNotFound):
        embed = discord.Embed(title=f"Stop memeing. Just stop.",
                              description=f"This user is not in this server.",
                              color=discord.Color.random())
        embed.set_footer(text="Have some mercy...")
        await ctx.send(embed=embed)
    else:
        raise (error)


@clear.error
async def clear_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"That's pretty vague",
                              description=f"You tell me to clear message but don't tell me how many.\nSo do I clear them all?",
                              color=discord.Color.random())
        embed.set_footer(text="Maybe NOT a good idea...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.BadArgument):
        embed = discord.Embed(title=f"Numbers. -_-",
                              description=f"I can only clear a number of messages. What else did you expect?",
                              color=discord.Color.random())
        embed.set_footer(text="You be being sus")
        await ctx.send(embed=embed)
    else:
        raise (error)


@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Alright I'll bite",
                              description=f"Who am I supposed to warn?",
                              color=discord.Color.random())
        embed.set_footer(text="Mentioning that wud be gr8")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"I couldn't find this user.",
                              description=f"So instead I warned my friend Louis here...",
                              color=discord.Color.random())
        embed.set_footer(text="Wait... what have you done to Louis?")
        await ctx.send(embed=embed)
    else:
        raise (error)


@userwarn.error
async def userwarn_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"I refuse",
                              description=f"I simply refuse to give you the warnings of *NOTHING*",
                              color=discord.Color.random())
        embed.set_footer(text="That would be a crime")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.UserNotFound):
        embed = discord.Embed(title=f"Ok no",
                              description=f"Reminding you that seeing the warnings of an invalid user is not allowed!",
                              color=discord.Color.random())
        embed.set_footer(text="Kids these days...")
        await ctx.send(embed=embed)
    else:
        raise (error)


@rps.error
async def rps_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Ok no",
                              description=f"Reminding you that playing rps with an imaginary user is not allowed.... Just play singleplayer mate",
                              color=discord.Color.random())
        embed.set_footer(text="Kids these days...")
        await ctx.send(embed=embed)
    else:
        raise (error)


@oddeve.error
async def oddeve_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Ok no",
                              description=f"Reminding you that playing with an imaginary user is not allowed.... Just play singleplayer mate",
                              color=discord.Color.random())

        embed.set_footer(text="Kids these days...")
        await ctx.send(embed=embed)



    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"No shit",
                              description=f"I take numbers only for your choice",
                              color=discord.Color.random())
        embed.set_footer(text="Kids these days...")
        await ctx.send(embed=embed)

    else:
        raise (error)


@lockdown.error
async def lockdown_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Ah sad",
                              description=f"U need to use either {ctx.prefix}lockdown true or {ctx.prefix}lockdown false",
                              color=discord.Color.random())
        embed.set_footer(text="That's how that works")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.error.CommandsInvokeError):
      embed = discord.Embed(title=f"I need more PERMS",
                              description=f"I need to be able to manage the server.\nNow use your comman sense and give me the perm necessary.",
                              color=discord.Color.random())
      embed.set_footer(text="Hopefully you have some")
      await ctx.send(embed=embed)

    else:
        raise (error)


@unmute.error
async def unmute_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Mention the user please",
                              description=f"I cannot unmute the void obviously",
                              color=discord.Color.random())
        embed.set_footer(text="Mentioning someone helps tho")
        await ctx.send(embed=embed)


    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"I really don't like this",
                              description=f"Pretty sure that Mr. Nothing couldn't talk in the first place.",
                              color=discord.Color.random())
        embed.set_footer(text="unmuting nothing is a horrific idea")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Nope, the member is more powerful than me",
                              description=f"Maybe put my role above him :pleading_face:",
                              color=discord.Color.random())
        embed.set_footer(text="I feel weak")
        await ctx.send(embed=embed)
    else:
        raise (error)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Mention the user please",
                              description=f"I cannot kick the void obviously",
                              color=discord.Color.random())
        embed.set_footer(text="Mentioning someone helps tho")
        await ctx.send(embed=embed)


    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"I really don't like this",
                              description=f"Pretty sure that this person didn't exist in the first place.",
                              color=discord.Color.random())
        embed.set_footer(text="Kicking the air... *shudder")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Nope, the member is more powerful than me",
                              description=f"Maybe put my role above him :pleading_face:",
                              color=discord.Color.random())
        embed.set_footer(text="I feel weak")
        await ctx.send(embed=embed)

    else:
        raise (error)


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Muting is not nice...",
                              description=f"But if you insist on it, mention *WHO* you want to mute.",
                              color=discord.Color.random())
        embed.set_footer(text="Because respect")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Muting random people is acceptable...",
                              description=f"...when the people actually exist",
                              color=discord.Color.random())
        embed.set_footer(text="So make sure they do")
        await ctx.send(embed=embed)

    else:
        raise (error)


@tempmute.error
async def tempmute_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Trying to tempmute no one",
                              description=f"Is not something people do\nYou seriously must mention who you wanna temp mute.",
                              color=discord.Color.random())
        embed.set_footer(text="This *no user mentioned* thing is getting old.")
        await ctx.send(embed=embed)


    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Did you just try to temp mute a user who isn't in this server.",
                              description=f"Tbh I deal with that non-sense so much I'm not even surprised.",
                              color=discord.Color.random())
        embed.set_footer(text="But seriously, stop")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Nope, the member is more powerful than me",

                              description=f"Maybe put my role above him :pleading_face:",

                              color=discord.Color.random())

        embed.set_footer(text="I feel weak")

        await ctx.send(embed=embed)


    else:
        raise (error)


@ban.error
async def ban_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"If only you were competent",
                              description=f"You would know the banning no one is a waste of time.",
                              color=discord.Color.random())
        embed.set_footer(text="Unpoggers indeed")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Banning is a sad thing",
                              description=f"It becomes 10 times worse when you can't even properly tell me who to ban!",
                              color=discord.Color.random())
        embed.set_footer(text="I may not have a life but still")
        await ctx.send(embed=embed)


    elif isinstance(error, commands.errors.CommandInvokeError):

        embed = discord.Embed(title=f"Nope, the member is more powerful than me",

                              description=f"Maybe put my role above him :pleading_face:",

                              color=discord.Color.random())

        embed.set_footer(text="I feel weak")

        await ctx.send(embed=embed)


    else:
        raise (error)


@tempban.error
async def tempban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Sure thing buddy",
                              description=f"Ima tempban my old buddy Louis. Oh wait...",
                              color=discord.Color.random())
        embed.set_footer(text="I think that's why I couldn't find him be4")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.UserNotFound):
        embed = discord.Embed(title=f"You failed at typing properly",
                              description=f"What else is new...",
                              color=discord.Color.random())
        embed.set_footer(text="I think the guy about to be banned is relieved")
        await ctx.send(embed=embed)


    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Nope, the member is more powerful than me",
                              description=f"Maybe put my role above him :pleading_face:",
                              color=discord.Color.random())
        embed.set_footer(text="I feel weak")
        await ctx.send(embed=embed)

    else:
        raise (error)


@unban.error
async def unban_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Unbanning is a sign of mercy",
                              description=f"But it would make you look better in front of your friends if you mention someone to ban.",
                              color=discord.Color.random())
        embed.set_footer(text="IOn the bright side, you can now unban someone")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.UserNotFound):
        embed = discord.Embed(title=f"Ahh the difficulty..",
                              description=f"It must be so hard for you to be able to mention a valid user.",
                              color=discord.Color.random())
        embed.set_footer(text="This is sarcasm")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Hold up!",
                              description=f"What do you think I am? The server owner?\nI can't do that, I don't got the permission!",
                              color=discord.Color.random())
        embed.set_footer(text="Stop trying to take my rights")
        await ctx.send(embed=embed)

    else:
        raise (error)


@dictionary.error
async def dict_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Alright.",
                              description=f"The definition of nothing is ___. It probably has synonyms and antonyms, but idrc.",
                              color=discord.Color.random())
        embed.set_footer(text="Im not stupid")
        await ctx.send(embed=embed)

    else:
        raise (error)


@translate.error
async def translate_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Why is this difficult",
                              description=f"All you gotta do, is use {ctx.prefix}help translate and do what it says.",
                              color=discord.Color.random())
        embed.set_footer(text="Why you being like this")
        await ctx.send(embed=embed)


    elif isinstance(error,commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Well that didn't work.....",
                              description=f"Probably u put in some invalid shit",
                              color=discord.Color.random())
        embed.set_footer(text="Failed! Just like your life")
        await ctx.send(embed=embed)


    else:
        raise (error)


@urban.error
async def urban_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"I can't believe it.",
                              description=f"This was the place where i really didn't expect an error. Use {ctx.prefix}Help urban for god's sake!",
                              color=discord.Color.random())
        embed.set_footer(text="Wish you could use more brain power for this")
        await ctx.send(embed=embed)

    else:
        raise (error)


@weather.error
async def weather_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Did you just try to find the weather of NOWHERE?!",
                              description=f"I don't even know what to say",
                              color=discord.Color.random())
        embed.set_footer(text="Actually I do. Try being smart.")
        await ctx.send(embed=embed)

    else:
        raise (error)


@wiki.error
async def wiki_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"It's good you search for knowledge",
                              description=f"But at least tell me what knowledge you want.\n There are a trillion+ websites of info out there.",
                              color=discord.Color.random())
        embed.set_footer(text="It's a huge world")
        await ctx.send(embed=embed)

    else:
        raise (error)


@ask.error
async def ask_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"What were you asking again?",
                              description=f"All I heard was ___",
                              color=discord.Color.random())
        embed.set_footer(text="Either I'm deaf, or you didn't even ask.")
        await ctx.send(embed=embed)

    else:
        raise (error)

@gif.error
async def gif_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"What were you searching gifs for again?",
                              description=f"All I heard was ___",
                              color=discord.Color.random())
        embed.set_footer(text="Either I'm deaf, or you didn't even type anything to search.")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Lmao sad life!",
                              description=f"Didn't find anything",

                              color=discord.Color.random())
        embed.set_footer(text=f"sad puppy")
        await ctx.send(embed=embed)


    else:
        raise (error)


@repeat.error
async def repeat_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Ik spamming is fun sometimes",
                              description=f"Spamming absolutely nothing, however, is not enjoyable.",
                              color=discord.Color.random())
        embed.set_footer(text="You'd just be staring at the screen then")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Ik spamming is fun sometimes",
                              description=f"But it would be really helpful if you give me number of times i have to spam?",

                              color=discord.Color.random())
        embed.set_footer(text=f"They expect me to repeat stuff without telling me how many times")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.0f}s.", color=discord.Color.random())
        em.set_footer(text="Bruh I know spam is fun but keep it a bit down")
        await ctx.send(embed=em)
    else:
        raise (error)


@epicgamerrate.error
async def gamerrate_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"I wish I knew how EPIC this user is.",
                              description=f"But sadly he doesn't exist.",
                              color=discord.Color.random())
        embed.set_footer(text="Ima go cry now")
        await ctx.send(embed=embed)

    else:
        raise (error)


@simprate.error
async def simprate_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Trying to see how much they simp eh?",
                              description=f"Oh wait. They don't exist!.\n So ima guess its 0",
                              color=discord.Color.random())
        embed.set_footer(text="Im smart BOI")
        await ctx.send(embed=embed)

    else:
        raise (error)


@poll.error
async def poll_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Ah I fell you",
                              description=f"This command is way too complex. Use {ctx.prefix}help poll",
                              color=discord.Color.random())
        embed.set_footer(text="The one command where mistakes be understandable")
        await ctx.send(embed=embed)

    else:
        raise (error)


@ascii.error
async def ascii_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Done!",
                              description=f"Successfully converted *nothing* into a beautiful picture!\nNow try actually giving me something for me to use",
                              color=discord.Color.random())
        embed.set_footer(text="smh smh SMH")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"BRUHH!",
                              description=f"That is too big to send!!",
                              color=discord.Color.random())
        embed.set_footer(text="That's what she said")
        await ctx.send(embed=embed)

    else:
        raise (error)


@act.error
async def act_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Bruh please give me all arguments for the command!",
                              description=f"It is... `{ctx.prefix}act @person_you_wanna_enact stuff_u_want_it_to_say`",
                              color=discord.Color.random())
        embed.set_footer(text="smh smh SMH")
        await ctx.send(embed=embed)


    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"BRUHH!",
                              description=f"Mention a human to act",
                              color=discord.Color.random())
        embed.set_footer(text="Who am i supposed to mimic... Joe Ma--")
        await ctx.send(embed=embed)

    else:
        raise (error)

@binary.error
async def binary_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Well you didn't input anything",
                              description=f"I'm assuming you want the binary code of a space key.\nIt's `00100000",
                              color=discord.Color.random())
        embed.set_footer(text="Tho you didn't want the binary of space did you?")
        await ctx.send(embed=embed)

    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        embed = discord.Embed(title="Chill out dude",
                              description="I can't send you something that long.\nTry putting a shorter message.",
                              color=discord.Color.random())
        embed.set_footer(text="That was going to be SO difficult to send")
        await ctx.send(embed=embed)
    else:
        raise (error)


@encrypt.error
async def encrypt_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Encrypted!",
                              description=f"`*Nothing*`",
                              color=discord.Color.random())
        embed.set_footer(text="lollers")
        await ctx.send(embed=embed)

    else:
        raise (error)


@decrypt.error
async def decrypt_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Decrypted!",
                              description=f"`*Nothing*`",
                              color=discord.Color.random())
        embed.set_footer(text="Even more lollers")
        await ctx.send(embed=embed)

    else:
        raise (error)


@choose.error
async def choose_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=f"Alright, if that's what you wish",
                                  description=f"I choose this particular non-existent thing over the other.",
                                  color=discord.Color.random())
            embed.set_footer(text="Don't really know what you will achieve with that knowledge")
            await ctx.send(embed=embed)

    else:
        raise (error)


@guess.error
async def guess_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Do you want to sit here FOREVER",
                              description=f"Seriously dude, I need both an upper and a lower limit.",
                              color=discord.Color.random())
        embed.set_footer(text="Imagine guessing a number in infinity")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Do you want to sit here FOREVER",
                              description=f"Seriously dude, I need it to be in numbers please.",
                              color=discord.Color.random())
        embed.set_footer(text="Imagine guessing a number in infinity")
        await ctx.send(embed=embed)


    else:
        raise (error)


@worthless.error
async def worthless_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Worthlessness has a limit",
                              description=f"`*Nothing*` can't be worthless",
                              color=discord.Color.random())
        embed.set_footer(text="This is philosophy")
        await ctx.send(embed=embed)

    else:
        raise (error)


@wanted.error
async def wanted_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=f"Do you hate your legal system?",
                                  description=f"Your trying to make the authorities do their best to try and catch *no one*",
                                  color=discord.Color.random())
            embed.set_footer(text="I wonder why...")
            await ctx.send(embed=embed)

    else:
        raise (error)


@rip.error
async def rip_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Imagine going to a grave yard...",
                              description=f"And finding gravestones where people have no names.",
                              color=discord.Color.random())
        embed.set_footer(text="Low budget cemetery")
        await ctx.send(embed=embed)

    else:
        raise (error)


@chad.error
async def chad_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Chad is great!",
                              description=f"I mean, I am Chad.\nBut Chad without a head... naaa",
                              color=discord.Color.random())
        embed.set_footer(text="Headless Chad WOULD be funny tho")
        await ctx.send(embed=embed)

    else:
        raise (error)


@quote.error
async def quote_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        abelin = "\n\"The Best way to predict your future is to create it.\" -Abraham Lincoln\n"
        suntzu = "\"The supreme art of war is to subdue the enemy without fighting.\" -Sun Tzu, The Art of War"
        embed = discord.Embed(title=f"Ahh, the quotes",
                              description=f"Some famous quotes are: {abelin} {suntzu}\nHowever, Nothing -No One, is not a good quote",
                              color=discord.Color.random())
        embed.set_footer(text="I mean, duh")
        await ctx.send(embed=embed)

    else:
        raise (error)


bot.remove_command('help')


@bot.command()
async def help(ctx, command=None):
    if command is None:
        page = 1
        pages = 5

        help_embed_1 = discord.Embed(title="Utilities")
        help_embed_1.add_field(name="Ping",
                               value=f"This allows you to check my ping.\n{ctx.prefix}help ping")
        help_embed_1.add_field(name="MakeRole",
                               value=f"Makes a new role in the server for you!\n{ctx.prefix}help makerole",
                               inline=False)
        help_embed_1.add_field(name="AddRole", value=f"Gives the user a role!\n{ctx.prefix}help addrole",
                               inline=False)
        help_embed_1.add_field(name="EditRole",
                               value=f"Edits an existing role in the server.\n{ctx.prefix}help editrole",
                               inline=False)
        help_embed_1.add_field(name="RemoveRole",
                               value=f"Takes away a user's role.\n{ctx.prefix}help removerole",
                               inline=False)
        help_embed_1.add_field(name="DeleteRole",
                               value=f"Deletes a role in the server.\n{ctx.prefix}help deleterole",
                               inline=False)
        help_embed_1.add_field(name="UserInfo",
                               value=f"Gives the  information of the member specified...\n{ctx.prefix}help userinfo",
                               inline=False)
        help_embed_1.add_field(name="Robmoji",
                               value=f"Robs an emoji! Basically takes an emoji from any server and uploads it here(in dis server) so everyone can use it!\n{ctx.prefix}help robmoji",
                               inline=False)

        help_embed_1.add_field(name="ServerInfo",
                               value=f"Provides the information about the server.\n{ctx.prefix}help serverinfo",
                               inline=False)
        help_embed_1.add_field(name="Nick",
                               value=f"Change nicknames in the server by using this feature.\n{ctx.prefix}help nick",
                               inline=False)
        help_embed_1.add_field(name="About",
                               value=f"Tells you something more about ME!\n{ctx.prefix}help about",
                               inline=False)
        help_embed_1.add_field(name="Snipe",
                               value=f"Allows You to restore the last deleted message of the channel.\n{ctx.prefix}help snipe",
                               inline=False)
        help_embed_1.add_field(name="Invite",
                               value=f"Gives you the link to invite me to your servers!\n{ctx.prefix}help invite",
                               inline=False)
        help_embed_1.add_field(name="Support",
                               value=f"Gives you my support server invite!\n{ctx.prefix}help support",
                               inline=False)
        help_embed_1.add_field(name="Website",
                               value=f"Takes you to my devs' website!\n{ctx.prefix}help website",
                               inline=False)
        help_embed_1.set_footer(text="Page 1")
        help_embed_1.color = discord.Color.random()

        help_embed_2 = discord.Embed(title="Moderation")          
        help_embed_2.add_field(name="Prefix",
                               value=f"Shows the prefix and allows you to change it!.\n{ctx.prefix}help prefix",
                               inline=False)
        help_embed_2.add_field(name="Slowmode",
                               value=f"Allows moderators to enable/disable slowmode.\n{ctx.prefix}help slowmode",
                               inline=False)
        help_embed_2.add_field(name="Blacklist", value=f"Blacklists a user.\n{ctx.prefix}help blacklist",
                               inline=False)
        help_embed_2.add_field(name="Unblacklist",
                               value=f"Unblacklists a user.\n{ctx.prefix}help unblacklist", inline=False)
        help_embed_2.add_field(name="Clear", value=f"Clears messages in a channel.\n{ctx.prefix}help clear",
                               inline=False)
        help_embed_2.add_field(name="Lockdown",
                               value=f"Enforces lockdown in the server.\n{ctx.prefix}help lockdown",
                               inline=False)
        help_embed_2.add_field(name="Warn", value=f"Gives a warning to a user.\n{ctx.prefix}help warn",
                               inline=False)
        help_embed_2.add_field(name="UserWarn",
                               value=f"Displays the history of warnings given to a user.\n{ctx.prefix}help userwarn",
                               inline=False)

        help_embed_2.add_field(name="Unmute",
                               value=f"Allows user from typing in the server.\n{ctx.prefix}help unmute",
                               inline=False)

                      
        help_embed_2.add_field(name="Tempmute",
                               value=f"Stop user from typing in the server TEMPORARILY.\n{ctx.prefix}help tempmute",
                               inline=False)
        help_embed_2.add_field(name="Mute",
                               value=f"Stop user from typing in the server.\n{ctx.prefix}help mute",
                               inline=False)
        help_embed_2.add_field(name="Kick", value=f"Kicks the specified user from the server.\n{ctx.prefix}help kick",
                               inline=False)
        help_embed_2.add_field(name="Unban", value=f"Unbans users, obviously.\n{ctx.prefix}help unban",
                               inline=False)
        help_embed_2.add_field(name="Tempban", value=f"Bans users, TEMPORARILY.\n{ctx.prefix}help tempban",
                               inline=False)
        help_embed_2.add_field(name="Ban", value=f"Bans users, like, DUH.\n{ctx.prefix}help ban",
                               inline=False)
        help_embed_2.set_footer(text="Page 2")
        help_embed_2.color = discord.Color.random()
        help_embed_3 = discord.Embed(title="Information")
        help_embed_3.add_field(name="Dictionary",
                               value=f"Finds dictionary meanings, synonyms and antonyms.\n{ctx.prefix}help dictionary",
                               inline=False)
        help_embed_3.add_field(name="Translate",
                               value=f"Translates a word into any language needed.\n{ctx.prefix}help translate",
                               inline=False)
        help_embed_3.add_field(name="Weather",
                               value=f"Gives you the current weather of a place.\n{ctx.prefix}help weather",
                               inline=False)
        help_embed_3.add_field(name="Wiki",
                               value=f"Searches up the Wikipedia for you.\n{ctx.prefix}help wiki",
                               inline=False)
        help_embed_3.add_field(name="UrbanDictionary",
                               value=f"Allows you to access the Urban Dictionary.\n{ctx.prefix}help urban",
                               inline=False)
        help_embed_3.set_footer(text="Page 3")
        help_embed_3.color = discord.Color.random()
        help_embed_4 = discord.Embed(title="Fun")
        help_embed_4.add_field(name="Ask",
                               value=f"Honestly answers a question you may have.\n{ctx.prefix}help ask",
                               inline=False)
        help_embed_4.add_field(name="Repeat", value=f"Repeats your message.\n{ctx.prefix}help repeat",
                               inline=False)
        help_embed_4.add_field(name="Dice", value=f"Roles a dice for you.\n{ctx.prefix}help dice",
                               inline=False)
        help_embed_4.add_field(name="EpicGamerRate",
                               value=f"Tells you how EPIC you are at gaming.\n{ctx.prefix}help epicgamerrate",
                               inline=False)
        help_embed_4.add_field(name="SimpRate",
                               value=f"Tells you how much you are simping.\n{ctx.prefix}help simprate",
                               inline=False)
        help_embed_4.add_field(name="Poll", value=f"Creates a poll for you.\n{ctx.prefix}help poll",
                               inline=False)
        help_embed_4.add_field(name="Script",
                               value=f"Translates the Zero&One script.\n{ctx.prefix}help script",
                               inline=False)

        help_embed_4.add_field(name="Binary",
                               value=f"Converts string to binary as zeros and ones are cool\n{ctx.prefix}help binary",
                               inline=False)
        help_embed_4.add_field(name="ASCII",
                               value=f"Creates a cool ASCII art for you.\n{ctx.prefix}help ascii",
                               inline=False)
        help_embed_4.add_field(name="Act",
                               value=f"Makes me act as though I'm another user...\n{ctx.prefix}help act",
                               inline=False)
        help_embed_4.add_field(name="Chooser",
                               value=f"Lets you choose between the given options.\n{ctx.prefix}help chooser",
                               inline=False)
        help_embed_4.add_field(name="Coinflip", value=f"Flips a coin for you.\n{ctx.prefix}help coinflip",
                               inline=False)
        help_embed_4.add_field(name="Hack", value=f"Hacks the required user.\n{ctx.prefix}help hack",
                               inline=False)
        help_embed_4.add_field(name="Gif",
                               value=f"Allows to search for GIFs or send random.\n{ctx.prefix}help gif",
                               inline=False)

        help_embed_4.add_field(name="ImageMemes",
                               value=f"Makes some very funny image memes for you.\n{ctx.prefix}help imagememes",
                               inline=False)
        help_embed_4.add_field(name="VCMeme",
                               value=f"Let's you have some fun with the people in your VC.\n{ctx.prefix}help vcmeme",
                               inline=False)
        help_embed_4.add_field(name="Quote",
                               value=f"Allows you to quote the sayings of your fellow human beings.\n{ctx.prefix}help quote",
                               inline=False)
        help_embed_4.set_footer(text="Page 4")
        help_embed_4.color = discord.Color.random()

        help_embed_5 = discord.Embed(title="Games")
        help_embed_5.add_field(name="Guess",
                               value=f"Lets you guess a number within any range.\n{ctx.prefix}help guess",
                               inline=False)
        help_embed_5.add_field(name="Rps",
                               value=f"Lets you play rock paper scissor with me **OR** your friends{ctx.prefix}\n{ctx.prefix}help rps",
                               inline=False)
        help_embed_5.add_field(name="OddEve",
                               value=f"Lets you play odd eve with me **OR** your friends{ctx.prefix}\n(cricket version coming out soon)\n{ctx.prefix}help oddeve",
                               inline=False)
        help_embed_5.add_field(name="More games coming soon!", value=f"You better believe it!")
        help_embed_5.set_footer(text="Page 5")
        help_embed_5.color = discord.Color.random()

        message = await ctx.send(embed=help_embed_1)

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        while True:
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=300, check=check)

                if str(reaction.emoji) == "▶️":
                    page += 1
                    if page == pages + 1:
                        page = 1
                    try:
                        await message.remove_reaction(reaction, user)
                    except:
                        print("Could not remove reaction in help")
                elif str(reaction.emoji) == "◀️":
                    page -= 1
                    if page == 0:
                        page = pages
                    try:
                        await message.remove_reaction(reaction, user)
                    except:
                        print("Could not remove reaction in help")

                else:
                    try:
                        await message.remove_reaction(reaction, user)
                    except:
                        print("Could not remove reaction in help")

                if page == 1:
                    try:
                        await message.edit(embed=help_embed_1)
                    except:
                        print("Could not edit")
                elif page == 2:
                    try:
                        await message.edit(embed=help_embed_2)
                    except:
                        print("Could not edit")
                elif page == 3:
                    try:
                        await message.edit(embed=help_embed_3)
                    except:
                        print("Could not edit")
                elif page == 4:
                    try:
                        await message.edit(embed=help_embed_4)
                    except:
                        print("Could not edit")
                elif page == 5:
                    try:
                        await message.edit(embed=help_embed_5)
                    except:
                        print("Could not edit")

            except asyncio.TimeoutError:
                print("Timed out oops")


    elif command.lower() == 'ping':
        embed = discord.Embed(title="Help Ping",
                              description="With this command, you can see how fast I am reacting to your messages in milliseconds.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:", value=f"{ctx.prefix}ping")
        embed.set_footer(text="I do be very fast u know...")
        await ctx.send(embed=embed)

    elif command.lower() == 'makerole':
        embed = discord.Embed(title="Help MakeRole",
                              description="At last, with just one command, you can make a new role in your server.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}makerole <rolename>\nCause you have the right to be LAZY")
        embed.set_footer(
            text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS")
        await ctx.send(embed=embed)

    elif command.lower() == 'addrole':
        embed = discord.Embed(title="Help AddRole",
                              description="You can also add roles to your members by just using this one command!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}addrole @<membername> @<rolename>\nSo now you can be LAZIER!")
        embed.set_footer(
            text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS")
        await ctx.send(embed=embed)


    elif command.lower() == 'editrole':
        embed = discord.Embed(title="Help EditRole",
                              description="Don't like the name of your role?\n Then just use this command to change its name!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}editrole @<fromrolename> <torolename>\nCause why not?")
        embed.set_footer(
            text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS")
        await ctx.send(embed=embed)


    elif command.lower() == 'removerole':
        embed = discord.Embed(title="Help RemoveRole",
                              description="If your members misuse their roles then there is only one solution:\n Take the role away from them!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}removerole @<membername> @<rolename>\nBasically making you a dictator...")
        embed.set_footer(
            text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS")
        await ctx.send(embed=embed)


    elif command.lower() == 'deleterole':
        embed = discord.Embed(title="Help DeleteRole",
                              description="You can also delete roles in your server when the role just becomes useless.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}deleterole @<rolename>\nImagine needing to delete roles ANYWAY...")
        embed.set_footer(
            text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS")
        await ctx.send(embed=embed)


    elif command.lower() == 'support':
        embed = discord.Embed(title="Help Support",
                              description="Need help with the my commands?\nWanna complain about them?\nMaybe make a suggestion?",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:", value=f"{ctx.prefix}support\nSo you can visit our support server.")
        embed.set_footer(text="Get support its good for you")
        await ctx.send(embed=embed)

    elif command.lower() == 'userinfo':
        embed = discord.Embed(title="Help UserInfo",
                              description="Find out about the wierdos who join your servers.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:", value=f"{ctx.prefix}userinfo @<membername>\n#gettingexposed")
        embed.set_footer(text="Being a stalker eh?")
        await ctx.send(embed=embed)

    elif command.lower() == 'robmoji':
        embed = discord.Embed(title="Help RobMoji",
                              description="Steal an emoji from another server and make it yours. If a name is not given, it will take the emoji's name. Also pls make sure that you give a name from 2 to 32.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:", value=f"{ctx.prefix}robmoji emoji name_of_new_emoji\n#MINE!")
        embed.set_footer(text="Should I call the cops?")
        await ctx.send(embed=embed)

    elif command.lower() == 'serverinfo':
        embed = discord.Embed(title="Help ServerInfo",
                              description="For everything you need to know about your server.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}serverinfo\nNever forget your memories, or your server info.")
        embed.set_footer(text="But seriously, how did you forget?")
        await ctx.send(embed=embed)


    elif command.lower() == 'nick':
        embed = discord.Embed(title="Help Nick",
                              description="Nickname your friends anything you want!\nIt is WAY too easy to do so, with this command.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}nick @<membername> <nickname>\nNow see what you can come up with...")
        embed.set_footer(text="Nasty surprise for the poor victim's names *sigh*")
        await ctx.send(embed=embed)


    elif command.lower() == 'about':
        embed = discord.Embed(title="Help About",
                              description="Get to know a little bit more about me!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}about\nPlease use this :pleading_face:\nMy devs think NO ONE wants to know more about me...")
        embed.set_footer(text="I mean, why not?")
        await ctx.send(embed=embed)


    elif command.lower() == 'snipe':
        embed = discord.Embed(title="Help Snipe",
                              description="Find out what the last deleted message in your server was.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}snipe\nNow you can catch your sneaky server members in the act!")
        embed.set_footer(text="More stonx for u")
        await ctx.send(embed=embed)


    elif command.lower() == 'invite':
        embed = discord.Embed(title="Help Invtie",
                              description="Use this to invite me to your other servers.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}about\nPlease use this :pleading_face:\nYou. Can't. Get. Enough. Of. Me.")
        embed.set_footer(text="I'm the BEST")
        await ctx.send(embed=embed)


    elif command.lower() == 'website':
        embed = discord.Embed(title="Help Website",
                              description="My developers have a website. Go check it out.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}about\nPlease use this :pleading_face:\nIt's not really related to me, but its cool anyway.")
        embed.set_footer(text="See you there!")
        await ctx.send(embed=embed)


    elif command.lower() == 'slowmode':
        embed = discord.Embed(title="Help Slowmode",
                              description="Allows you to put or remove a slowmode in your channel.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}slowmode <timeinseconds>\nThat will stop the SPAMMERS")
        embed.set_footer(text="Sad life for spammers.")
        await ctx.send(embed=embed)


    elif command.lower() == 'blacklist':
        embed = discord.Embed(title="Help Blacklist",
                              description="This makes users unable to use my commands.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}blacklist @<membername>\nThis is one of the most CRUELLEST punishments possible.")
        embed.set_footer(text="Not using CHAD be SAD")
        await ctx.send(embed=embed)


    elif command.lower() == 'unblacklist':
        embed = discord.Embed(title="Help Unblacklist",
                              description="Removes blacklisted users from the list of naughty people...",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}unblacklist @<membername>\nOnly kindness can make you use this command.")
        embed.set_footer(text="Unblacklisters = Saviours")
        await ctx.send(embed=embed)


    elif command.lower() == 'clear':
        embed = discord.Embed(title="Help Clear",
                              description="Clears the required number of messages in a channel.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}clear\nHelps when your server members just don't want to stop chatting...")
        embed.set_footer(text="Get ERASED")
        await ctx.send(embed=embed)


    elif command.lower() == 'lockdown':
        embed = discord.Embed(title="Help Lockdown",
                              description="Basically stops EVERYONE from using the channel.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:", value=f"{ctx.prefix}lockdown <trueorfalse>\nFor total Monarchy servers.")
        embed.set_footer(text="Imagine needing lockdown in discord...")
        await ctx.send(embed=embed)


    elif command.lower() == 'warn':
        embed = discord.Embed(title="Help Warn",
                              description="Gives the rule-breakers a warning!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}warn <username> <reason>\nOnly for those naughty users who don't like rules.")
        embed.set_footer(text="So you've been warned...")
        await ctx.send(embed=embed)

    elif command.lower() == 'prefix':
        embed = discord.Embed(title="Help Prefix",
                              description="Change dat prefix",
                              colour=discord.Color.random(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}prefix <newprefix>\nVery handy for big servers!")
        embed.set_footer(text="Just don't forget what your prefix was...")
        await ctx.send(embed=embed)


    elif command.lower() == 'userwarn':
        embed = discord.Embed(title="Help UserWarn",
                              description="Gives a record of why and how many times a user was warned in the server.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}userwarn @<username>\nNow you have a record of their crimes.")
        embed.set_footer(text="*Evil laughter from admins*")
        await ctx.send(embed=embed)


    elif command.lower() == 'unmute':
        embed = discord.Embed(title="Help Unmute",
                              description="Allows you to unmute a user.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}unmute @<username>\nThis makes the able to talk in your server again.")
        embed.set_footer(text="Support Freedom of Speech")
        await ctx.send(embed=embed)


    elif command.lower() == 'tempmute':
        embed = discord.Embed(title="Help Tempmute",
                              description="Allows you to temporarily mute a user.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}tempmute <timeinseconds>s @<username>\nIf you think you may forget to unmute a user, then I do it for you!")
        embed.set_footer(text="That's one less thing to remember...")
        await ctx.send(embed=embed)


    elif command.lower() == 'mute':
        embed = discord.Embed(title="Help Mute",
                              description="Allows you to mute a user.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}mute @<username>\nNow they can't talk until you allow them too!")
        embed.set_footer(text="Sad life for the muted")
        await ctx.send(embed=embed)


    elif command.lower() == 'kick':
        embed = discord.Embed(title="Help Kick",
                              description="Allows you to kick a user.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}kick @<username>\nSo basically they just get yeeted out.")
        embed.set_footer(text="Get rekt lol")
        await ctx.send(embed=embed)


    elif command.lower() == 'unban':
        embed = discord.Embed(title="Help Unban",
                              description="Allows you to unban a user.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}unban @<username>\nSo that they can return to the server.")
        embed.set_footer(text="Oh look, they're back lol")
        await ctx.send(embed=embed)


    elif command.lower() == 'tempban':
        embed = discord.Embed(title="Help Tempban",
                              description="Allows you to temporarily ban a user.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}tempban <timeinseconds>s @<username>\nIf you really hate someone, and may \"accidentally\" forget to unban them...")
        embed.set_footer(text="That's just sus uk")
        await ctx.send(embed=embed)


    elif command.lower() == 'ban':
        embed = discord.Embed(title="Help Ban",
                              description="Allows you to ban a user.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}mute @<username>\nThey can NEVER COME BACK NOW MWA HA HA HA\nJeez I was only joking")
        embed.set_footer(text="Get banished lmao")
        await ctx.send(embed=embed)


    elif command.lower() == 'dictionary':
        embed = discord.Embed(title="Help Dictionary",
                              description="Lets you access a dictionary through discord!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}dictionary <word>\nWhat you can do is get meanings, synonyms and antonyms!\nThen you type either meanings, synonyms or antonyms.")
        embed.set_footer(text="All for geeky lil nerds!")
        await ctx.send(embed=embed)


    elif command.lower() == 'translate':
        embed = discord.Embed(title="Help Translate",
                              description="Translate a word to any language you want.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}translate <wordtotranslate>\nAnd then you enter the language translate to.")
        embed.set_footer(text="Merci!")
        await ctx.send(embed=embed)


    elif command.lower() == 'weather':
        embed = discord.Embed(title="Help Weather",
                              description="Get the real-time weather of any place!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}search <cityname>\nAny city can be searched for!")
        embed.set_footer(text="Try searching \"Israel\" lol")
        await ctx.send(embed=embed)


    elif command.lower() == 'wiki':
        embed = discord.Embed(title="Help Wiki",
                              description="Search Wikipedia.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}wiki <whatyouwannasearch>\nCause clearly, google wasn't enough.")
        embed.set_footer(text="Wisdom is in DISCORD PPL")
        await ctx.send(embed=embed)


    elif command.lower() == 'urban':
        embed = discord.Embed(title="Help UrbanDictionary",
                              description="Let's you use the Urban Dictionary (like, obviously).",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}urban <whatyouwannasearch>\nAn interesting place of knowledge.")
        embed.set_footer(text="The urban dict be lollers (I mean try searching your own name)")
        await ctx.send(embed=embed)


    elif command.lower() == 'ask':
        embed = discord.Embed(title="Help Ask",
                              description="Answer you question for you.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}ask <question>\nIts prophetic power is to be respected.")
        embed.set_footer(text="The Bot don't lie...")
        await ctx.send(embed=embed)


    elif command.lower() == 'repeat':
        embed = discord.Embed(title="Help Repeat",
                              description="Makes me spam for you..",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}repeat <numberoftimes> <messagetorepeat>\nWhy do I have to do the dirty work?")
        embed.set_footer(text="Just don't get blacklisted lol")
        await ctx.send(embed=embed)


    elif command.lower() == 'dice':
        embed = discord.Embed(title="Help Dice",
                              description="Makes me **role**(pun intended) a dice for you.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:", value=f"{ctx.prefix}dice\nYou get a random number for 1 to 6! Yay!")
        embed.set_footer(text="Ok this is starting to get ridiculously lazy")
        await ctx.send(embed=embed)


    elif command.lower() == 'epicgamerrate':
        embed = discord.Embed(title="Help epicgamerrate",
                              description="Now you can find out how epic you are at gaming.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:", value=f"{ctx.prefix}epicgamerrate\nThis is totally true btw")
        embed.set_footer(text="It's a perfect way of knowing how good you are!")
        await ctx.send(embed=embed)


    elif command.lower() == 'simprate':
        embed = discord.Embed(title="Help simprate",
                              description="Now you can find out how much you simp.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:", value=f"{ctx.prefix}simprate\nThis is totally true btw")
        embed.set_footer(text="It's a perfect way of knowing how simpy you are!")
        await ctx.send(embed=embed)


    elif command.lower() == 'poll':
        embed = discord.Embed(title="Help Poll",
                              description="Create a poll to get some votes",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}poll <timeinseconds> <whatyoupollfor>: <optionswithcommas>\nEveryone can just choose what they wanna choose.")
        embed.set_footer(text="I don't think there is any other way to poll on discord...")
        await ctx.send(embed=embed)


    elif command.lower() == 'script':
        embed = discord.Embed(title="Help Script",
                              description="Translates the ZeroAndOne Script",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}encrypt <stufftoencrypt>\n!decrypt <stufftodecrypt>\nCheck out the way this script works [here](https://secret-message-encoder-decoder.itszeroandone.repl.co/).")
        embed.set_footer(text="You'll love the script.")
        await ctx.send(embed=embed)


    elif command.lower() == 'ascii':
        embed = discord.Embed(title="Help ASCII",
                              description="Turns me into a painter and makes ASCII art.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}ascii <stufftoput>\nI can't really explain it's beauty.")
        embed.set_footer(text="What you put may or may not be what you get")
        await ctx.send(embed=embed)

    
    elif command.lower() == 'act':
        embed = discord.Embed(title="Help Act",
                              description="Use this to make me act like another user!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}act @<usertoactlike> <messagetouse>\nMostly used for fake evidence :smiling_imp:")
        embed.set_footer(text="This is for pure evil purposes")
        await ctx.send(embed=embed)

    elif command.lower() == 'binary':
        embed = discord.Embed(title="Help binary",
                              description="converts string to binary",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}binary <yourstring>")
        embed.set_footer(text="Zeros and Ones are cool")
        await ctx.send(embed=embed)

    elif command.lower() == 'choose' or command.lower() == 'chooser':
        embed = discord.Embed(title="Help Choose",
                              description="Makes a choice for you.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}choose <choices>\nAgain, this bot knows everything.\nIt makes the correct choice.")
        embed.set_footer(text="The bot KNOWS")
        await ctx.send(embed=embed)


    elif command.lower() == 'coinflip':
        embed = discord.Embed(title="Help Coinflip",
                              description="Flips a coin. Seriously why do you even need help in that?",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}coinflip <heads/tails>\nYou choose correct, you win.")
        embed.set_footer(text="So pretty obvious how you lose")
        await ctx.send(embed=embed)

    elif command.lower() == 'hack':
        embed = discord.Embed(title="Help Hack",
                              description="Totally hacks the targeted user pc.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}hack @<membername>\nA lot of bad stuff happens.\nUse only in cases of extreme hate or prejudice.")
        embed.set_footer(text="The bad stuff be bad")
        await ctx.send(embed=embed)

    
    elif command.lower() == 'gif':
        embed = discord.Embed(title="Help Gif",
                              description="Allows you to search giphy for GIFS",
                              colour=discord.Color.random(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}gif <nameofgif>\nGifs are cool yay")
        embed.set_footer(text="Who needs inbuilt GIFs smh")
        await ctx.send(embed=embed)


    elif command.lower() == 'imagememes':
        embed = discord.Embed(title="Help ImageMemes",
                              description="Cool memes with images!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}imagememes \nGives you a list of image memes. Enjoy!")
        embed.set_footer(text="Cause there can NEVER be enough memes")
        await ctx.send(embed=embed)


    elif command.lower() == 'vcmeme':
        embed = discord.Embed(title="Help VCMeme",
                              description="Prank your friends in your VC.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}vcmeme <chosenvcmeme>\nThe list is long...\nTo check the list, type {ctx.prefix}vcmeme")
        embed.set_footer(text="I feel sorry for VC users...")
        await ctx.send(embed=embed)


    elif command.lower() == 'quote':
        embed = discord.Embed(title="Help Quote",
                              description="Creates a quote so you can remember your most famous sayings!",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:", value=f"{ctx.prefix}quote <quoter> <quote>\nIt gives you glory.")
        embed.set_footer(text="Always remember...")
        await ctx.send(embed=embed)

    elif command.lower() == 'guess':
        embed = discord.Embed(title="Help Guess",
                              description="Let's you play guess the number between literally any two numbers.",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Usage:",
                        value=f"{ctx.prefix}guess <lowerboundary> <upperboundary>\nThen you just guess ig...")
        embed.set_footer(text="Bet you can't beat my dev Zero in 1 - 10000")
        await ctx.send(embed=embed)

    elif command.lower() == 'rps':
        embed = discord.Embed(title="Help RPS",
                              description="You can either play:",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Single player:", value=f"Use {ctx.prefix}rps <rock/paper/scissor> to play against me, or")
        embed.add_field(name="Multi player:", value=f"Use {ctx.prefix}rps <useryouwanttodefeat> to play against them.")
        embed.set_footer(text="Its a great game!")
        await ctx.send(embed=embed)

    elif command.lower() == 'oddeve':
        embed = discord.Embed(title="Help OddEve",
                              description="You can either play:",
                              colour=discord.colour.Colour.green(),
                              inline=True)
        embed.add_field(name="Single player:", value=f"Use {ctx.prefix}oddeve <odd/even> to play against me, or")
        embed.add_field(name="Multi player:", value=f"Use {ctx.prefix}oddeve <useryouwanttodefeat> to play against them.")
        embed.set_footer(text="Its a great game!")
        await ctx.send(embed=embed)

# Starts the bot


keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
