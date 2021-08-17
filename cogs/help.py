import discord
import asyncio
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def help(self, ctx, command=None):
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        if command is None:
            embed = discord.Embed(title="Help", colour=discord.Color.random())
            embed.add_field(name="Utilities",
                            value="`!help utilities`",
                            inline=True)
            embed.add_field(name="Moderation",
                            value="`!help moderation`",
                            inline=True)
            embed.add_field(name="Information",
                            value="`!help information`",
                            inline=True)
            embed.add_field(name="Fun", value="`!help fun`", inline=True)
            embed.add_field(name="Games", value="`!help games`", inline=True)
            embed.add_field(
                name=f"Most Important Commands",
                value=
                f"Prefix:\n{ctx.prefix}help prefix\nPing Settings:\n{ctx.prefix}help pingset\nInvite to other servers:\n{ctx.prefix}help invite\nSupport Server:\n{ctx.prefix}help support",
                inline=False)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return

        elif command.lower() == "utilities" or command.lower() == "utils":
            page = 1
            pages = 3
            help_utils_1 = discord.Embed(title="Utilities")
            help_utils_1.add_field(
                name="Ping",
                value=f"This allows you to check my ping.\n{ctx.prefix}help ping")
            help_utils_1.add_field(
                name="MakeRole",
                value=
                f"Makes a new role in the server for you!\n{ctx.prefix}help makerole",
                inline=False)
            help_utils_1.add_field(
                name="AddRole",
                value=f"Gives the user a role!\n{ctx.prefix}help addrole",
                inline=False)
            help_utils_1.add_field(
                name="EditRole",
                value=
                f"Edits an existing role in the server.\n{ctx.prefix}help editrole",
                inline=False)
            help_utils_1.add_field(
                name="RemoveRole",
                value=f"Takes away a user's role.\n{ctx.prefix}help removerole",
                inline=False)
            help_utils_1.add_field(
                name="DeleteRole",
                value=f"Deletes a role in the server.\n{ctx.prefix}help deleterole",
                inline=False)
            help_utils_1.set_footer(text="Page 1 of 3")
            help_utils_1.color = discord.Color.random()

            help_utils_2 = discord.Embed(title="Utilities")
            help_utils_2.add_field(
                name="UserInfo",
                value=
                f"Gives the  information of the member specified...\n{ctx.prefix}help userinfo",
                inline=False)
            help_utils_2.add_field(
                name="ServerInfo",
                value=
                f"Provides the information about the server.\n{ctx.prefix}help serverinfo",
                inline=False)
            help_utils_2.add_field(
                name="Robmoji",
                value=
                f"Robs an emoji! Basically takes an emoji from any server and uploads it here(in dis server) so everyone can use it!\n{ctx.prefix}help robmoji",
                inline=False)
            help_utils_2.add_field(
                name="Nick",
                value=
                f"Change nicknames in the server by using this feature.\n{ctx.prefix}help nick",
                inline=False)
            help_utils_2.add_field(
                name="Afk",
                value=
                f"Shows your friends that you are afk for some reason.\n{ctx.prefix}help afk",
                inline=False)
            help_utils_2.add_field(
                name="Reminder",
                value=
                f"Remind yourself to do something in a certain amount of time!.\n{ctx.prefix}help remind",
                inline=False)
            help_utils_2.set_footer(text="Page 2 of 3")
            help_utils_2.color = discord.Color.random()

            help_utils_3 = discord.Embed(title="Utilities")
            help_utils_3.add_field(
                name="About",
                value=f"Tells you something more about ME!\n{ctx.prefix}help about",
                inline=False)
            help_utils_3.add_field(
                name="Vote",
                value=f"Gives link to vote for me!\n{ctx.prefix}help vote",
                inline=False)
            help_utils_3.add_field(
                name="Snipe",
                value=
                f"Allows You to restore the last deleted message of the channel.\n{ctx.prefix}help snipe",
                inline=False)
            help_utils_3.add_field(
                name="Invite",
                value=
                f"Gives you the link to invite me to your servers!\n{ctx.prefix}help invite",
                inline=False)
            help_utils_3.add_field(
                name="Support",
                value=
                f"Gives you my support server invite!\n{ctx.prefix}help support",
                inline=False)
            help_utils_3.add_field(
                name="Website",
                value=f"Takes you to my devs' website!\n{ctx.prefix}help website",
                inline=False)
            help_utils_3.set_footer(text="Page 3 of 3")
            help_utils_3.color = discord.Color.random()

            util_message = await ctx.send(embed=help_utils_1)

            await util_message.add_reaction("◀️")
            await util_message.add_reaction("▶️")
            while True:

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in [
                        "◀️", "▶️"
                    ] and reaction.message == util_message

                try:
                    reaction, user = await self.bot.wait_for("reaction_add",
                                                            timeout=300,
                                                            check=check)

                    if str(reaction.emoji) == "▶️":
                        page += 1
                        if page == pages + 1:
                            page = 1
                        try:
                            await util_message.remove_reaction(reaction, user)
                        except:
                            print("Could not remove reaction in help")
                    elif str(reaction.emoji) == "◀️":
                        page -= 1
                        if page == 0:
                            page = pages
                        try:
                            await util_message.remove_reaction(reaction, user)
                        except:
                            print("Could not remove reaction in help")

                    else:
                        try:
                            await util_message.remove_reaction(reaction, user)
                        except:
                            print("Could not remove reaction in help")

                    if page == 1:
                        try:
                            await util_message.edit(embed=help_utils_1)
                        except:
                            print("Could not edit")
                    elif page == 2:
                        try:
                            await util_message.edit(embed=help_utils_2)
                        except:
                            print("Could not edit")
                    elif page == 3:
                        try:
                            await util_message.edit(embed=help_utils_3)
                        except:
                            print("Could not edit")
                    pass
                except asyncio.TimeoutError:
                    print("Timed out oops")

        elif command.lower() == "moderation" or command.lower() == "mod":
            page = 1
            pages = 3
            help_mod_1 = discord.Embed(title="Moderation")
            help_mod_1.add_field(
                name="Prefix",
                value=
                f"Shows the prefix and allows you to change it!.\n{ctx.prefix}help prefix",
                inline=False)
            help_mod_1.add_field(
                name="Slowmode",
                value=
                f"Allows moderators to enable/disable slowmode.\n{ctx.prefix}help slowmode",
                inline=False)
            help_mod_1.add_field(
                name="Blacklist",
                value=f"Blacklists a user.\n{ctx.prefix}help blacklist",
                inline=False)
            help_mod_1.add_field(
                name="Unblacklist",
                value=f"Unblacklists a user.\n{ctx.prefix}help unblacklist",
                inline=False)
            help_mod_1.add_field(
                name="Clear",
                value=f"Clears messages in a channel.\n{ctx.prefix}help clear",
                inline=False)
            help_mod_1.set_footer(text="Page 1 of 3")
            help_mod_1.color = discord.Color.random()

            help_mod_2 = discord.Embed(title="Moderation")
            help_mod_2.add_field(
                name="Lockdown",
                value=
                f"Enforces lockdown in the server.\n{ctx.prefix}help lockdown",
                inline=False)
            help_mod_2.add_field(
                name="Warn",
                value=f"Gives a warning to a user.\n{ctx.prefix}help warn",
                inline=False)
            help_mod_2.add_field(
                name="UserWarn",
                value=
                f"Displays the history of warnings given to a user.\n{ctx.prefix}help userwarn",
                inline=False)
            help_mod_2.add_field(
                name="Unmute",
                value=
                f"Allows user from typing in the server.\n{ctx.prefix}help unmute",
                inline=False)
            help_mod_2.add_field(
                name="Tempmute",
                value=
                f"Stop user from typing in the server TEMPORARILY.\n{ctx.prefix}help tempmute",
                inline=False)
            help_mod_2.add_field(
                name="Mute",
                value=
                f"Stop user from typing in the server.\n{ctx.prefix}help mute",
                inline=False)
            help_mod_2.set_footer(text="Page 2 of 3")
            help_mod_2.color = discord.Color.random()

            help_mod_3 = discord.Embed(title="Moderation")
            help_mod_3.add_field(
                name="Kick",
                value=
                f"Kicks the specified user from the server.\n{ctx.prefix}help kick",
                inline=False)
            help_mod_3.add_field(
                name="Unban",
                value=f"Unbans users, obviously.\n{ctx.prefix}help unban",
                inline=False)
            help_mod_3.add_field(
                name="Tempban",
                value=f"Bans users, TEMPORARILY.\n{ctx.prefix}help tempban",
                inline=False)
            help_mod_3.add_field(
                name="Ban",
                value=f"Bans users, like, DUH.\n{ctx.prefix}help ban",
                inline=False)
            help_mod_3.set_footer(text="Page 3 of 3")
            help_mod_3.color = discord.Color.random()
            mod_message = await ctx.send(embed=help_mod_1)

            await mod_message.add_reaction("◀️")
            await mod_message.add_reaction("▶️")
            while True:

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in [
                        "◀️", "▶️"
                    ] and reaction.message == util_message

                try:
                    reaction, user = await self.bot.wait_for("reaction_add",
                                                            timeout=300,
                                                            check=check)

                    if str(reaction.emoji) == "▶️":
                        page += 1
                        if page == pages + 1:
                            page = 1
                        try:
                            await mod_message.remove_reaction(reaction, user)
                        except:
                            print("Could not remove reaction in help")
                    elif str(reaction.emoji) == "◀️":
                        page -= 1
                        if page == 0:
                            page = pages
                        try:
                            await mod_message.remove_reaction(reaction, user)
                        except:
                            print("Could not remove reaction in help")

                    else:
                        try:
                            await mod_message.remove_reaction(reaction, user)
                        except:
                            print("Could not remove reaction in help")

                    if page == 1:
                        try:
                            await mod_message.edit(embed=help_mod_1)
                        except:
                            print("Could not edit")
                    elif page == 2:
                        try:
                            await mod_message.edit(embed=help_mod_2)
                        except:
                            print("Could not edit")
                    elif page == 3:
                        try:
                            await mod_message.edit(embed=help_mod_3)
                        except:
                            print("Could not edit")
                    pass
                except asyncio.TimeoutError:
                    print("Timed out oops")

        elif command.lower() == "information" or command.lower() == "info":
            page = 1
            pages = 1
            help_info_1 = discord.Embed(title="Information")
            help_info_1.add_field(
                name="Dictionary",
                value=
                f"Finds dictionary meanings, synonyms and antonyms.\n{ctx.prefix}help dictionary",
                inline=False)
            help_info_1.add_field(
                name="Translate",
                value=
                f"Translates a word into any language needed.\n{ctx.prefix}help translate",
                inline=False)
            help_info_1.add_field(
                name="Weather",
                value=
                f"Gives you the current weather of a place.\n{ctx.prefix}help weather",
                inline=False)
            help_info_1.add_field(
                name="Wiki",
                value=f"Searches up the Wikipedia for you.\n{ctx.prefix}help wiki",
                inline=False)
            help_info_1.add_field(
                name="UrbanDictionary",
                value=
                f"Allows you to access the Urban Dictionary.\n{ctx.prefix}help urban",
                inline=False)
            help_info_1.set_footer(text="Page 1 of 1")
            help_info_1.color = discord.Color.random()
            fun_message = await ctx.send(embed=help_info_1)

        elif command.lower() == "fun":
            page = 1
            pages = 3
            help_fun_1 = discord.Embed(title="Fun")
            help_fun_1.add_field(
                name="Ask",
                value=
                f"Honestly answers a question you may have.\n{ctx.prefix}help ask",
                inline=False)
            help_fun_1.add_field(
                name="Repeat",
                value=f"Repeats your message.\n{ctx.prefix}help repeat",
                inline=False)
            help_fun_1.add_field(
                name="Dice",
                value=f"Roles a dice for you.\n{ctx.prefix}help dice",
                inline=False)
            help_fun_1.add_field(
                name="EpicGamerRate",
                value=
                f"Tells you how EPIC you are at gaming.\n{ctx.prefix}help epicgamerrate",
                inline=False)
            help_fun_1.add_field(
                name="SimpRate",
                value=
                f"Tells you how much you are simping.\n{ctx.prefix}help simprate",
                inline=False)
            help_fun_1.add_field(
                name="Poll",
                value=f"Creates a poll for you.\n{ctx.prefix}help poll",
                inline=False)
            help_fun_1.set_footer(text="Page 1 of 3")
            help_fun_1.color = discord.Color.random()

            help_fun_2 = discord.Embed(title="Fun")
            help_fun_2.add_field(
                name="Script",
                value=f"Translates the Zero&One script.\n{ctx.prefix}help script",
                inline=False)
            help_fun_2.add_field(
                name="Binary",
                value=
                f"Converts string to binary as zeros and ones are cool\n{ctx.prefix}help binary",
                inline=False)
            help_fun_2.add_field(
                name="ASCII",
                value=f"Creates a cool ASCII art for you.\n{ctx.prefix}help ascii",
                inline=False)
            help_fun_2.add_field(
                name="Act",
                value=
                f"Makes me act as though I'm another user...\n{ctx.prefix}help act",
                inline=False)
            help_fun_2.add_field(
                name="Chooser",
                value=
                f"Lets you choose between the given options.\n{ctx.prefix}help chooser",
                inline=False)
            help_fun_2.add_field(
                name="Coinflip",
                value=f"Flips a coin for you.\n{ctx.prefix}help coinflip",
                inline=False)
            help_fun_2.set_footer(text="Page 2 of 3")
            help_fun_2.color = discord.Color.random()

            help_fun_3 = discord.Embed(title="Fun")
            help_fun_3.add_field(
                name="Hack",
                value=f"Hacks the required user.\n{ctx.prefix}help hack",
                inline=False)
            help_fun_3.add_field(
                name="Gif",
                value=
                f"Allows to search for GIFs or send random.\n{ctx.prefix}help gif",
                inline=False)
            help_fun_3.add_field(
                name="ImageMemes",
                value=
                f"Makes some very funny image memes for you.\n{ctx.prefix}help imagememes",
                inline=False)
            help_fun_3.add_field(
                name="VCMeme",
                value=
                f"Let's you have some fun with the people in your VC.\n{ctx.prefix}help vcmeme",
                inline=False)
            help_fun_3.add_field(
                name="Quote",
                value=
                f"Allows you to quote the sayings of your fellow human beings.\n{ctx.prefix}help quote",
                inline=False)
            help_fun_3.set_footer(text="Page 3 of 3")
            help_fun_3.color = discord.Color.random()
            fun_message = await ctx.send(embed=help_fun_1)

            await fun_message.add_reaction("◀️")
            await fun_message.add_reaction("▶️")
            while True:

                def check(reaction, user):
                    return user == ctx.author and str(
                        reaction.emoji) in ["◀️", "▶️"]

                try:
                    reaction, user = await self.bot.wait_for("reaction_add",
                                                            timeout=300,
                                                            check=check)

                    if str(reaction.emoji) == "▶️":
                        page += 1
                        if page == pages + 1:
                            page = 1
                        try:
                            await fun_message.remove_reaction(reaction, user)
                        except:
                            print("Could not remove reaction in help")
                    elif str(reaction.emoji) == "◀️":
                        page -= 1
                        if page == 0:
                            page = pages
                        try:
                            await fun_message.remove_reaction(reaction, user)
                        except:
                            print("Could not remove reaction in help")

                    else:
                        try:
                            await fun_message.remove_reaction(reaction, user)
                        except:
                            print("Could not remove reaction in help")

                    if page == 1:
                        try:
                            await fun_message.edit(embed=help_fun_1)
                        except:
                            print("Could not edit")
                    elif page == 2:
                        try:
                            await fun_message.edit(embed=help_fun_2)
                        except:
                            print("Could not edit")
                    elif page == 3:
                        try:
                            await fun_message.edit(embed=help_fun_3)
                        except:
                            print("Could not edit")
                    pass
                except asyncio.TimeoutError:
                    print("Timed out oops")

        elif command.lower() == "games":
            page = 1
            pages = 1
            help_games_1 = discord.Embed(title="Games")
            help_games_1.add_field(
                name="Guess",
                value=
                f"Lets you guess a number within any range.\n{ctx.prefix}help guess",
                inline=False)
            help_games_1.add_field(
                name="Rps",
                value=
                f"Lets you play rock paper scissor with me **OR** your friends{ctx.prefix}\n{ctx.prefix}help rps",
                inline=False)
            help_games_1.add_field(
                name="OddEve",
                value=
                f"Lets you play odd eve with me **OR** your friends{ctx.prefix}\n(cricket version coming out soon)\n{ctx.prefix}help oddeve",
                inline=False)
            help_games_1.add_field(name="More games coming soon!",
                                  value=f"You better believe it!")
            help_games_1.set_footer(text="Page 1 of 1")
            help_games_1.color = discord.Color.random()

            game_message = await ctx.send(embed=help_games_1)

        elif command.lower() == "settings" or command.lower() == "set":
            page = 1
            pages = 1
            help_set_1 = discord.Embed(title="Settings")
            help_set_1.add_field(
                name="Ping settings",
                value=
                f"To toggle on and off the ping settings\n{ctx.prefix}help pingset",
                inline=False)
            help_set_1.set_footer(text="Page 1 of 1")
            help_set_1.color = discord.Color.random()

            set_message = await ctx.send(embed=help_set_1)

        elif command.lower() == 'ping':
            embed = discord.Embed(
                title="Help Ping",
                description=
                "With this command, you can see how fast I am reacting to your messages in milliseconds.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(name="Usage:", value=f"{ctx.prefix}ping")
            embed.set_footer(text="I do be very fast u know...")
            await ctx.send(embed=embed)

        elif command.lower() == 'makerole':
            embed = discord.Embed(
                title="Help MakeRole",
                description=
                "At last, with just one command, you can make a new role in your server.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}makerole <rolename>\nCause you have the right to be LAZY"
            )
            embed.set_footer(
                text=
                "Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'addrole':
            embed = discord.Embed(
                title="Help AddRole",
                description=
                "You can also add roles to your members by just using this one command!",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}addrole @<membername> @<rolename>\nSo now you can be LAZIER!"
            )
            embed.set_footer(
                text=
                "Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'editrole':
            embed = discord.Embed(
                title="Help EditRole",
                description=
                "Don't like the name of your role?\n Then just use this command to change its name!",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}editrole @<fromrolename> <torolename>\nCause why not?"
            )
            embed.set_footer(
                text=
                "Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'removerole':
            embed = discord.Embed(
                title="Help RemoveRole",
                description=
                "If your members misuse their roles then there is only one solution:\n Take the role away from them!",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}removerole @<membername> @<rolename>\nBasically making you a dictator..."
            )
            embed.set_footer(
                text=
                "Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'deleterole':
            embed = discord.Embed(
                title="Help DeleteRole",
                description=
                "You can also delete roles in your server when the role just becomes useless.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}deleterole @<rolename>\nImagine needing to delete roles ANYWAY..."
            )
            embed.set_footer(
                text=
                "Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'support':
            embed = discord.Embed(
                title="Help Support",
                description=
                "Need help with the my commands?\nWanna complain about them?\nMaybe make a suggestion?",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}support\nSo you can visit our support server.")
            embed.set_footer(text="Get support its good for you")
            await ctx.send(embed=embed)

        elif command.lower() == 'userinfo':
            embed = discord.Embed(
                title="Help UserInfo",
                description="Find out about the wierdos who join your servers.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}userinfo @<membername>\n#gettingexposed")
            embed.set_footer(text="Being a stalker eh?")
            await ctx.send(embed=embed)

        elif command.lower() == 'robmoji':
            embed = discord.Embed(
                title="Help RobMoji",
                description=
                "Steal an emoji from another server and make it yours. If a name is not given, it will take the emoji's name. Also pls make sure that you give a name from 2 to 32.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}robmoji emoji name_of_new_emoji\n#MINE!")
            embed.set_footer(text="Should I call the cops?")
            await ctx.send(embed=embed)

        elif command.lower() == 'serverinfo':
            embed = discord.Embed(
                title="Help ServerInfo",
                description="For everything you need to know about your server.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}serverinfo\nNever forget your memories, or your server info."
            )
            embed.set_footer(text="But seriously, how did you forget?")
            await ctx.send(embed=embed)

        elif command.lower() == 'nick':
            embed = discord.Embed(
                title="Help Nick",
                description=
                "Nickname your friends anything you want!\nIt is WAY too easy to do so, with this command.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}nick @<membername> <nickname>\nNow see what you can come up with..."
            )
            embed.set_footer(
                text="Nasty surprise for the poor victim's names *sigh*")
            await ctx.send(embed=embed)

        elif command.lower() == 'afk':
            embed = discord.Embed(
                title="Help Afk",
                description=
                "Use this to make people know that your are afk when they ping you.\nUseful to warn people about your afkness!",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}afk <reason>\nThis will solve a lot of afk problems..."
            )
            embed.set_footer(text="Why didn't we think of this be4?")
            await ctx.send(embed=embed)

        elif command.lower() == 'remind' or command.lower() == 'reminder':
            embed = discord.Embed(
                title="Help Reminder",
                description=
                "Nickname your friends anything you want!\nIt is WAY too easy to do so, with this command.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}remind <time> <thingtoremind>\nThis is specially for people who forget what they were doing in like, 2 seconds"
            )
            embed.set_footer(text="Now you cannot forget ANYTHING")
            await ctx.send(embed=embed)

        elif command.lower() == 'about':
            embed = discord.Embed(
                title="Help About",
                description="Get to know a little bit more about me!",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}about\nPlease use this :pleading_face:\nMy devs think NO ONE wants to know more about me..."
            )
            embed.set_footer(text="I mean, why not?")
            await ctx.send(embed=embed)

        elif command.lower() == 'vote':
            embed = discord.Embed(title="Help Vote",
                                  description="Vote me or perish",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}vote\nSupports me a lot :pleading_face:\nMakes me.... **EVEN MORE POPULAR**"
            )
            embed.set_footer(text="I mean, why not?")
            await ctx.send(embed=embed)

        elif command.lower() == 'snipe':
            embed = discord.Embed(
                title="Help Snipe",
                description=
                "Find out what the last deleted message in your server was.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}snipe\nNow you can catch your sneaky server members in the act!"
            )
            embed.set_footer(text="More stonx for u")
            await ctx.send(embed=embed)

        elif command.lower() == 'invite':
            embed = discord.Embed(
                title="Help invite",
                description="Use this to invite me to your other servers.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}invite\nPlease use this :pleading_face:\nYou. Can't. Get. Enough. Of. Me."
            )
            embed.set_footer(text="I'm the BEST")
            await ctx.send(embed=embed)

        elif command.lower() == 'website':
            embed = discord.Embed(
                title="Help Website",
                description="My developers have a website. Go check it out.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}website\nPlease use this :pleading_face:\nIt's not really related to me, but its cool anyway."
            )
            embed.set_footer(text="See you there!")
            await ctx.send(embed=embed)

        elif command.lower() == 'slowmode':
            embed = discord.Embed(
                title="Help Slowmode",
                description=
                "Allows you to put or remove a slowmode in your channel.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}slowmode <timeinseconds>\nThat will stop the SPAMMERS"
            )
            embed.set_footer(text="Sad life for spammers.")
            await ctx.send(embed=embed)

        elif command.lower() == 'blacklist':
            embed = discord.Embed(
                title="Help Blacklist",
                description="This makes users unable to use my commands.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}blacklist @<membername>\nThis is one of the most CRUELLEST punishments possible."
            )
            embed.set_footer(text="Not using CHAD be SAD")
            await ctx.send(embed=embed)

        elif command.lower() == 'unblacklist':
            embed = discord.Embed(
                title="Help Unblacklist",
                description=
                "Removes blacklisted users from the list of naughty people...",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}unblacklist @<membername>\nOnly kindness can make you use this command."
            )
            embed.set_footer(text="Unblacklisters = Saviours")
            await ctx.send(embed=embed)

        elif command.lower() == 'clear':
            embed = discord.Embed(
                title="Help Clear",
                description="Clears the required number of messages in a channel.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}clear\nHelps when your server members just don't want to stop chatting..."
            )
            embed.set_footer(text="Get ERASED")
            await ctx.send(embed=embed)

        elif command.lower() == 'lockdown':
            embed = discord.Embed(
                title="Help Lockdown",
                description="Basically stops EVERYONE from using the channel.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}lockdown <trueorfalse>\nFor total Monarchy servers.")
            embed.set_footer(text="Imagine needing lockdown in discord...")
            await ctx.send(embed=embed)

        elif command.lower() == 'warn':
            embed = discord.Embed(title="Help Warn",
                                  description="Gives the rule-breakers a warning!",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}warn <username> <reason>\nOnly for those naughty users who don't like rules."
            )
            embed.set_footer(text="So you've been warned...")
            await ctx.send(embed=embed)

        elif command.lower() == 'prefix':
            embed = discord.Embed(title="Help Prefix",
                                  description="Change dat prefix",
                                  colour=discord.Color.random(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}prefix <newprefix>\nVery handy for big servers!"
            )
            embed.set_footer(text="Just don't forget what your prefix was...")
            await ctx.send(embed=embed)

        elif command.lower() == 'userwarn':
            embed = discord.Embed(
                title="Help UserWarn",
                description=
                "Gives a record of why and how many times a user was warned in the server.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}userwarn @<username>\nNow you have a record of their crimes."
            )
            embed.set_footer(text="*Evil laughter from admins*")
            await ctx.send(embed=embed)

        elif command.lower() == 'unmute':
            embed = discord.Embed(title="Help Unmute",
                                  description="Allows you to unmute a user.",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}unmute @<username>\nThis makes the able to talk in your server again."
            )
            embed.set_footer(text="Support Freedom of Speech")
            await ctx.send(embed=embed)

        elif command.lower() == 'tempmute':
            embed = discord.Embed(
                title="Help Tempmute",
                description="Allows you to temporarily mute a user.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}tempmute <timeinseconds>s @<username>\nIf you think you may forget to unmute a user, then I do it for you!"
            )
            embed.set_footer(text="That's one less thing to remember...")
            await ctx.send(embed=embed)

        elif command.lower() == 'mute':
            embed = discord.Embed(title="Help Mute",
                                  description="Allows you to mute a user.",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}mute @<username>\nNow they can't talk until you allow them too!"
            )
            embed.set_footer(text="Sad life for the muted")
            await ctx.send(embed=embed)

        elif command.lower() == 'kick':
            embed = discord.Embed(title="Help Kick",
                                  description="Allows you to kick a user.",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}kick @<username>\nSo basically they just get yeeted out."
            )
            embed.set_footer(text="Get rekt lol")
            await ctx.send(embed=embed)

        elif command.lower() == 'unban':
            embed = discord.Embed(title="Help Unban",
                                  description="Allows you to unban a user.",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}unban @<username>\nSo that they can return to the server."
            )
            embed.set_footer(text="Oh look, they're back lol")
            await ctx.send(embed=embed)

        elif command.lower() == 'tempban':
            embed = discord.Embed(
                title="Help Tempban",
                description="Allows you to temporarily ban a user.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}tempban <timeinseconds>s @<username>\nIf you really hate someone, and may \"accidentally\" forget to unban them..."
            )
            embed.set_footer(text="That's just sus uk")
            await ctx.send(embed=embed)

        elif command.lower() == 'ban':
            embed = discord.Embed(title="Help Ban",
                                  description="Allows you to ban a user.",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}ban @<username>\nThey can NEVER COME BACK NOW MWA HA HA HA\nJeez I was only joking"
            )
            embed.set_footer(text="Get banished lmao")
            await ctx.send(embed=embed)

        elif command.lower() == 'dictionary':
            embed = discord.Embed(
                title="Help Dictionary",
                description="Lets you access a dictionary through discord!",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}dictionary <word>\nWhat you can do is get meanings, synonyms and antonyms!\nThen you type either meanings, synonyms or antonyms."
            )
            embed.set_footer(text="All for geeky lil nerds!")
            await ctx.send(embed=embed)

        elif command.lower() == 'translate':
            embed = discord.Embed(
                title="Help Translate",
                description="Translate a word to any language you want.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}translate <wordtotranslate>\nAnd then you enter the language translate to."
            )
            embed.set_footer(text="Merci!")
            await ctx.send(embed=embed)

        elif command.lower() == 'weather':
            embed = discord.Embed(
                title="Help Weather",
                description="Get the real-time weather of any place!",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}search <cityname>\nAny city can be searched for!")
            embed.set_footer(text="Try searching \"Israel\" lol")
            await ctx.send(embed=embed)

        elif command.lower() == 'wiki':
            embed = discord.Embed(title="Help Wiki",
                                  description="Search Wikipedia.",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}wiki <whatyouwannasearch>\nCause clearly, google wasn't enough."
            )
            embed.set_footer(text="Wisdom is in DISCORD PPL")
            await ctx.send(embed=embed)

        elif command.lower() == 'urban':
            embed = discord.Embed(
                title="Help UrbanDictionary",
                description="Let's you use the Urban Dictionary (like, obviously).",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}urban <whatyouwannasearch>\nAn interesting place of knowledge."
            )
            embed.set_footer(
                text=
                "The urban dict be lollers (I mean try searching your own name)")
            await ctx.send(embed=embed)

        elif command.lower() == 'ask':
            embed = discord.Embed(title="Help Ask",
                                  description="Answer you question for you.",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}ask <question>\nIts prophetic power is to be respected."
            )
            embed.set_footer(text="The Bot don't lie...")
            await ctx.send(embed=embed)

        elif command.lower() == 'repeat':
            embed = discord.Embed(title="Help Repeat",
                                  description="Makes me spam for you..",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}repeat <numberoftimes> <messagetorepeat>\nWhy do I have to do the dirty work?"
            )
            embed.set_footer(text="Just don't get blacklisted lol")
            await ctx.send(embed=embed)

        elif command.lower() == 'dice':
            embed = discord.Embed(
                title="Help Dice",
                description="Makes me **role**(pun intended) a dice for you.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}dice\nYou get a random number for 1 to 6! Yay!"
            )
            embed.set_footer(text="Ok this is starting to get ridiculously lazy")
            await ctx.send(embed=embed)

        elif command.lower() == 'epicgamerrate':
            embed = discord.Embed(
                title="Help epicgamerrate",
                description="Now you can find out how epic you are at gaming.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}epicgamerrate\nThis is totally true btw")
            embed.set_footer(
                text="It's a perfect way of knowing how good you are!")
            await ctx.send(embed=embed)

        elif command.lower() == 'simprate':
            embed = discord.Embed(
                title="Help simprate",
                description="Now you can find out how much you simp.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}simprate\nThis is totally true btw")
            embed.set_footer(
                text="It's a perfect way of knowing how simpy you are!")
            await ctx.send(embed=embed)

        elif command.lower() == 'poll':
            embed = discord.Embed(title="Help Poll",
                                  description="Create a poll to get some votes",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}poll <timeinseconds> <whatyoupollfor>: <optionswithcommas>\nEveryone can just choose what they wanna choose."
            )
            embed.set_footer(
                text="I don't think there is any other way to poll on discord...")
            await ctx.send(embed=embed)

        elif command.lower() == 'script':
            embed = discord.Embed(title="Help Script",
                                  description="Translates the ZeroAndOne Script",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}encrypt <stufftoencrypt>\n!decrypt <stufftodecrypt>\nCheck out the way this script works [here](https://secret-message-encoder-decoder.itszeroandone.repl.co/)."
            )
            embed.set_footer(text="You'll love the script.")
            await ctx.send(embed=embed)

        elif command.lower() == 'ascii':
            embed = discord.Embed(
                title="Help ASCII",
                description="Turns me into a painter and makes ASCII art.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}ascii <stufftoput>\nI can't really explain it's beauty."
            )
            embed.set_footer(text="What you put may or may not be what you get")
            await ctx.send(embed=embed)

        elif command.lower() == 'act':
            embed = discord.Embed(
                title="Help Act",
                description="Use this to make me act like another user!",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}act @<usertoactlike> <messagetouse>\nMostly used for fake evidence :smiling_imp:"
            )
            embed.set_footer(text="This is for pure evil purposes")
            await ctx.send(embed=embed)

        elif command.lower() == 'binary':
            embed = discord.Embed(title="Help binary",
                                  description="converts string to binary",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(name="Usage:",
                            value=f"{ctx.prefix}binary <yourstring>")
            embed.set_footer(text="Zeros and Ones are cool")
            await ctx.send(embed=embed)

        elif command.lower() == 'choose' or command.lower() == 'chooser':
            embed = discord.Embed(title="Help Choose",
                                  description="Makes a choice for you.",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}choose <choices>\nAgain, this bot knows everything.\nIt makes the correct choice."
            )
            embed.set_footer(text="The bot KNOWS")
            await ctx.send(embed=embed)

        elif command.lower() == 'coinflip':
            embed = discord.Embed(
                title="Help Coinflip",
                description=
                "Flips a coin. Seriously why do you even need help in that?",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}coinflip <heads/tails>\nYou choose correct, you win."
            )
            embed.set_footer(text="So pretty obvious how you lose")
            await ctx.send(embed=embed)

        elif command.lower() == 'hack':
            embed = discord.Embed(
                title="Help Hack",
                description="Totally hacks the targeted user pc.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}hack @<membername>\nA lot of bad stuff happens.\nUse only in cases of extreme hate or prejudice."
            )
            embed.set_footer(text="The bad stuff be bad")
            await ctx.send(embed=embed)

        elif command.lower() == 'gif':
            embed = discord.Embed(
                title="Help Gif",
                description="Allows you to search giphy for GIFS",
                colour=discord.Color.random(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}gif <nameofgif>\nGifs are cool yay")
            embed.set_footer(text="Who needs inbuilt GIFs smh")
            await ctx.send(embed=embed)

        elif command.lower() == 'imagememes':
            embed = discord.Embed(title="Help ImageMemes",
                                  description="Cool memes with images!",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}imagememes \nGives you a list of image memes. Enjoy!"
            )
            embed.set_footer(text="Cause there can NEVER be enough memes")
            await ctx.send(embed=embed)

        elif command.lower() == 'vcmeme':
            embed = discord.Embed(title="Help VCMeme",
                                  description="Prank your friends in your VC.",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}vcmeme <chosenvcmeme>\nThe list is long...\nTo check the list, type {ctx.prefix}vcmeme"
            )
            embed.set_footer(text="I feel sorry for VC users...")
            await ctx.send(embed=embed)

        elif command.lower() == 'quote':
            embed = discord.Embed(
                title="Help Quote",
                description=
                "Creates a quote so you can remember your most famous sayings!",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}quote <quoter> <quote>\nIt gives you glory.")
            embed.set_footer(text="Always remember...")
            await ctx.send(embed=embed)

        elif command.lower() == 'guess':
            embed = discord.Embed(
                title="Help Guess",
                description=
                "Let's you play guess the number between literally any two numbers.\nBetween 1 and 10000\nLmao",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}guess <lowerboundary> <upperboundary>\nThen you just guess ig..."
            )
            embed.set_footer(text="Bet you can't beat my dev Zero in 1 - 10000")
            await ctx.send(embed=embed)

        elif command.lower() == 'rps':
            embed = discord.Embed(title="Help RPS",
                                  description="You can either play:",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Single player:",
                value=
                f"Use {ctx.prefix}rps <rock/paper/scissors> to play against me, or"
            )
            embed.add_field(
                name="Multi player:",
                value=
                f"Use {ctx.prefix}rps @<useryouwanttodefeat> to play against them."
            )
            embed.set_footer(text="Its a great game!")
            await ctx.send(embed=embed)

        elif command.lower() == 'oddeve':
            embed = discord.Embed(title="Help OddEve",
                                  description="You can either play:",
                                  colour=discord.Color.green(),
                                  inline=True)
            embed.add_field(
                name="Single player:",
                value=f"Use {ctx.prefix}oddeve <odd/even> to play against me, or")
            embed.add_field(
                name="Multi player:",
                value=
                f"Use {ctx.prefix}oddeve <useryouwanttodefeat> to play against them."
            )
            embed.set_footer(text="Its a great game!")
            await ctx.send(embed=embed)

        elif command.lower() == 'pingset' or command.lower() == 'pingsettings':
            embed = discord.Embed(
                title="Help Ping Settings",
                description=
                "This allows/ stops Chad from using pings in your server.",
                colour=discord.Color.green(),
                inline=True)
            embed.add_field(
                name="Usage:",
                value=
                f"{ctx.prefix}pingsettings <trueorfalse>.\nA very, very useful command indeed!"
            )
            embed.set_footer(text="Now no more Chad annoying you with pings eyyy")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
