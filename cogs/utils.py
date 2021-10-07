
import discord
import asyncio
from discord.ext import commands
import calendar
import time
from tzlocal import get_localzone
from datetime import datetime, timedelta
import aiohttp
from tinydb import TinyDB, Query
def checkping(guild_id_var):
    db = TinyDB('databases/pings.json')
    query = Query()
    values = str(list(map(lambda entry: entry["pingstate"],
                          db.search(query.guild_id == str(guild_id_var))))[0])

    return values.lower()

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.sniped_messages = {}


    @commands.command(aliases=['p'])
    async def ping(self,ctx):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.send(embed=discord.Embed(title="Testing Ping...", color=discord.Color.random()))
        end_time = time.time()

        await message.edit(embed=discord.Embed(title=f"Latency: {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms", color=discord.Color.random()))
    
      
    @commands.command(aliases=['maker', 'mrole', 'mr'])
    async def makerole(self,ctx, *, rolename):
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


    @commands.command(aliases=['addr', 'arole', 'ar'])
    async def addrole(self,ctx, member: discord.Member, *, role: discord.Role = None):
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


    @commands.command(aliases=['editr', 'erole', 'er'])
    async def editrole(self,ctx, from_role: discord.Role, *, to_role):
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


    @commands.command(aliases=['remover', 'rrole', 'rr'])
    async def removerole(self,ctx, member: discord.Member, *, role: discord.Role = None):
        if ctx.author.guild_permissions.manage_roles:
            embed = discord.Embed(
                title=f"Role Removed",
                description=f"{role} has been removed from {member.name}."
            )
            embed.color = discord.Color.random()
            embed.set_footer(text=f"")
            await member.remove_roles(role)
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=discord.Embed(title="Stop right there!", description="You require the Manage Roles permission.",
                                    color=discord.Color.green()))


    @commands.command(aliases=['deleter', 'drole', 'dr'])
    async def deleterole(self,ctx, rolename: discord.Role):
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
    

    @commands.command(aliases=['user', 'uinfo', 'ui'])
    async def userinfo(self,ctx, target: discord.Member):
        x = ctx.guild.members
        if target in x:
            roles = [role for role in target.roles if role != ctx.guild.default_role]
            if roles == []:
                roles = None
            embed = discord.Embed(title="User information", color=discord.Color.gold(),
                                timestamp=datetime.utcnow())

            embed.set_author(name=target.name, icon_url=target.avatar_url)

            embed.set_thumbnail(url=target.avatar_url)

            embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                            icon_url=ctx.author.avatar_url)

            if roles is None:
                fields = [("Name", str(target), False),
                        ("ID", target.id, False),
                        ("Status", str(target.status).title(), False),
                        (f"Roles", "No roles", False),
                        ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S") + " UTC", False),
                        ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S") + " UTC", False)]

            else:
                fields = [("Name", str(target), False),
                        ("ID", target.id, False),
                        ("Status", str(target.status).title(), False),
                        (f"Roles ({len(roles)})", " ".join([role.mention for role in roles]), False),
                        ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S")+" UTC", False),
                   ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S")+" UTC", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'You have to ping someone from this server and this server only')
        

    @commands.command(aliases=['server', 'sinfo', 'si'])
    @commands.guild_only()
    async def serverinfo(self,ctx):
        format = "%a, %d %b %Y | %H:%M:%S %UTC"
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

    @commands.command(aliases=['robemoji', 'remoji', 'robmo', 'rm'])
    async def robmoji(self, ctx, emoji: discord.PartialEmoji, *, Name=None):
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

    
    @commands.command(aliases=['n'])
    async def nick(self, ctx, member=None, *, nick=None):
        if member is None and nick is None:
            if ctx.author.guild_permissions.change_nickname:
                await ctx.author.edit(nick=None)
                embed = discord.Embed(title=f"Your nickname has been removed",
                                              description=f"Your name is now displayed as {ctx.author.display_name}",
                                              color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(
                embed=discord.Embed(title="I refuse", description="You require the change nickname permission.",
                                    color=discord.Color.red()))
                return

        if member != None:
            if '@' in member:
              member = await commands.MemberConverter().convert(ctx, member)

        if isinstance(member, str) or (isinstance(member, discord.Member) and ctx.author == member):
            if ctx.author.guild_permissions.change_nickname:
                if type(member) is not discord.Member:
                  if nick is None:
                      nick = str(member)
                  else:
                      nick = str(member) + " " + nick
                if len(nick) > 48:
                    embed = discord.Embed(title=f"That nickname is TOO LONG",
                                    description=f" I'd probably get bored changing it.\nTry a nickname that has less then 32 characters.",
                                    color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
                await ctx.author.edit(nick=nick)
                embed = discord.Embed(title=f"Your nickname has been changed",
                                          description=f"Your name is now displayed as {ctx.author.display_name}",
                                          color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(
                embed=discord.Embed(title="I refuse", description="You require the change nickname permission.",
                                    color=discord.Color.red()))
                return

        elif isinstance(member, discord.Member):
            if ctx.author.guild_permissions.manage_nicknames:
                if nick is None:
                    await member.edit(nick=member.name)
                    embed = discord.Embed(title=f"Nickname removed for {member.name}",
                                          description=f"Their name is now displayed as {member.display_name}",
                                          color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return

                elif len(nick) > 48:
                    embed = discord.Embed(title=f"That nickname is TOO LONG",
                                    description=f" I'd probably get bored changing it.\nTry a nickname that has less then 48 characters.",
                                    color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return

                await member.edit(nick=nick)
                embed = discord.Embed(title=f"Nickname changed for {member.name}",
                                          description=f"Their name is now displayed as {member.display_name}",
                                          color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            else:
                await ctx.send(
                    embed=discord.Embed(title="I refuse", description="You require the manage nicknames permission.",
                                        color=discord.Color.red()))

     

        
    @commands.command()
    async def afk(self,ctx, *, reason=None):
        if reason is None:
            embed = discord.Embed(title="Give ME A REASON",
                                description="You can't be afk for ___",
                                color=discord.Color.random())
            embed.set_footer(text="That's Louis' job")
            await ctx.send(embed=embed)
            return

        if len(reason) > 30:
            embed = discord.Embed(title="I'm sorry.",
                                description="I got bored reading your LONG reason.\nSo I ignored it.",
                                color=discord.Color.random())
            embed.set_footer(text="Nothing more than 30 characters please")
            await ctx.send(embed=embed)
            return

        db = TinyDB('databases/afk.json')
        db.insert({'afk_user': ctx.author.id, 'reason': reason})
        
        await ctx.send(embed=discord.Embed(title=f"Ok {ctx.author.display_name}.",
                                        description=f"I have set your status as afk for {reason}.",
                                        color=discord.Color.random()))


    @commands.command(aliases=['remind'])
    async def reminder(self, ctx, time, *, reminder):
        embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.')
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"

        if seconds == 0:
            embed.add_field(name='Warning',
                            value='Please specify a proper duration')

        elif seconds < 120:
            embed.add_field(name='Warning',
                            value='You have specified too short a duration!\nMinimum duration is 2 minutes.')

        elif seconds > 7776000:
            embed.add_field(name='Warning', value='You have specified too long a duration!\nMaximum duration is 90 days.')

        else:
            await ctx.send(embed=discord.Embed(title=f"I wish I had a title for this embed",
                                            description=f"But I will remind you about {reminder} in {counter}.",
                                            color=discord.Color.random()))
            await asyncio.sleep(seconds)
            await ctx.send(f"{ctx.author.mention} Hi, you asked me to remind you to \"{reminder}\" {counter} ago.")
            return

        await ctx.send(embed=embed)

    @commands.command(aliases=['sf'])
    async def snowflake(self, ctx, id: int):
        def utc_to_local(utc_dt):
            timestamp = calendar.timegm(utc_dt.timetuple())
            local_dt = datetime.fromtimestamp(timestamp, tz=get_localzone())
            print(local_dt)
            assert utc_dt.resolution >= timedelta(microseconds=1)
            return local_dt.replace(microsecond=utc_dt.microsecond)
        utc_dt = discord.utils.snowflake_time(id)
        local_dt = utc_to_local(utc_dt=utc_dt)
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        def custom_strftime(format, t):
            return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

        utc_dt = custom_strftime("%a, {S} %b, %Y \|| %I:%M:%S %p", utc_dt)
        local_dt = custom_strftime("%a, {S} %b, %Y \|| %I:%M:%S %p", local_dt)
        print(utc_dt)
        print(local_dt)
        await ctx.send(embed=discord.Embed(title=f"ID {id}",
                                          description=f"Was created on {utc_dt} UTC and\non {local_dt} in your local time.",
                                          color=discord.Color.random()))


    @commands.command(aliases=['ab'])
    async def about(self,ctx):
        about_embed = discord.Embed(title="About ME!", color=discord.Color.green())
        about_embed.add_field(name="Bot Developed by:", value=f"ZeroAndOne, [My epic devs!](https://zeroandone.ml)")
        about_embed.add_field(name="Created to:", value=f"Make discord a better place. :angel:")
        about_embed.add_field(name="Features:", value=f"Use !help", inline=True)
        about_embed.add_field(name="Give me feedback and complains here. Help me improve myself!\nAlso useful for finding out about the latest Chad updates!!",
                            value=f"[Support Server](https://discord.gg/wTsj4DZhyZ)", inline=True)
        about_embed.add_field(name="Vote for me and make me POPULAR!!",value=f"[I'm on top.gg](https://top.gg/bot/864010316424806451/vote)", inline=True)
        user = self.bot.get_user(864010316424806451)
        about_embed.add_field(name="Vote for me here too!",value=f"[I'm on the Discord Bot List](https://discordbotlist.com/bots/chad-6621/upvote)", inline=True)
        about_embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=about_embed)


    @commands.command(aliases=['v'])
    async def vote(self,ctx):
        vote = discord.Embed(title="Vote for me buckaroo!",color=discord.Color.random())
        vote.add_field(name="1",value = f"[top.gg](https://top.gg/bot/864010316424806451/vote)")
        vote.add_field(name="2",value = f"[discordbotlist.com](https://discordbotlist.com/bots/chad-6621/upvote)")
        vote.set_thumbnail(url="https://i.imgur.com/QICgRpf.png")
        await ctx.send(embed=vote)


    @commands.Cog.listener()
    async def on_message_delete(self,message):
        self.bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

        
    @commands.command(aliases=['inv'])
    async def invite(self,ctx):
        embed = discord.Embed(
            title="Invite",
            description=f"To invite me to your own server [click here](https://discord.com/api/oauth2/authorize?client_id=864010316424806451&permissions=4227997759&scope=applications.commands%20bot)")
        
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.color = discord.Color.green()
        await ctx.send(embed=embed)


    @commands.command(aliases=['sup'])
    async def support(self,ctx):
        embed = discord.Embed(title="Support Server",
                            description="To visit our support server, click [here](https://discord.gg/wTsj4DZhyZ).\nNow you can complain all you want!!",
                            color=discord.Color.random())
        embed.set_footer(text=f"Support Server requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)



    @commands.command(aliases=['web', 'site', 'www', 'zo'])
    async def website(self, ctx):
        embed = discord.Embed(title="Link for our website",
                            color=discord.Color.dark_magenta(),
                            description="This is our main [website](https://zeroandone.netlify.app/)\nClick [here](https://www.youtube.com/channel/UCF0DZYNiHcIGZKBoPWfc0lg) to see our YouTube Channel.")
        embed.set_footer(text=f"Website requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pat', 'donate'])
    async def patreon(self,ctx):
        embed = discord.Embed(title="Here is our patreon.",
                            description="Donate to us [here](https://www.patreon.com/TheChadBot) to show your love for Chad!",
                            color=discord.Color.random())
        embed.set_footer(text=f"Patreon requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        


    @commands.command(aliases=['sn'])
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time = self.bot.sniped_messages[ctx.guild.id]
            
        except:
            await ctx.send(embed=discord.Embed(title="Couldn't find a message to snipe!", color=discord.Color.random()))
            return

        embed = discord.Embed(description=contents, color=discord.Color.random(), timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")

        await ctx.channel.send(embed=embed)


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


    @nick.error
    async def nick_error(self,ctx,error):
        if isinstance(error, commands.errors.CommandInvokeError):
            embed = discord.Embed(title=f"Nope, the member is more powerful than me",
                                description=f"Maybe put my role above him :pleading_face:",
                                color=discord.Color.random())
            embed.set_footer(text="I feel weak")
            await ctx.send(embed=embed)

        else:
            raise (error)

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
  
    @snowflake.error
    async def snowflake_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="The given ID **NOTHING**",
                                              description="Was never created.",
                                              color=discord.Color.random()))

        else:
            raise (error)
    
def setup(bot):
    bot.add_cog(Utils(bot))
