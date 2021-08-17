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
import discord
from discord.ext import commands, tasks
import random
import os
import requests
import re
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math
from io import BytesIO
from tinydb import TinyDB, Query
from keep_alive import keep_alive
from discord.ext.commands import MissingPermissions
from pprint import pprint
import typing
from discord.ext.commands import cooldown, BucketType

intents = discord.Intents().all()


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
startup_extensions = ['fun', 'errors', 'games', 'help', 'info', 'moderation', 'settings', 'utils','events']

for extension in startup_extensions:
    try:
        bot.load_extension(f"cogs.{extension}")
    except Exception as e:
        exec = "{} : {}".format(extension, e)
        print(exec)

#bot.load_extension("cogs.errors")

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
                embed=discord.Embed(title=f"{member.name} is currently afk",
                                    description=f"Afk note is: {value}",
                                    color=discord.Color.random()))

    member = message.author
    if db2.search(query['afk_user'] == member.id):
        await message.channel.send(embed=discord.Embed(
            title=f"{member.name} You typed a message!",
            description=f"That means you ain't afk!\nWelcome back buddy.",
            color=discord.Color.random()))

        query = Query()
        db2.remove(query.afk_user == member.id)
    await bot.process_commands(message=message)

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
                raise commands.BadArgument(
                    "{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


def checkping(guild_id_var):
    db = TinyDB('databases/pings.json')
    query = Query()
    values = str(list(map(lambda entry: entry["pingstate"],
                          db.search(query.guild_id == str(guild_id_var))))[0])

    return values.lower()


@bot.command()
async def load(ctx, *, module):
    """Loads a module."""
    if ctx.author.id == 815555652780294175 or ctx.author.id == 815555652780294175:
        try:
            bot.load_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    else:
        await ctx.send("Who do you think you are huh?\n Definately not the owner")


@bot.command()
async def unload(ctx, *, module):
    """Unloads a module."""
    if ctx.author.id == 815555652780294175 or ctx.author.id == 815555652780294175:
        try:
            bot.unload_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    else:
        await ctx.send("Who do you think you are huh?\n Definately not the owner")


@bot.command()
async def reload(ctx, *, module):
    if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
        try:
            bot.reload_extension(f"cogs.{module}")
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    else:
        await ctx.send("Who do you think you are huh?\n Definately not the owner")


    


keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
# Starts the bot
bot.run(token)
