from giphy_client.rest import ApiException
import giphy_client
import aiohttp
import sys
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
from discord_components import *
import asyncio
import time
import discord
import urbandict
from discord.utils import get
from discord.ext import commands, tasks
import random
import os
import requests
import re
import datetime
from PIL import Image, ImageFont, ImageDraw
import math
from io import BytesIO
from tinydb import TinyDB, Query
from discord.ext.commands import MissingPermissions
from pprint import pprint
import typing
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv
import topgg


load_dotenv()
intents = discord.Intents.default()
intents.members = True

async def determine_prefix(bot, message):
    if message.guild:
        db = TinyDB('databases/prefix.json')
        if message is not None:
            guild_id = message.guild.id
        query = Query()
        if db.search(query['guild_id'] == str(guild_id)):
            values = list(map(lambda entry: entry["prefix"], db.search(
                query.guild_id == str(guild_id))))
            return values
        return '!'

    else:
        return '!'


bot = commands.Bot(command_prefix=determine_prefix, intents=intents)
bot.remove_command('help')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")

        except commands.ExtensionError as e:
            print(f'{e.__class__.__name__}: {e}')
            
bot.load_extension("uptime")
dbl_token = os.getenv(dbl_token)
bot.topggpy = topgg.DBLClient(bot, dbl_token, autopost=True)

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

    db2 = TinyDB('databases/afk.json')
    query = Query()

    for member in message.mentions:
        if db2.search(query['afk_user'] == member.id):
            value = str(
                list(
                    map(lambda entry: entry["reason"],
                        db2.search(query['afk_user'] == member.id)))[0])
            await message.channel.send(
                embed=discord.Embed(title=f"{member.display_name} is currently afk",
                                    description=f"Afk note is: {value}",
                                    color=discord.Color.random()))

    member = message.author
    if db2.search(query['afk_user'] == member.id):
        await message.channel.send(embed=discord.Embed(
            title=f"{member.display_name} You typed a message!",
            description=f"That means you ain't afk!\nWelcome back buddy.",
            color=discord.Color.random()))

        query = Query()
        db2.remove(query.afk_user == member.id)
    await bot.process_commands(message=message)


@bot.command()
async def load(ctx, *, module):
    """loads a module."""
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        if ctx.author.id == 815555652780294175:
            author = "Mr One"

        elif ctx.author.id == 723032217504186389:
            author = "Mr Zero"

        try:
            bot.load_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(embed=discord.Embed(title="Oof Buddy, there is an error <a:zo_cri:886222278331867187>", description=f'{e.__class__.__name__}: {e}', color=discord.Color.random()))
        else:
            embed1 = discord.Embed(title=f"Alright {author}. Loaded {module}.py with no errors",
                                   description=f"<a:zo_thumbs_up:886219697694081045>", color=discord.Color.random())
            await ctx.send(embed=embed1)

    else:
        await ctx.send(embed=discord.Embed(title="Nope you imposter", description="I dont take orders from peasants like you <a:ZOWumpusTongue:865559251764903946>", color=discord.Color.random()))


@bot.command()
async def unload(ctx, *, module):
    """Unloads a module."""
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        if ctx.author.id == 815555652780294175:
            author = "Mr One"

        elif ctx.author.id == 723032217504186389:
            author = "Mr Zero"

        try:
            bot.unload_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(embed=discord.Embed(title="Oof Buddy, there is an error <a:zo_cri:886222278331867187>", description=f'{e.__class__.__name__}: {e}', color=discord.Color.random()))
        else:
            embed1 = discord.Embed(title=f"Alright {author}. Unloaded {module}.py with no errors",
                                   description=f"<a:zo_thumbs_up:886219697694081045>", color=discord.Color.random())
            await ctx.send(embed=embed1)

    else:
        await ctx.send(embed=discord.Embed(title="Nope you imposter", description="I dont take orders from peasants like you <a:ZOWumpusTongue:865559251764903946>", color=discord.Color.random()))


