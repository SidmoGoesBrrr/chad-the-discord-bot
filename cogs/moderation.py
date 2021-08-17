import discord
import asyncio
from discord.ext import commands
import random
from tinydb import TinyDB, Query
import re

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
    
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command()
    async def slowmode(self,ctx, seconds: int):
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
    

    @commands.command()
    async def blacklist(self,ctx, member: discord.Member):
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


    @commands.command()
    async def unblacklist(self,ctx, member: discord.Member):
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


    @commands.command()
    async def clear(self,ctx, times: int, hide=None):
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


    @commands.command()
    async def warn(self,ctx, member: discord.Member, *, reason: str):
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
                    await ctx.send(embed=discord.Embed(title="Please provide a reason",
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


    @commands.command()
    async def userwarn(self,ctx, member: discord.Member):
        db = TinyDB('databases/warnings.json')
        guild_id_var = ctx.guild.id
        query = Query()
        tht_member_warnings = db.search(query['member'] == str(member))
        a = db.search((query['guild_id'] == guild_id_var) & (query['member'] == str(member)))
        embed = discord.Embed(title=f"Here are the warnings for {member.display_name}:", description="Warnings")
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


    @commands.command()
    async def lockdown(self,ctx, state):
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

    @commands.command()
    async def unmute(self,ctx, member: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name="Is Muted")
            guild = ctx.guild
            if mutedRole in member.roles:
                embed = discord.Embed(title=f"{member.display_name} has now been unmuted!!", color=discord.Color.blurple())
                embed.set_footer(text="Rejoice son, don't make this mistake again")
                await member.remove_roles(mutedRole)
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


    @commands.command()
    async def tempmute(self,ctx,duration: TimeConverter, member: discord.Member, *, reason=None):
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


    @commands.command()
    async def mute(self,ctx, member: discord.Member, *, reason="No reason given"):
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

            if checkping(ctx.message.guild.id)=='true':
                membervar=member.mention

            else:
                membervar=member.display_name

            embed = discord.Embed(title="Muted", description=f"{membervar} was muted.",
                                color=discord.Color.random())
            embed.add_field(name="reason:", value=reason, inline=True)
            await ctx.send(embed=embed)

            if mutedRole is not None:
                await member.add_roles(mutedRole, reason=reason)

            else:
                await ctx.send("Couldn't mute user")
                return
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


    @commands.command()
    async def kick(self,ctx, member: discord.Member):
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


    @commands.command()
    async def unban(self,ctx, member: discord.User = None):
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


    @commands.command()
    async def tempban(self,ctx, duration: TimeConverter, member: discord.Member, *, reason=None):
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
                    color=discord.Color.random())
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


    @commands.command()
    async def ban(self,ctx, member: discord.Member, *, reason=None):
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

def setup(bot):
    bot.add_cog(Moderation(bot))