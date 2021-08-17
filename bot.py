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
mod = bot.get_cog('Moderation')
fun = bot.get_cog('Fun')
info = bot.get_cog('Info')
settings = bot.get_cog('Settings')
games = bot.get_cog('Games')
Help = bot.get_cog('Help')
utils = bot.get_cog('Utils')  

slowmode = mod.slowmode
@slowmode.error
async def slowmode_error(self,ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):

        if ctx.channel.slowmode_delay == 0:
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


hack = fun.hack


@hack.error
async def hack_error(self,ctx,error):
    member = ctx.author

    if checkping(ctx.message.guild.id) == 'true':
        membervar = member.mention

    else:
        membervar = member.display_name

    if isinstance(error, commands.MissingRequiredArgument):

        await ctx.send(embed=discord.Embed(title="Your kidding right?",
                                        description=f"{membervar} please mention a user to hack\n That way, I won't need to hack thin air!!",
                                        color=discord.Color.random()))

    elif isinstance(error, commands.UserNotFound):
        await ctx.send(embed=discord.Embed(title="This is ridiculous",
                                        description=f"<:ZO_Bruh:866252668225585152> {membervar} have the brain cells to mention the target smh.\n How are you unable to MENTION SOMEONE"))

    else:
        raise (error)


robmoji = utils.robmoji


@robmoji.error
async def rob_moji_error(self,ctx,error):
    member = ctx.author
    if checkping(ctx.message.guild.id) == 'true':
        membervar = member.mention

    else:
        membervar = member.display_name
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title="You're kidding right?",
                                        description=f"{membervar} please mention an emojito steal\n That way, I won't need to steal thin air!!",
                                        color=discord.Color.random()))

    elif isinstance(error, commands.errors.PartialEmojiConversionFailure):
        error = getattr(error, "original", error)
        the_error_arg = error.argument
        embed = discord.Embed(title="Whoops",
                            description=f"Could not convert {the_error_arg} to an emoji",
                            color=discord.Color.random())
        embed.set_footer(
            text="If this is not you being dumb and a genuine error in the code,let us know here (https://discord.gg/TeRyp9JWbg)")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send(embed=discord.Embed(title="You're kidding right?",
                                        description=f"{membervar} give it a name from 2 to 32 characters **ONLY**\nAnd NO SPACES PLS \n this is an emoji name not a train",
                                        color=discord.Color.random()))

    else:
        raise (error)


userinfo = utils.userinfo


@userinfo.error
async def userinfo_error(self,ctx,error):
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


makerole = utils.makerole


@makerole.error
async def make_role_error(self,ctx,error):
    member = ctx.author

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Hmmmm...",
                            description="Why haven't you mentioned the NAME OF THE ROLE YOU WANT TO CREATE\nA role with the name ___ is pretty stupid.",
                            color=discord.Color.random())
        embed.set_footer(text="Think about it")
        await ctx.send(embed=embed)

    else:
        raise (error)


addrole = utils.addrole


@addrole.error
async def add_role_error(self,ctx,error):
    member = ctx.author
    if checkping(ctx.message.guild.id) == 'true':
        membervar = member.mention

    else:
        membervar = member.display_name

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
                            description=f"{membervar} you will have to place my role above that role.",
                            color=discord.Color.random())
        embed.set_footer(text="It is a necessity")
        await ctx.send(embed=embed)

    else:
        raise (error)


editrole = utils.editrole


@editrole.error
async def edit_error(self,ctx,error):
    member = ctx.author
    if checkping(ctx.message.guild.id) == 'true':
        membervar = member.mention

    else:
        membervar = member.display_name

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="I didn't find this role.",
                            description=f"{membervar} please mention the role to edit **AND** the new role.",
                            color=discord.Color.random())
        embed.set_footer(
            text="Imagine being able to write bot commands properly...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title="I didn't find this role.",
                            description=f"{membervar} Mentioning a valid role couldn't HURT you know...",
                            color=discord.Color.random())
        embed.set_footer(text="The validity check never ends...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title="I can't do that!",
                            description=f"{membervar} you will have to place my role above that role.",
                            color=discord.Color.random())
        embed.set_footer(text="It is a necessity")
        await ctx.send(embed=embed)

    else:
        raise (error)


