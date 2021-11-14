import nextcord
import asyncio
from nextcord.ext import commands
import random
from tinydb import TinyDB, Query
import re
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import typing

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


async def convert(argument):
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


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="slowmode", description="Allows you to put or remove a slowmode in your channel.",
                       options=[
                           create_option(name="duration",
                                         description="The time you want the slowmode to be (e.g: 2h or 5m)",
                                         option_type=3,
                                         required=False)])
    async def _slowmode(self, ctx: SlashContext, duration='0s'):
        try:
            if duration.isdigit():
                duration = int(duration)
            else:
                duration = await convert(duration)
        except:
            await ctx.send(embed=nextcord.Embed(title="Please give a proper duration", color=nextcord.Color.random()))
            return

        if ctx.author.guild_permissions.administrator:
            if duration == 0:
                await ctx.channel.edit(slowmode_delay=duration)
                embed = nextcord.Embed(
                    title="Slowmode Disabled!",
                    description=f"Y'all can talk your heart out now.",
                    color=nextcord.Color.random()
                )
            elif duration <= 21600:
                await ctx.channel.edit(slowmode_delay=duration)
                embed = nextcord.Embed(
                    title="Slowmode Enabled!",
                    description=f"There is a {int(duration)} seconds slowmode on this channel now.",
                    color=nextcord.Color.random()
                )
            else:
                embed = nextcord.Embed(title="Did you know?",
                                       description=f"Discord allows slowmodes up to 21600 seconds on its channels, which is equal to 360m, which is 6h!",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Point being, you can't set a slowmode above that")
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Administrators permission.",
                                     color=nextcord.Color.red()))

    @commands.command(aliases=['slomo', 'slowmo', 'sm', 'slo', 'smode'])
    async def slowmode(self, ctx, duration='0s'):
        try:
            if duration.isdigit():
                duration = int(duration)
            else:
                duration = await convert(duration)
        except:
            await ctx.send(embed=nextcord.Embed(title="Please give a proper duration", color=nextcord.Color.random()))
            return

        if ctx.author.guild_permissions.administrator:
            if duration == 0:
                await ctx.channel.edit(slowmode_delay=duration)
                embed = nextcord.Embed(
                    title="Slowmode Disabled!",
                    description=f"Y'all can talk your heart out now.",
                    color=nextcord.Color.random()
                )
            elif duration <= 21600:
                await ctx.channel.edit(slowmode_delay=duration)
                embed = nextcord.Embed(
                    title="Slowmode Enabled!",
                    description=f"There is a {int(duration)} seconds slowmode on this channel now.",
                    color=nextcord.Color.random()
                )
            else:
                embed = nextcord.Embed(title="Did you know?",
                                       description=f"Discord allows slowmodes up to 21600 seconds on its channels, which is equal to 360m, which is 6h!",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Point being, you can't set a slowmode above that")
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Administrators permission.",
                                     color=nextcord.Color.red()))

    @cog_ext.cog_slash(name="blacklist", description="Blacklists a user.",
                       options=[
                           create_option(name="member",
                                         description="The member you want to blacklist",
                                         option_type=6,
                                         required=True)])
    async def _blacklist(self, ctx: SlashContext, member: nextcord.Member):
        db = TinyDB('databases/blacklist.json')
        guild_id_var = ctx.guild.id
        if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
            db.insert({'guild_id': guild_id_var, 'blacklisted': str(member.id)})
            await ctx.send(embed=nextcord.Embed(title=f"I'm Sorry, but my boss wants you blacklisted"))
            return

        elif ctx.author.guild_permissions.administrator:
            if not member:
                await ctx.send(embed=nextcord.Embed(title="Please provide a member to blacklist smh"))
                return

            if member == ctx.author:
                embed = nextcord.Embed(title="Bruh why are you trying to blacklist yourself.",
                                       description="I refuse to let your stupidity get the better of you.",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Users these days...")
                await ctx.send(embed=embed)
                return

            elif member.id == 815555652780294175 or member.id == 723032217504186389:
                await ctx.send(
                    embed=nextcord.Embed(title="Buddy you can't blacklist the boss <a:ZO_BlobCool:866263738545078302>"))
                return

            elif member.guild_permissions.administrator:
                await ctx.send(
                    embed=nextcord.Embed(title="Halt! (lmao)",
                                         description="You cannot just go ahead and stop your fellow admins from using me!",
                                         color=nextcord.Color.red()))
                return

            elif {"guild_id": guild_id_var, "blacklisted": str(member.id)} in db.all():
                await ctx.send(embed=nextcord.Embed(title=f"{member.display_name} is already blacklisted...",
                                                    description="Jeez why do you hate him so much",
                                                    color=nextcord.Color.teal()))
                return

            else:
                db.insert({'guild_id': guild_id_var, 'blacklisted': str(member.id)})
                await ctx.send(embed=nextcord.Embed(title=f"{member.display_name} is blacklisted",
                                                    description="He can no longer use me :cry:",
                                                    color=nextcord.Color.teal()))
                return

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the administrator permission.",
                                     color=nextcord.Color.red()))

    @commands.command(aliases=['blist', 'blackl', 'bl'])
    async def blacklist(self, ctx, member: nextcord.Member):
        db = TinyDB('databases/blacklist.json')
        guild_id_var = ctx.guild.id
        if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
            db.insert({'guild_id': guild_id_var, 'blacklisted': str(member.id)})
            await ctx.send(embed=nextcord.Embed(title=f"I'm Sorry, but my boss wants you blacklisted"))
            return

        elif ctx.author.guild_permissions.administrator:
            if not member:
                await ctx.send(embed=nextcord.Embed(title="Please provide a member to blacklist smh"))
                return

            if member == ctx.author:
                embed = nextcord.Embed(title="Bruh why are you trying to blacklist yourself.",
                                       description="I refuse to let your stupidity get the better of you.",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Users these days...")
                await ctx.send(embed=embed)
                return

            elif member.id == 815555652780294175 or member.id == 723032217504186389:
                await ctx.send(
                    embed=nextcord.Embed(title="Buddy you can't blacklist the boss <a:ZO_BlobCool:866263738545078302>"))
                return

            elif member.guild_permissions.administrator:
                await ctx.send(
                    embed=nextcord.Embed(title="Halt! (lmao)",
                                         description="You cannot just go ahead and stop your fellow admins from using me!",
                                         color=nextcord.Color.red()))
                return

            elif {"guild_id": guild_id_var, "blacklisted": str(member.id)} in db.all():
                await ctx.send(embed=nextcord.Embed(title=f"{member.display_name} is already blacklisted...",
                                                    description="Jeez why do you hate him so much",
                                                    color=nextcord.Color.teal()))
                return

            else:
                db.insert({'guild_id': guild_id_var, 'blacklisted': str(member.id)})
                await ctx.send(embed=nextcord.Embed(title=f"{member.display_name} is blacklisted",
                                                    description="He can no longer use me :cry:",
                                                    color=nextcord.Color.teal()))
                return

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the administrator permission.",
                                     color=nextcord.Color.red()))

    @cog_ext.cog_slash(name="unblacklist", description="Unblacklists a user.",
                       options=[
                           create_option(name="member",
                                         description="The member you want to unblacklist",
                                         option_type=6,
                                         required=True)])
    async def _unblacklist(self, ctx: SlashContext, member: nextcord.Member):
        db = TinyDB('databases/blacklist.json')
        if ctx.author.guild_permissions.administrator or ctx.author.id == 815555652780294175 or \
                ctx.author.id == 723032217504186389:
            if not member:
                embed = nextcord.Embed(title="Please provide-", description="a member to unblacklist!",
                                       color=nextcord.Color.random())
                embed.set_footer(text="I mean, seriously... isn't this obvious?")
                await ctx.send(embed=embed)
                return
            query = Query()
            try:
                db.remove(query.blacklisted == str(member.id))
                if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
                    await ctx.send(embed=nextcord.Embed(title=f"{member.display_name} is unblacklisted",
                                                        description="My boss asked me to do so... :joy:",
                                                        color=nextcord.Color.random()))

                else:
                    await ctx.send(embed=nextcord.Embed(title=f"{member.display_name} is unblacklisted",
                                                        description="He can now use me! :joy:",
                                                        color=nextcord.Color.random()))
            except:
                await ctx.send(embed=nextcord.Embed(title="Nope!",
                                                    description=f"{member.display_name} is not blacklisted in this server."))
        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the administrator permission.",
                                     color=nextcord.Color.red()))

    @commands.command(aliases=['unbl', 'ubl', 'unblackl', 'unblist', 'ublackl', 'ublist'])
    async def unblacklist(self, ctx, member: nextcord.Member):
        db = TinyDB('databases/blacklist.json')
        if ctx.author.guild_permissions.administrator or ctx.author.id == 815555652780294175 or \
                ctx.author.id == 723032217504186389:
            if not member:
                embed = nextcord.Embed(title="Please provide-", description="a member to unblacklist!",
                                       color=nextcord.Color.random())
                embed.set_footer(text="I mean, seriously... isn't this obvious?")
                await ctx.send(embed=embed)
                return
            query = Query()
            try:
                db.remove(query.blacklisted == str(member.id))
                if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
                    await ctx.send(embed=nextcord.Embed(title=f"{member.display_name} is unblacklisted",
                                                        description="My boss asked me to do so... :joy:",
                                                        color=nextcord.Color.random()))

                else:
                    await ctx.send(embed=nextcord.Embed(title=f"{member.display_name} is unblacklisted",
                                                        description="He can now use me! :joy:",
                                                        color=nextcord.Color.random()))
            except:
                await ctx.send(embed=nextcord.Embed(title="Nope!",
                                                    description=f"{member.display_name} is not blacklisted in this server."))
        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the administrator permission.",
                                     color=nextcord.Color.red()))

    @cog_ext.cog_slash(name="clear", description="Clears messages in a channel.",
                       options=[
                           create_option(name="number",
                                         description="The number of messages you want to clear",
                                         option_type=4,
                                         required=True),
                           create_option(name="member",
                                         description="The member whose messages you want to clear",
                                         option_type=6,
                                         required=False)])
    async def _clear(self, ctx: SlashContext, number: int, member: nextcord.Member = None):
        if ctx.author.guild_permissions.manage_messages:
            if member is None:
                await ctx.channel.purge(limit=number)
                embed_message = await ctx.send(
                    embed=nextcord.Embed(title=f"{number} messages deleted", color=nextcord.Color.random()))
                await embed_message.delete(delay=3)

            else:
                await ctx.channel.purge(limit=number, check=lambda message: message.author == member)
                embed = nextcord.Embed(title=f"Done clearing the {number} messages of the specified user",
                                       description=f"I hope you're proud, it was a lot of work.",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Imagine being an ungrateful swine")
                await ctx.send(embed=embed, delete_after=5)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Manage Messages permission.",
                                     color=nextcord.Color.green()))

    @commands.command(aliases=['cl', 'purge', 'delete'])
    async def clear(self, ctx, times: int, member: nextcord.Member = None):
        if ctx.author.guild_permissions.manage_messages:
            if member is None:
                await ctx.channel.purge(limit=times)
                embed_message = await ctx.send(
                    embed=nextcord.Embed(title=f"{times} messages deleted", color=nextcord.Color.random()))
                await embed_message.delete(delay=3)

            else:
                await ctx.channel.purge(limit=times, check=lambda message: message.author == member)
                embed = nextcord.Embed(title=f"Done clearing the {times} messages of the specified user",
                                       description=f"I hope you're proud, it was a lot of work.",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Imagine being an ungrateful swine")
                await ctx.send(embed=embed, delete_after=5)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Manage Messages permission.",
                                     color=nextcord.Color.green()))

    @cog_ext.cog_slash(name="warn", description="Gives a warning to a user.",
                       options=[
                           create_option(name="member",
                                         description="The member who you want to warn",
                                         option_type=6,
                                         required=True),
                           create_option(name="reason",
                                         description="The reason for the warn",
                                         option_type=3,
                                         required=False)])
    async def _warn(self, ctx: SlashContext, member: nextcord.Member, *, reason: str):
        db = TinyDB('databases/warnings.json')
        guild_id_var = ctx.guild.id
        if ctx.author != member:
            if ctx.author.guild_permissions.administrator:
                if member.guild_permissions.administrator:
                    await ctx.send(embed=nextcord.Embed(title="ALERT! ALERT! :dizzy_face:",
                                                        description="Warning fellow admins is a no-no, kids!",
                                                        color=nextcord.Color.random()))
                    return
                elif not reason:
                    await ctx.send(embed=nextcord.Embed(title="Please provide a reason",
                                                        color=nextcord.Color.random()))
                    return

                elif len(reason) > 150:
                    await ctx.send(
                        embed=nextcord.Embed(title=f"The reason for warning cannot be more then 150 characters long!",
                                             description=f"You are {len(reason) - 150} characters over the limit!",
                                             color=nextcord.Color.random()))
                    return
                else:
                    await ctx.send(
                        embed=nextcord.Embed(title=f"{member.display_name} has been warned", description=reason,
                                             color=nextcord.Color.random()))
                    db.insert({'guild_id': guild_id_var, 'member': str(member), 'reason': reason})

            else:
                await ctx.send(
                    embed=nextcord.Embed(title="Stop right there!",
                                         description="You require the administrator permission.",
                                         color=nextcord.Color.red()))
        else:
            await ctx.send(embed=nextcord.Embed(title="Stop trying to warn yourself.",
                                                description="IT. IS. A. BAD. THING.",
                                                color=nextcord.Color.random()))

    @commands.command()
    async def warn(self, ctx, member: nextcord.Member, *, reason: str):
        db = TinyDB('databases/warnings.json')
        guild_id_var = ctx.guild.id
        if ctx.author != member:
            if ctx.author.guild_permissions.administrator:
                if member.guild_permissions.administrator:
                    await ctx.send(embed=nextcord.Embed(title="ALERT! ALERT! :dizzy_face:",
                                                        description="Warning fellow admins is a no-no, kids!",
                                                        color=nextcord.Color.random()))
                    return
                elif not reason:
                    await ctx.send(embed=nextcord.Embed(title="Please provide a reason",
                                                        color=nextcord.Color.random()))
                    return

                elif len(reason) > 150:
                    await ctx.send(
                        embed=nextcord.Embed(title=f"The reason for warning cannot be more then 150 characters long!",
                                             description=f"You are {len(reason) - 150} characters over the limit!",
                                             color=nextcord.Color.random()))
                    return
                else:
                    await ctx.send(
                        embed=nextcord.Embed(title=f"{member.display_name} has been warned", description=reason,
                                             color=nextcord.Color.random()))
                    db.insert({'guild_id': guild_id_var, 'member': str(member), 'reason': reason})

            else:
                await ctx.send(
                    embed=nextcord.Embed(title="Stop right there!",
                                         description="You require the administrator permission.",
                                         color=nextcord.Color.red()))
        else:
            await ctx.send(embed=nextcord.Embed(title="Stop trying to warn yourself.",
                                                description="IT. IS. A. BAD. THING.",
                                                color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="userwarn", description="Displays the history of warnings given to a user.",
                       options=[
                           create_option(name="member",
                                         description="The member whose criminal record you want to access",
                                         option_type=6,
                                         required=True)])
    async def _userwarn(self, ctx: SlashContext, member: nextcord.Member):
        db = TinyDB('databases/warnings.json')
        guild_id_var = ctx.guild.id
        query = Query()
        a = db.search((query['guild_id'] == guild_id_var) & (query['member'] == str(member)))
        embed = nextcord.Embed(title=f"Here are the warnings for {member.display_name}:", description="Warnings",
                               color=0xa6ff00)
        if len(a) == 0:
            embed = nextcord.Embed(title="This user has a MIND BLOWING number of warnings!!",
                                   description="0, to be exact",
                                   color=nextcord.Color.green())
            embed.set_footer(text="Clean record for now, eh?")
        else:
            i = 0
            for a in a:
                i += 1
                b = a.get('reason')
                embed.add_field(name=f"{i}. ", value=b, inline=False)
            embed.set_footer(text="Someone's been a naughty boi. Unless you're a girl.")

        await ctx.send(embed=embed)

    @commands.command(aliases=['warnings', 'warning', 'userw', 'uwarn', 'uw'])
    async def userwarn(self, ctx, member: nextcord.Member):
        db = TinyDB('databases/warnings.json')
        guild_id_var = ctx.guild.id
        query = Query()
        a = db.search((query['guild_id'] == guild_id_var) & (query['member'] == str(member)))
        embed = nextcord.Embed(title=f"Here are the warnings for {member.display_name}:", description="Warnings")
        if len(a) == 0:
            embed = nextcord.Embed(title="This user has a MIND BLOWING number of warnings!!",
                                   description="0, to be exact",
                                   color=0xa6ff00)
            embed.set_footer(text="Clean record for now, eh?")
        else:
            i = 0
            for a in a:
                i += 1
                b = a.get('reason')
                embed.add_field(name=f"{i}. ", value=b, inline=False)
            embed.set_footer(text="Someone's been a naughty boi. Unless you're a girl.")

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="lockdown", description="Enforces lockdown in the server.",
                       options=[
                           create_option(name="state",
                                         description="True if you want lockdown, False if you don't",
                                         option_type=3,
                                         choices=[create_choice(name="True", value="true"),
                                                  create_choice(name="False", value="false")],
                                         required=True)])
    async def _lockdown(self, ctx: SlashContext, state):
        db = TinyDB('databases/lockdown.json')
        query = Query()
        if ctx.author.guild_permissions.administrator:
            guild = ctx.guild
            everyone = nextcord.utils.get(guild.roles)
            unaffected_channels = []
            if state.lower() == 'true':
                if db.search(query.guild == ctx.guild.id)[0]['state'] is False:
                    embed = nextcord.Embed(
                        title="Turned on lockdown. No one gets in or out <a:ZOWumpusTongue:865559251764903946>",
                        color=nextcord.Color.red())
                    embed.set_footer(text="Corona is ONLINE")
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
                    await ctx.send(embed=nextcord.Embed(title="This channel is ALREADY under lockdown",
                                                        description="You can be arrested by law if you place a lockdown TWICE.",
                                                        color=nextcord.Color.random()))

            elif state.lower() == 'false':
                if db.search(query.guild == ctx.guild.id)[0]['state'] is True:
                    unaffected_channels = db.search(query.guild == ctx.guild.id)[0]['unaffected_channels']
                    for channel in guild.text_channels:
                        if channel.id in unaffected_channels:
                            pass
                        else:
                            await channel.set_permissions(everyone, send_messages=None)
                    for channel in guild.voice_channels:
                        if channel.id in unaffected_channels:
                            pass
                        else:
                            await channel.set_permissions(everyone, speak=None)
                    db.update({'state': False}, query.guild == ctx.guild.id)
                    embed = nextcord.Embed(
                        title="Lockdown has been lifted.... Enjoy Suckas <a:ZOPepeRave:865560322966421514>",
                        color=nextcord.Color.green())
                    embed.set_footer(text="Corona go poof ")
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(embed=nextcord.Embed(title="This channel is ALREADY free",
                                                        description="Don't give too much freedom. It will lead to chaos.",
                                                        color=nextcord.Color.random()))
        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Manage roles permission. :expressionless:\nJk lol U need admin perms.",
                                     color=nextcord.Color.red()))

    @commands.command(aliases=['lock', 'lockd', 'ldown', 'ld'])
    async def lockdown(self, ctx, state):
        db = TinyDB('databases/lockdown.json')
        query = Query()
        if ctx.author.guild_permissions.administrator:
            guild = ctx.guild
            everyone = nextcord.utils.get(guild.roles)
            unaffected_channels = []
            if state.lower() == 'true':
                if db.search(query.guild == ctx.guild.id)[0]['state'] is False:
                    embed = nextcord.Embed(
                        title="Turned on lockdown. No one gets in or out <a:ZOWumpusTongue:865559251764903946>",
                        color=nextcord.Color.red())
                    embed.set_footer(text="Corona is ONLINE")
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
                    await ctx.send(embed=nextcord.Embed(title="This channel is ALREADY under lockdown",
                                                        description="You can be arrested by law if you place a lockdown TWICE.",
                                                        color=nextcord.Color.random()))

            elif state.lower() == 'false':
                if db.search(query.guild == ctx.guild.id)[0]['state'] is True:
                    unaffected_channels = db.search(query.guild == ctx.guild.id)[0]['unaffected_channels']
                    for channel in guild.text_channels:
                        if channel.id in unaffected_channels:
                            pass
                        else:
                            await channel.set_permissions(everyone, send_messages=None)
                    for channel in guild.voice_channels:
                        if channel.id in unaffected_channels:
                            pass
                        else:
                            await channel.set_permissions(everyone, speak=None)
                    db.update({'state': False}, query.guild == ctx.guild.id)
                    embed = nextcord.Embed(
                        title="Lockdown has been lifted.... Enjoy Suckas <a:ZOPepeRave:865560322966421514>",
                        color=nextcord.Color.green())
                    embed.set_footer(text="Corona go poof ")
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(embed=nextcord.Embed(title="This channel is ALREADY free",
                                                        description="Don't give too much freedom. It will lead to chaos.",
                                                        color=nextcord.Color.random()))

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Manage roles permission. :expressionless:\nJk lol U need admin perms.",
                                     color=nextcord.Color.red()))

    @cog_ext.cog_slash(name="unmute", description="Allows user from typing in the server.",
                       options=[
                           create_option(name="member",
                                         description="Member who you want to unmute.",
                                         option_type=6,
                                         required=True)])
    async def _unmute(self, ctx: SlashContext, member: nextcord.Member):
        if ctx.author.guild_permissions.manage_messages:
            guild = ctx.guild
            muted_role = nextcord.utils.get(guild.roles, name="Is Muted")
            if muted_role in member.roles:
                embed = nextcord.Embed(title=f"{member.display_name} has now been unmuted!!",
                                       color=nextcord.Color.blurple())
                embed.set_footer(text="Rejoice son, don't make this mistake again")
                await member.remove_roles(muted_role)
                await ctx.send(embed=embed)
            else:
                embed = nextcord.Embed(title="This user isn't even muted.",
                                       description="Forgiveness maybe a good thing.\nBut you're still WASTING MY TIME.",
                                       color=nextcord.Color.random())
                embed.set_footer(text="If only the world had a bit of common sense...")
                await ctx.send(embed=embed)
                return

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require to be an admin!",
                                     color=nextcord.Color.red()))

    @commands.command(aliases=['unm', 'um'])
    async def unmute(self, ctx, member: nextcord.Member):
        if ctx.author.guild_permissions.manage_messages:
            guild = ctx.guild
            muted_role = nextcord.utils.get(guild.roles, name="Is Muted")
            if muted_role in member.roles:
                embed = nextcord.Embed(title=f"{member.display_name} has now been unmuted!!",
                                       color=nextcord.Color.blurple())
                embed.set_footer(text="Rejoice son, don't make this mistake again")
                await member.remove_roles(muted_role)
                await ctx.send(embed=embed)
            else:
                embed = nextcord.Embed(title="This user isn't even muted.",
                                       description="Forgiveness maybe a good thing.\nBut you're still WASTING MY TIME.",
                                       color=nextcord.Color.random())
                embed.set_footer(text="If only the world had a bit of common sense...")
                await ctx.send(embed=embed)
                return

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require to be an admin!",
                                     color=nextcord.Color.red()))

    @cog_ext.cog_slash(name="tempmute", description="Stop user from typing in the server TEMPORARILY.",
                       options=[
                           create_option(name="duration",
                                         description="Duration for which member should be muted.",
                                         option_type=3,
                                         required=True),
                           create_option(name="member",
                                         description="Member who you want to mute temporarily.",
                                         option_type=6,
                                         required=True),
                           create_option(name="reason",
                                         description="Reason for muting the member.",
                                         option_type=3,
                                         required=False)
                       ])
    async def _tempmute(self, ctx: SlashContext, duration='0s', member: nextcord.Member = None, *, reason=None):
        try:
            if duration.isdigit():
                duration = int(duration)
            else:
                duration = await convert(duration)
        except:
            await ctx.send(embed=nextcord.Embed(title="Please give a proper duration", color=nextcord.Color.random()))
            return
        guild = ctx.guild
        muted_role = nextcord.utils.get(guild.roles, name="Is Muted")
        if duration != 0:
            if member == ctx.author:
                embed = nextcord.Embed(title="Why would you even DO that?",
                                       description=f"Did you really just try to mute yourself? :person_facepalming:",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Sometimes I just wonder...")
                await ctx.send(embed=embed)
                return

            if muted_role in member.roles:
                embed = nextcord.Embed(title="Already muted idiot",
                                       description="How many times do you wish to mute this dude?",
                                       color=nextcord.Color.random())
                embed.set_footer(text="I feel sorry for my bro")
                await ctx.send(embed=embed)
                return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just mute your fellow admins.",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return

            if reason is None:
                reason = "no reason specified"

            if muted_role is None:
                perms = nextcord.Permissions(speak=False, send_messages=False, read_message_history=True,
                                             read_messages=True)
                await guild.create_role(name="Is Muted", color=nextcord.Color.dark_gray(), permissions=perms)
                muted_role = nextcord.utils.get(guild.roles, name=" Is Muted")

            message = f"You have been muted in {ctx.guild.name} for {reason}"
            try:
                await member.send(message)
            except:
                pass

            await member.add_roles(muted_role, reason=reason)
            embed = nextcord.Embed(title=f"{member.display_name} has now been muted for {duration}.!!",
                                   color=nextcord.Color.blurple())
            embed.set_footer(text="Waiting for that to end...")
            await ctx.send(embed=embed)

            await asyncio.sleep(duration)
            message2 = f"You have been unmuted in {ctx.guild.name}."
            await member.remove_roles(muted_role)

            try:
                await member.send(message2)
            except:
                pass

            embed = nextcord.Embed(title=f"{member.display_name} has now been unmuted!!",
                                   color=nextcord.Color.blurple())
            embed.set_footer(text="Rejoice son, don't make this mistake again")
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Cannot tempmute user", description="Invalid time given",
                                     color=nextcord.Color.random()))

    @commands.command(aliases=['tmute', 'tempm', 'tm'])
    async def tempmute(self, ctx, duration='0s', member: nextcord.Member = None, *, reason=None):
        try:
            if duration.isdigit():
                duration = int(duration)
            else:
                duration = await convert(duration)
        except:
            await ctx.send(embed=nextcord.Embed(title="Please give a proper duration", color=nextcord.Color.random()))
            return
        guild = ctx.guild
        muted_role = nextcord.utils.get(guild.roles, name="Is Muted")
        if duration != 0:
            if member is None:
                member = ctx.author
            if member == ctx.author:
                embed = nextcord.Embed(title="Why would you even DO that?",
                                       description=f"Did you really just try to mute yourself? :person_facepalming:",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Sometimes I just wonder...")
                await ctx.send(embed=embed)
                return

            if muted_role in member.roles:
                embed = nextcord.Embed(title="Already muted idiot",
                                       description="How many times do you wish to mute this dude?",
                                       color=nextcord.Color.random())
                embed.set_footer(text="I feel sorry for my bro")
                await ctx.send(embed=embed)
                return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just mute your fellow admins.",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return

            if reason is None:
                reason = "no reason specified"

            if muted_role is None:
                perms = nextcord.Permissions(speak=False, send_messages=False, read_message_history=True,
                                             read_messages=True)
                await guild.create_role(name="Is Muted", color=nextcord.Color.dark_gray(), permissions=perms)
                muted_role = nextcord.utils.get(guild.roles, name=" Is Muted")

            message = f"You have been muted in {ctx.guild.name} for {reason}"
            try:
                await member.send(message)

            except:
                pass

            await member.add_roles(muted_role, reason=reason)
            embed = nextcord.Embed(title=f"{member.display_name} has now been muted for {duration}!!",
                                   color=nextcord.Color.blurple())
            embed.set_footer(text="Waiting for that to end...")
            await ctx.send(embed=embed)

            await asyncio.sleep(duration)
            message2 = f"You have been unmuted in {ctx.guild.name}."
            await member.remove_roles(muted_role)

            try:
                await member.send(message2)
            except:
                pass

            embed = nextcord.Embed(title=f"{member.display_name} has now been unmuted!!",
                                   color=nextcord.Color.blurple())
            embed.set_footer(text="Rejoice son, don't make this mistake again")
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Cannot tempmute user", description="Invalid time given",
                                     color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="mute", description="Stop user from typing in the server.",
                       options=[
                           create_option(name="member",
                                         description="Member who you want to mute.",
                                         option_type=6,
                                         required=True),
                           create_option(name="reason",
                                         description="Reason for muting the member.",
                                         option_type=3,
                                         required=False)
                       ])
    async def _mute(self, ctx: SlashContext, member: nextcord.Member, *, reason="No reason given"):
        if ctx.author.guild_permissions.manage_messages:
            if member == ctx.author:
                embed = nextcord.Embed(title="Why would you even DO that?",
                                       description=f"Did you really just try to mute yourself? :person_facepalming:",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Sometimes I just wonder...")
                await ctx.send(embed=embed)
                return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just mute your fellow admins.",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return

            guild = ctx.guild
            muted_role = nextcord.utils.get(guild.roles, name="Is Muted")
            if muted_role in member.roles:
                embed = nextcord.Embed(title="Already muted idiot",
                                       description="How many times do you wish to mute this dude?",
                                       color=nextcord.Color.random())
                embed.set_footer(text="I feel sorry for my bro")
                await ctx.send(embed=embed)
                return

            if muted_role is None:
                perms = nextcord.Permissions(speak=False, send_messages=False, read_message_history=True,
                                             read_messages=True)
                await guild.create_role(name="Is Muted", color=nextcord.Color.dark_gray(), permissions=perms)
                muted_role = nextcord.utils.get(guild.roles, name=" Is Muted")

            membervar = member.display_name

            embed = nextcord.Embed(title="Muted", description=f"{membervar} was muted.",
                                   color=nextcord.Color.random())
            embed.add_field(name="reason:", value=reason, inline=True)
            await ctx.send(embed=embed)

            if muted_role is not None:
                await member.add_roles(muted_role, reason=reason)

            else:
                await ctx.send("Couldn't mute user")
                return
            for channel in guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
            try:
                await member.send(f" You have been muted in: {guild.name} reason: {reason}")
            except:
                pass
        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require to be an admin!",
                                     color=nextcord.Color.red()))

    @commands.command(aliases=['m'])
    async def mute(self, ctx, member: nextcord.Member, *, reason="No reason given"):
        if ctx.author.guild_permissions.manage_messages:
            if member == ctx.author:
                embed = nextcord.Embed(title="Why would you even DO that?",
                                       description=f"Did you really just try to mute yourself? :person_facepalming:",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Sometimes I just wonder...")
                await ctx.send(embed=embed)
                return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just mute your fellow admins.",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return

            guild = ctx.guild
            muted_role = nextcord.utils.get(guild.roles, name="Is Muted")
            if muted_role in member.roles:
                embed = nextcord.Embed(title="Already muted idiot",
                                       description="How many times do you wish to mute this dude?",
                                       color=nextcord.Color.random())
                embed.set_footer(text="I feel sorry for my bro")
                await ctx.send(embed=embed)
                return

            if muted_role is None:
                perms = nextcord.Permissions(speak=False, send_messages=False, read_message_history=True,
                                             read_messages=True)
                await guild.create_role(name="Is Muted", color=nextcord.Color.dark_gray(), permissions=perms)
                muted_role = nextcord.utils.get(guild.roles, name=" Is Muted")

            membervar = member.display_name

            embed = nextcord.Embed(title="Muted", description=f"{membervar} was muted.",
                                   color=nextcord.Color.random())
            embed.add_field(name="reason:", value=reason, inline=True)
            await ctx.send(embed=embed)

            if muted_role is not None:
                await member.add_roles(muted_role, reason=reason)

            else:
                await ctx.send("Couldn't mute user")
                return
            for channel in guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
            try:
                await member.send(f" You have been muted in: {guild.name} reason: {reason}")
            except:
                pass
        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require to be an admin!",
                                     color=nextcord.Color.red()))

    @cog_ext.cog_slash(name="kick", description="Kicks the specified user from the server.",
                       options=[
                           create_option(name="member",
                                         description="Member who you want to kick.",
                                         option_type=6,
                                         required=True),
                           create_option(name="reason",
                                         description="Reason for kicking the member.",
                                         option_type=3,
                                         required=False)
                       ])
    async def _kick(self, ctx: SlashContext, member: nextcord.Member, reason: str = "None specified"):
        if ctx.author.guild_permissions.kick_members:
            if member == ctx.author:
                embed = nextcord.Embed(title="Why would you even DO that?",
                                       description=f"Did you really just try to kick yourself? :person_facepalming:",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Sometimes I just wonder...")
                await ctx.send(embed=embed)
                return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just kick your fellow admins.",
                                       color=nextcord.Color.random())

                await ctx.send(embed=embed)
                return

            message = f"You have been kicked from {ctx.guild.name} for reason: {reason}"
            try:
                await member.send(message)

            except:
                pass
            await ctx.guild.kick(user=member, reason=reason)
            await ctx.channel.send(embed=nextcord.Embed(title=f"{member} has been kicked kicked!\nReason: {reason}",
                                                        color=nextcord.Color.random()))

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Kick Member permission.",
                                     color=nextcord.Color.green()))

    @commands.command(aliases=['k'])
    async def kick(self, ctx, member: nextcord.Member, reason: str = "None specified"):
        if ctx.author.guild_permissions.kick_members:
            if member == ctx.author:
                embed = nextcord.Embed(title="Why would you even DO that?",
                                       description=f"Did you really just try to kick yourself? :person_facepalming:",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Sometimes I just wonder...")
                await ctx.send(embed=embed)
                return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just kick your fellow admins.",
                                       color=nextcord.Color.random())

                await ctx.send(embed=embed)
                return

            message = f"You have been kicked from {ctx.guild.name} for reason: {reason}"
            try:
                await member.send(message)

            except:
                pass
            await ctx.guild.kick(member, reason)
            await ctx.channel.send(embed=nextcord.Embed(title=f"{member} has been kicked kicked!\nReason: {reason}",
                                                        color=nextcord.Color.random()))

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Kick Member permission.",
                                     color=nextcord.Color.green()))

    @cog_ext.cog_slash(name="unban", description="Unbans users, obviously.",
                       options=[
                           create_option(name="member",
                                         description="Member who you want to unban.",
                                         option_type=6,
                                         required=True)])
    async def _unban(self, ctx: SlashContext, member: nextcord.User = None):
        if ctx.author.guild_permissions.ban_members:
            if member is None or member == ctx.message.author:
                await ctx.channel.send("You cannot unban yourself")
                return
            await ctx.guild.unban(member)
            await ctx.channel.send(embed=nextcord.Embed(title=f"{member} is unbanned!", color=nextcord.Color.random()))

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Ban Member permission.",
                                     color=nextcord.Color.green()))

    @commands.command(aliases=['unb', 'ub'])
    async def unban(self, ctx, member: nextcord.User = None):
        if ctx.author.guild_permissions.ban_members:
            if member is None or member == ctx.message.author:
                await ctx.channel.send("You cannot unban yourself")
                return
            await ctx.guild.unban(member)
            await ctx.channel.send(embed=nextcord.Embed(title=f"{member} is unbanned!", color=nextcord.Color.random()))

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Ban Member permission.",
                                     color=nextcord.Color.green()))

    @cog_ext.cog_slash(name="tempban", description="Bans users, TEMPORARILY.",
                       options=[
                           create_option(name="duration",
                                         description="Duration for which member should be banned.",
                                         option_type=3,
                                         required=True),
                           create_option(name="member",
                                         description="Member who you want to ban temporarily.",
                                         option_type=6,
                                         required=True),
                           create_option(name="reason",
                                         description="Reason for banning the member.",
                                         option_type=3,
                                         required=False)
                       ])
    async def _tempban(self, ctx: SlashContext, duration='0s', member=None, *, reason=None):
        try:
            if duration.isdigit():
                duration = int(duration)
            else:
                duration = await convert(duration)
        except:
            await ctx.send(embed=nextcord.Embed(title="Please give a proper duration", color=nextcord.Color.random()))
            return
        if duration != 0:
            if member == ctx.author:
                embed = nextcord.Embed(title="Why would you even DO that?",
                                       description=f"Did you really just try to ban yourself? :person_facepalming:\nEven temporarily, that's just stupid.",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Sometimes I just wonder...")
                await ctx.send(embed=embed)
                return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just ban your fellow admins temporarily!",
                                       color=nextcord.Color.random())
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
                embed = nextcord.Embed(
                    title=f"You have been banned from {ctx.guild.name} for {reason}",
                    description=f"Use this {str(invite)} to join after {duration}",
                    color=nextcord.Color.random())
                embed.set_image(url=random.choice(banned_gifs))
                try:
                    await member.send(embed=embed)
                except:
                    pass

                await ctx.guild.ban(member)
                embed1 = nextcord.Embed(
                    title=f"{member.display_name} has been banned for {reason}",
                    description=f"They will be allowed to return in {duration}",
                    color=nextcord.Color.random()
                )
                embed1.set_image(url=random.choice(banned_gifs))
                await ctx.send(embed=embed1)
                await asyncio.sleep(duration)
                await ctx.guild.unban(member)
                await ctx.channel.send(embed=nextcord.Embed(
                    title=f"{member.display_name} has been unbanned.",
                    description=f"They will be here soon enough...",
                    color=nextcord.Color.random()
                ))

            else:
                await ctx.send(
                    embed=nextcord.Embed(title="Stop right there!",
                                         description="You require the Ban Member permission.",
                                         color=nextcord.Color.green()))

    @commands.command(aliases=['tempb', 'tban', 'tb'])
    async def tempban(self, ctx, duration='0s', member: nextcord.Member = None, *, reason=None):
        try:
            if duration.isdigit():
                duration = int(duration)
            else:
                duration = await convert(duration)
        except:
            await ctx.send(embed=nextcord.Embed(title="Please give a proper duration", color=nextcord.Color.random()))
            return
        if duration != 0:
            if member == ctx.author:
                embed = nextcord.Embed(title="Why would you even DO that?",
                                       description=f"Did you really just try to ban yourself? :person_facepalming:\nEven temporarily, that's just stupid.",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Sometimes I just wonder...")
                await ctx.send(embed=embed)
                return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just ban your fellow admins temporarily!",
                                       color=nextcord.Color.random())
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
                embed = nextcord.Embed(
                    title=f"You have been banned from {ctx.guild.name} for {reason}",
                    description=f"Use this {str(invite)} to join after {duration}",
                    color=nextcord.Color.random())
                embed.set_image(url=random.choice(banned_gifs))
                try:
                    await member.send(embed=embed)
                except:
                    pass
            

                await ctx.guild.ban(member)
                embed1 = nextcord.Embed(
                    title=f"{member.display_name} has been banned for {reason}",
                    description=f"They will be allowed to return in {duration}",
                    color=nextcord.Color.random()
                )
                embed1.set_image(url=random.choice(banned_gifs))
                await ctx.send(embed=embed1)
                await asyncio.sleep(duration)
                await ctx.guild.unban(member)
                await ctx.channel.send(embed=nextcord.Embed(
                    title=f"{member.display_name} has been unbanned.",
                    description=f"They will be here soon enough...",
                    color=nextcord.Color.random()
                ))

            else:
                await ctx.send(
                    embed=nextcord.Embed(title="Stop right there!",
                                         description="You require the Ban Member permission.",
                                         color=nextcord.Color.green()))

    @cog_ext.cog_slash(name="ban", description="Bans users, like, DUH.",
                       options=[
                           create_option(name="member",
                                         description="Member who you want to ban.",
                                         option_type=6,
                                         required=True),
                           create_option(name="reason",
                                         description="Reason for banning the member.",
                                         option_type=3,
                                         required=False)
                       ])
    async def _ban(self, ctx: SlashContext, member: nextcord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            banned_gifs = ["https://media.tenor.com/images/d41f93e7538f0afb56ad1450fed9c02e/tenor.gif",
                           "https://media.tenor.com/images/048b3da98bfc09b882d3801cb8eb0c1f/tenor.gif",
                           "https://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif",
                           "https://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif",
                           "https://media.tenor.com/images/1a84c478d1073757cf8929a89e47bbfc/tenor.gif"]

            if member == ctx.message.author:
                if member == ctx.author:
                    embed = nextcord.Embed(title="Why would you even DO that?",
                                           description=f"Did you really just try to ban yourself? :person_facepalming: ",
                                           color=nextcord.Color.random())
                    embed.set_footer(text="Sometimes I just wonder...")
                    await ctx.send(embed=embed)
                    return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just ban your fellow admins.",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return

            if reason is None:
                reason = "No reason specified"
            message = nextcord.Embed(title=f"You have been banned from {ctx.guild.name} for {reason}",
                                     color=nextcord.Color.random())
            try:
                await member.send(embed=message)

            except:
                pass

            await ctx.guild.ban(user=member, reason=reason)
            await ctx.channel.send(f"{member} is banned!")
            embed1 = nextcord.Embed(
                title=f"{member.display_name} has been banned for {reason}",
                description=f"Their mouth has been perma-shut",
                color=nextcord.Color.random()
            )
            embed1.set_image(url=random.choice(banned_gifs))
            await ctx.send(embed=embed1)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Ban Member permission.",
                                     color=nextcord.Color.green()))

    @commands.command(aliases=['b'])
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            banned_gifs = ["https://media.tenor.com/images/d41f93e7538f0afb56ad1450fed9c02e/tenor.gif",
                           "https://media.tenor.com/images/048b3da98bfc09b882d3801cb8eb0c1f/tenor.gif",
                           "https://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif",
                           "https://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif",
                           "https://media.tenor.com/images/1a84c478d1073757cf8929a89e47bbfc/tenor.gif"]

            if member == ctx.message.author:
                if member == ctx.author:
                    embed = nextcord.Embed(title="Why would you even DO that?",
                                           description=f"Did you really just try to ban yourself? :person_facepalming: ",
                                           color=nextcord.Color.random())
                    embed.set_footer(text="Sometimes I just wonder...")
                    await ctx.send(embed=embed)
                    return

            if member.guild_permissions.administrator:
                embed = nextcord.Embed(title="Nuh uh not happening",
                                       description="You can't just ban your fellow admins.",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return

            if reason is None:
                reason = "No reason specified"
            message = nextcord.Embed(title=f"You have been banned from {ctx.guild.name} for {reason}",
                                     color=nextcord.Color.random())
            try:
                await member.send(embed=message)

            except:
                pass

            await ctx.guild.ban(user=member, reason=reason)
            await ctx.channel.send(f"{member} is banned!")
            embed1 = nextcord.Embed(
                title=f"{member.display_name} has been banned for {reason}",
                description=f"Their mouth has been perma-shut",
                color=nextcord.Color.random()
            )
            embed1.set_image(url=random.choice(banned_gifs))
            await ctx.send(embed=embed1)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Ban Member permission.",
                                     color=nextcord.Color.green()))

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.channel.slomode_delay == 0:
                await ctx.send(embed=nextcord.Embed(title="Slowmode disabled already dumbass",
                                                    color=nextcord.Color.random()))

            elif ctx.author.guild_permissions.administrator:
                await ctx.channel.edit(slowmode_delay=0)
                await ctx.send(embed=nextcord.Embed(title="Slowmode disabled!", color=nextcord.Color.dark_magenta(),
                                                    description="Now y'all can talk your heart out"))

            else:
                await ctx.send(
                    embed=nextcord.Embed(title="Stop right there!",
                                         description="You require the Administrators permission.",
                                         color=nextcord.Color.green()))

        if isinstance(error, commands.BadArgument):
            await ctx.send(
                embed=nextcord.Embed(title="How hard is it to set a slowmode :rolling_eyes: ",
                                     color=nextcord.Color.magenta(),
                                     description=f"Do {ctx.prefix}slowmode to disable it and {ctx.prefix}slowmode 10 to set slowmode of 10 secs"))

    @blacklist.error
    async def blacklist_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"C'mon dude",
                                   description=f"I don't really want to stop people from using me\nBut if you really want me too, then at least tell me who to stop?",
                                   color=nextcord.Color.random())
            embed.set_footer(text="The least you can do")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Please stop making this hard for me...",
                                   description=f"Just mention who I must stop.\nRandom names won't really do",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Is this necessary")
            await ctx.send(embed=embed)
        else:
            raise error

    @unblacklist.error
    async def unblacklist_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Are u serious?",
                                   description=f"Reminding you the blacklisting thin air is NOT possible",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I mean, isn't it obvious?")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Stop memeing. Just stop.",
                                   description=f"This user is not in this server.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Have some mercy...")
            await ctx.send(embed=embed)
        else:
            raise error

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"That's pretty vague",
                                   description=f"You tell me to clear message but don't tell me how many.\nSo do I clear them all?",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Maybe NOT a good idea...")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.BadArgument):
            embed = nextcord.Embed(title=f"Numbers. -_-",
                                   description=f"I can only clear a number of messages. What else did you expect?",
                                   color=nextcord.Color.random())
            embed.set_footer(text="You be being sus")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.MemberNotFound):
            embed = nextcord.Embed(title=f"Couldn't find this member",
                                   description=f"Why can't you just gve me\nA PROPER MEMBER",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Im really so bored of this")
            await ctx.send(embed=embed)

        else:
            raise error

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"I couldn't find this dude.",
                                   description=f"So instead I warned my friend Louis here...",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Wait... what have you done to Louis?")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            if "reason" in str(error.param):
                embed = nextcord.Embed(title=f"Alright I'll bite",
                                       description=f"What should I warn the user for?",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Can't just warn him cause you said so can I?")
                await ctx.send(embed=embed)
            else:
                embed = nextcord.Embed(title=f"Alright I'll bite",
                                       description=f"Who am I supposed to warn?",
                                       color=nextcord.Color.random())
                embed.set_footer(text="Mentioning that wud be gr8")
                await ctx.send(embed=embed)

        else:
            raise error

    @userwarn.error
    async def userwarn_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"I refuse",
                                   description=f"I simply refuse to give you the warnings of *NOTHING*",
                                   color=nextcord.Color.random())
            embed.set_footer(text="That would be a crime")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.UserNotFound):
            embed = nextcord.Embed(title=f"Ok no",
                                   description=f"Reminding you that seeing the warnings of an invalid user is not allowed!",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Kids these days...")
            await ctx.send(embed=embed)
        else:
            raise error

    @lockdown.error
    async def lockdown_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Ah sad",
                                   description=f"U need to use either {ctx.prefix}lockdown true or {ctx.prefix}lockdown false",
                                   color=nextcord.Color.random())
            embed.set_footer(text="That's how that works")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(title=f"I need more PERMS",
                                   description=f"I need to be able to manage the server.\nNow use your common sense and give me the perm necessary.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Hopefully you have some")
            await ctx.send(embed=embed)

        else:
            raise error

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Mention the user please",
                                   description=f"I cannot unmute the void obviously",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Mentioning someone helps tho")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"I really don't like this",
                                   description=f"Pretty sure that Mr. Nothing couldn't talk in the first place.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="unmuting nothing is a horrific idea")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"Nope, the member is more powerful than me",
                                   description=f"Maybe put my role above him :pleading_face:",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I feel weak")
            await ctx.send(embed=embed)
        else:
            raise error

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Mention the user please",
                                   description=f"I cannot kick the void obviously",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Mentioning someone helps tho")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"I really don't like this",
                                   description=f"Pretty sure that this person didn't exist in the first place.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Kicking the air... *shudder")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"Nope, the member is more powerful than me",
                                   description=f"Maybe put my role above him :pleading_face:",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I feel weak")
            await ctx.send(embed=embed)

        else:
            raise error

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Muting is not nice...",
                                   description=f"But if you insist on it, mention *WHO* you want to mute.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Because respect")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Muting random people is acceptable...",
                                   description=f"...when the people actually exist",
                                   color=nextcord.Color.random())
            embed.set_footer(text="So make sure they do")
            await ctx.send(embed=embed)

        else:
            raise error

    @tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Trying to tempmute no one",
                                   description=f"Is not something people do\nYou seriously must mention who you wanna temp mute.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="This *no user mentioned* thing is getting old.")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Did you just try to temp mute a user who isn't in this server.",
                                   description=f"Tbh I deal with that non-sense so much I'm not even surprised.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="But seriously, stop")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"Nope, the member is more powerful than me",
                                   description=f"Maybe put my role above him :pleading_face:",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I feel weak")
            await ctx.send(embed=embed)

        else:
            raise error

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"If only you were competent",
                                   description=f"You would know the banning no one is a waste of time.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Unpoggers indeed")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Banning is a sad thing",
                                   description=f"It becomes 10 times worse when you can't even properly tell me who to ban!",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I may not have a life but still")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):

            embed = nextcord.Embed(title=f"Nope, the member is more powerful than me",

                                   description=f"Maybe put my role above him :pleading_face:",

                                   color=nextcord.Color.random())

            embed.set_footer(text="I feel weak")

            await ctx.send(embed=embed)

        else:
            raise error

    @tempban.error
    async def tempban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Sure thing buddy",
                                   description=f"Ima tempban my old buddy Louis. Oh wait...",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I think that's why I couldn't find him be4")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"You failed at typing properly",
                                   description=f"What else is new...",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I think the guy about to be banned is relieved")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"Nope, the member is more powerful than me",
                                   description=f"Maybe put my role above him :pleading_face:",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I feel weak")
            await ctx.send(embed=embed)

        else:
            raise error

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Unbanning is a sign of mercy",
                                   description=f"But it would make you look better in front of your friends if you mention someone to ban.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="IOn the bright side, you can now unban someone")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.UserNotFound):
            embed = nextcord.Embed(title=f"Ahh the difficulty..",
                                   description=f"It must be so hard for you to be able to mention a valid user.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="This is sarcasm")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"Hold up!",
                                   description=f"What do you think I am? The server owner?\nI can't do that, I don't got the permission!",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Stop trying to take my rights")
            await ctx.send(embed=embed)

        else:
            raise error


def setup(bot):
    bot.add_cog(Moderation(bot))