@bot.command()
async def reload(ctx, *, module):
    """reloads a module."""
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        if ctx.author.id == 815555652780294175:
            author = "Mr One"

        elif ctx.author.id == 723032217504186389:
            author = "Mr Zero"

        try:
            bot.reload_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(embed=discord.Embed(title="Oof Buddy, there is an error<a:zo_cri:886222278331867187>", description=f'{e.__class__.__name__}: {e}', color=discord.Color.random()))
        else:
            embed1 = discord.Embed(title=f"Alright {author}. Reloaded {module}.py with no errors",
                                   description=f"<a:zo_thumbs_up:886219697694081045>", color=discord.Color.random())
            await ctx.send(embed=embed1)

    else:
        await ctx.send(embed=discord.Embed(title="Nope you imposter", description="I dont take orders from peasants like you <a:ZOWumpusTongue:865559251764903946>", color=discord.Color.random()))


@bot.command(aliases=["reloadall", "reloadcogs"])
async def massreload(ctx):
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        if ctx.author.id == 815555652780294175:
            author = "Mr One"

        elif ctx.author.id == 723032217504186389:
            author = "Mr Zero"

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.send(f"Reloading {filename[:-3]}")
                await asyncio.sleep(1)
                try:
                    bot.reload_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(f"Done Reloading {filename[:-3]}, now moving on to the next one")

                except commands.ExtensionError as e:
                    await ctx.send(embed=discord.Embed(title="Oof Buddy, there is an error <a:zo_cri:886222278331867187>", description=f'{e.__class__.__name__}: {e}', color=discord.Color.random()))
            
    else:
        await ctx.send(embed=discord.Embed(title="Nope you imposter", description="I dont take orders from peasants like you <a:ZOWumpusTongue:865559251764903946>", color=discord.Color.random()))

@bot.command(aliases=["unloadall", "unloadcogs"])
async def massunload(ctx):
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        if ctx.author.id == 815555652780294175:
            author = "Mr One"

        elif ctx.author.id == 723032217504186389:
            author = "Mr Zero"
            
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'): 
                await ctx.send(f"Unloading {filename[:-3]}")
                await asyncio.sleep(1)
                try:
                    bot.unload_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(f"Done Unloading {filename[:-3]}, now moving on to the next one")

                except commands.ExtensionError as e:
                    await ctx.send(embed=discord.Embed(title="Oof Buddy, there is an error<a:zo_cri:886222278331867187>", description=f'{e.__class__.__name__}: {e}', color=discord.Color.random()))

@bot.command(aliases=["loadall", "loadcogs"])
async def massload(ctx):
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        if ctx.author.id == 815555652780294175:
            author = "Mr One"

        elif ctx.author.id == 723032217504186389:
            author = "Mr Zero"
            
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.send(f"Loading {filename[:-3]}")
                await asyncio.sleep(1)
                try:
                    bot.load_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(f"Done Loading {filename[:-3]}, now moving on to the next one")

                except commands.ExtensionError as e:
                    await ctx.send(embed=discord.Embed(title="Oof Buddy, there is an error <a:zo_cri:886222278331867187>", description=f'{e.__class__.__name__}: {e}', color=discord.Color.random()))


    else:
        await ctx.send(embed=discord.Embed(title="Nope you imposter", description="I dont take orders from peasants like you <a:ZOWumpusTongue:865559251764903946>", color=discord.Color.random()))

    
@bot.command(aliases=["checkcogs"])
async def checkcog(ctx):
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        if ctx.author.id == 815555652780294175:
            author = "Mr One"

        elif ctx.author.id == 723032217504186389:
            author = "Mr Zero"
        
        all_cogs=[]
        loaded_cogs=[]
        for filename in os.listdir('./cogs'):

            if filename.endswith('.py'):
                print(filename[:-3])
                all_cogs.append(filename[:-3])
                
        await ctx.send(f"Hey {author} All cogs are [{', '.join(all_cogs)}]")

        for i in all_cogs:
            try:
                bot.load_extension(f"cogs.{i}")
                await ctx.send(f"{i} wasn't loaded")
                await asyncio.sleep(1)
                bot.unload_extension(f"cogs.{i}")
            except commands.ExtensionAlreadyLoaded:
                loaded_cogs.append(i)

        await ctx.send(f"Hey {author} All loaded cogs are [{', '.join(loaded_cogs)}]")
    else:
        await ctx.send(embed=discord.Embed(title="Nope you imposter", description="I dont take orders from peasants like you <a:ZOWumpusTongue:865559251764903946>", color=discord.Color.random()))



@bot.event
async def on_autopost_success():
    print(f"Posted server count ({bot.topggpy.guild_count}))")
      
token = os.getenv("DISCORD_BOT_SECRET")
bot.run(token)