removerole = utils.removerole


@removerole.error
async def remove_role_error(self,ctx,error):
    member = ctx.author
    if checkping(ctx.message.guild.id) == 'true':
        membervar = member.mention

    else:
        membervar = member.display_name

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="I didn't find this role. (Again...)",
                            description=f"{membervar} please mention the role to edit **AND** the new role. (Again)",
                            color=discord.Color.random())
        embed.set_footer(
            text="Imagine being able to write bot commands properly... (Again...)")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title="I didn't find this role.",
                            description=f"{membervar}Mentioning a valid role couldn't HURT you know...\nBut its sad I gotta repeat stuff I said be4.\n Didn't you guys see this is in the mistake of role edits?",
                            color=discord.Color.random())
        embed.set_footer(text="Once again, the validity check never ends...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="That username... is not in this server?",
                            description=f"{membervar} I didn't find this so-called user name you mentioned.",
                            color=discord.Color.random())
        embed.set_footer(
            text="I can only remove the role of people who exist in the server.")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title="I do not have the permission!",
                            description=f"{membervar} my place is currently BELOW that role.\nTry placing me above.",
                            color=discord.Color.random())
        embed.set_footer(text="It is a necessity")
        await ctx.send(embed=embed)

    else:
        raise (error)


deleterole = utils.deleterole


@deleterole.error
async def delete_role_error(self,ctx,error):
    member = ctx.author
    if checkping(ctx.message.guild.id) == 'true':
        membervar = member.mention

    else:
        membervar = member.display_name

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Ok cool",
                            description=f"**Intense Concentration** There!\nI have deleted a non-existent role.",
                            color=discord.Color.random())
        embed.set_footer(text="No need to thank me...")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title=f"Dear {membervar}",
                            description=f"I assure you that I will do my best to delete a role that I couldn't find in this server.",
                            color=discord.Color.random())
        embed.set_footer(text="I exist to serve")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title="I do not have the permission!",
                            description=f"{membervar} my place is currently BELOW that role.\nTry placing me above.",
                            color=discord.Color.random())
        embed.set_footer(text="It is a necessity")
        await ctx.send(embed=embed)

    else:
        raise (error)


nick = utils.nick


@nick.error
async def nick_error(self,ctx,error):
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


reminder = utils.reminder


@reminder.error
async def rem_error(self,ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title=f"{ctx.author.display_name} please give me time and the reminder",
                                        color=discord.Color.random()))

    elif isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send(embed=discord.Embed(title=f"{ctx.author.display_name} That is an invalid time",
                                        color=discord.Color.random()))

    else:
        raise (error)


blacklist = mod.blacklist


@blacklist.error
async def blacklist_error(self,ctx,error):
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

unblacklist = mod.unblacklist


@unblacklist.error
async def unblacklist_error(self,ctx,error):
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

clear = mod.clear


@clear.error
async def clear_error(self,ctx,error):
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

warn = mod.warn


@warn.error
async def warn_error(self,ctx,error):
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

userwarn = mod.userwarn


@userwarn.error
async def userwarn_error(self,ctx,error):
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

rps = games.rps


@rps.error
async def rps_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Ok no",
                            description=f"Reminding you that playing rps with an imaginary user is not allowed.... Just play singleplayer mate",
                            color=discord.Color.random())
        embed.set_footer(text="Kids these days...")
        await ctx.send(embed=embed)

    else:
        raise (error)

oddeve = games.oddeve


@oddeve.error
async def oddeve_error(self,ctx,error):
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

lockdown = mod.lockdown


@lockdown.error
async def lockdown_error(self,ctx,error):
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

unmute = mod.unmute


@unmute.error
async def unmute_error(self,ctx,error):
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

kick = mod.kick


@kick.error
async def kick_error(self,ctx,error):
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

mute = mod.mute


@mute.error
async def mute_error(self,ctx,error):
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

tempmute = mod.tempmute


@tempmute.error
async def tempmute_error(self,ctx,error):
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

ban = mod.ban


@ban.error
async def ban_error(self,ctx,error):
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

tempban = mod.tempban


@tempban.error
async def tempban_error(self,ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Sure thing buddy",
                            description=f"Ima tempban my old buddy Louis. Oh wait...",
                            color=discord.Color.random())
        embed.set_footer(text="I think that's why I couldn't find him be4")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
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

unban = mod.unban


@unban.error
async def unban_error(self,ctx,error):
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

dictionary = info.dictionary


@dictionary.error
async def dict_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Alright.",
                            description=f"The definition of nothing is ___. It probably has synonyms and antonyms, but idrc.",
                            color=discord.Color.random())
        embed.set_footer(text="Im not stupid")
        await ctx.send(embed=embed)

    else:
        raise (error)

translate = info.translate


@translate.error
async def translate_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Why is this difficult",
                            description=f"All you gotta do, is use {ctx.prefix}help translate and do what it says.",
                            color=discord.Color.random())
        embed.set_footer(text="Why you being like this")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Well that didn't work.....",
                            description=f"Probably u put in some invalid shit",
                            color=discord.Color.random())
        embed.set_footer(text="Failed! Just like your life")
        await ctx.send(embed=embed)

    else:
        raise (error)

urban = info.urban


@urban.error
async def urban_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"I can't believe it.",
                            description=f"This was the place where i really didn't expect an error. Use {ctx.prefix}Help urban for god's sake!",
                            color=discord.Color.random())
        embed.set_footer(text="Wish you could use more brain power for this")
        await ctx.send(embed=embed)

    else:
        raise (error)

weather = info.weather


@weather.error
async def weather_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Did you just try to find the weather of NOWHERE?!",
                            description=f"I don't even know what to say",
                            color=discord.Color.random())
        embed.set_footer(text="Actually I do. Try being smart.")
        await ctx.send(embed=embed)

    else:
        raise (error)

wiki = info.wiki


@wiki.error
async def wiki_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"It's good you search for knowledge",
                            description=f"But at least tell me what knowledge you want.\n There are a trillion+ websites of info out there.",
                            color=discord.Color.random())
        embed.set_footer(text="It's a huge world")
        await ctx.send(embed=embed)

    else:
        raise (error)

ask = fun.ask


@ask.error
async def ask_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"What were you asking again?",
                            description=f"All I heard was ___",
                            color=discord.Color.random())
        embed.set_footer(text="Either I'm deaf, or you didn't even ask.")
        await ctx.send(embed=embed)

    else:
        raise (error)

gif = fun.gif


@gif.error
async def gif_error(self,ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"What were you searching gifs for again?",
                            description=f"All I heard was ___",
                            color=discord.Color.random())
        embed.set_footer(
            text="Either I'm deaf, or you didn't even type anything to search.")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.errors.CommandInvokeError):
        embed = discord.Embed(title=f"Lmao sad life!",
                            description=f"Didn't find anything",

                            color=discord.Color.random())
        embed.set_footer(text=f"sad puppy")
        await ctx.send(embed=embed)

    else:
        raise (error)

repeat = fun.repeat


@repeat.error
async def repeat_error(self,ctx,error):
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
        embed.set_footer(
            text=f"They expect me to repeat stuff without telling me how many times")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow it down bro!", description=f"Try again in {error.retry_after:.0f}s.",
                        color=discord.Color.random())
        em.set_footer(text="Bruh I know spam is fun but keep it a bit down")
        await ctx.send(embed=em)
    else:
        raise (error)

epicgamerrate = fun.epicgamerrate


@epicgamerrate.error
async def gamerrate_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"I wish I knew how EPIC this user is.",
                            description=f"But sadly he doesn't exist.",
                            color=discord.Color.random())
        embed.set_footer(text="Ima go cry now")
        await ctx.send(embed=embed)

    else:
        raise (error)

simprate = fun.simprate


@simprate.error
async def simprate_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Trying to see how much they simp eh?",
                            description=f"Oh wait. They don't exist!.\n So ima guess its 0",
                            color=discord.Color.random())
        embed.set_footer(text="Im smart BOI")
        await ctx.send(embed=embed)

    else:
        raise (error)

poll = fun.poll


@poll.error
async def poll_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Ah I fell you",
                            description=f"This command is way too complex. Use {ctx.prefix}help poll",
                            color=discord.Color.random())
        embed.set_footer(
            text="The one command where mistakes be understandable")
        await ctx.send(embed=embed)

    else:
        raise (error)

ascii = fun.ascii


@ascii.error
async def ascii_error(self,ctx,error):
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

act = fun.act


@act.error
async def act_error(self,ctx,error):
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

binary = fun.binary


@binary.error
async def binary_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Well you didn't input anything",
                            description=f"I'm assuming you want the binary code of a space key.\nIt's `00100000",
                            color=discord.Color.random())
        embed.set_footer(
            text="Tho you didn't want the binary of space did you?")
        await ctx.send(embed=embed)

    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        embed = discord.Embed(title="Chill out dude",
                            description="I can't send you something that long.\nTry putting a shorter message.",
                            color=discord.Color.random())
        embed.set_footer(text="That was going to be SO difficult to send")
        await ctx.send(embed=embed)
    else:
        raise (error)

encrypt = fun.encrypt


@encrypt.error
async def encrypt_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Encrypted!",
                            description=f"`*Nothing*`",
                            color=discord.Color.random())
        embed.set_footer(text="lollers")
        await ctx.send(embed=embed)

    else:
        raise (error)

decrypt = fun.decrypt


@decrypt.error
async def decrypt_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Decrypted!",
                            description=f"`*Nothing*`",
                            color=discord.Color.random())
        embed.set_footer(text="Even more lollers")
        await ctx.send(embed=embed)

    else:
        raise (error)

choode = fun.choose

choose = fun.choose
@choose.error
async def choose_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=f"Alright, if that's what you wish",
                                description=f"I choose this particular non-existent thing over the other.",
                                color=discord.Color.random())
            embed.set_footer(
                text="Don't really know what you will achieve with that knowledge")
            await ctx.send(embed=embed)

    else:
        raise (error)

guess = games.guess


@guess.error
async def guess_error(self,ctx,error):
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

worthless = fun.worthless


@worthless.error
async def worthless_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Worthlessness has a limit",
                            description=f"`*Nothing*` can't be worthless",
                            color=discord.Color.random())
        embed.set_footer(text="This is philosophy")
        await ctx.send(embed=embed)

    else:
        raise (error)

wanted = fun.wanted


@wanted.error
async def wanted_error(self,ctx,error):
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

rip = fun.rip


@rip.error
async def rip_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Imagine going to a grave yard...",
                            description=f"And finding gravestones where people have no names.",
                            color=discord.Color.random())
        embed.set_footer(text="Low budget cemetery")
        await ctx.send(embed=embed)

    else:
        raise (error)

chad = fun.chad


@chad.error
async def chad_error(self,ctx,error):
    member = ctx.author
    if isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"Chad is great!",
                            description=f"I mean, I am Chad.\nBut Chad without a head... naaa",
                            color=discord.Color.random())
        embed.set_footer(text="Headless Chad WOULD be funny tho")
        await ctx.send(embed=embed)

    else:
        raise (error)

quote = fun.quote
@quote.error
async def quote_error(self,ctx,error):
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

    


keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
# Starts the bot
bot.run(token)
