import discord
import asyncio
from discord.ext import commands
import random
import math


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['g'])
    async def guess(self, ctx, lower, upper):
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

            msg = await self.bot.wait_for("message", check=check)
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

    @commands.command()
    async def rps(self, ctx, *, msg=None):
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
                embed.color = discord.Color.random()
                embed.set_footer(text="Its not over yet...")
                await ctx.send(embed=embed)

            elif player == "rock" or player == "r":
                if computer == "paper":
                    embed = discord.Embed(
                        title="You lose!",
                        description=f"{t[1]} covers {t[0]}".format(computer, player))
                    embed.color = discord.Color.random()
                    embed.set_footer(text="Sad life 4 u...")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="You win!",
                        description=f"{t[0]} breaks {t[2]}".format(player, computer))
                    embed.color = discord.Color.random()
                    embed.set_footer(text="GG")
                    await ctx.send(embed=embed)

            elif player == "paper" or player == "p":
                if computer == "scissors":
                    embed = discord.Embed(
                        title="You lose!",
                        description=f"{t[2]} cut {t[1]}".format(computer, player))
                    embed.color = discord.Color.random()
                    embed.set_footer(text="Sad life 4 u...")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="You win!",
                        description=f"{t[1]} covers {t[0]}".format(player, computer))
                    embed.color = discord.Color.random()
                    embed.set_footer(text="GG")  # dont test yet im almost done too
                    await ctx.send(embed=embed)

            elif player == "scissors" or player == "s" or player == "s":
                if computer == "rock":
                    embed = discord.Embed(
                        title="You lose!",
                        description=f"{t[0]} breaks {t[2]}".format(computer, player))
                    embed.color = discord.Color.random()
                    embed.set_footer(text="Sad life 4 u...")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="You win!",
                        description=f"{t[2]} cut {t[1]}".format(player, computer))
                    embed.color = discord.Color.random()
                    embed.set_footer(text="GG")
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="What the hell bruh",
                    description=f"You have managed to put an invalid option in rock paper scissors. :rolling_eyes:")
                embed.color = discord.Color.random()
                embed.set_footer(text="Imagine having just 3 brain cells")
                await ctx.send(embed=embed)


        elif isinstance(msg, discord.Member):
            embed1 = discord.Embed(
                title=f"Hello!! So you have challenged {msg.name} to an epic rock paper scissor battle!",
                description="Enter your choice from Rock,Paper,Scissors here",
                color=discord.Color.random())
            embed2 = discord.Embed(
                title=f"Hello! So you have been challenged by {ctx.author.name} to an epic rock paper scissor battle!",
                description="Enter your choice from Rock, Paper or Scissors here (if you wanna play)",
                color=discord.Color.random())
            embed2.set_footer(text="Otherwise just ignore me like everyone else (SOB SOB)")
            if msg.bot:
                embed = discord.Embed(title=f"This is a bot.",
                                      description=f"I seriously don't know how you expect a bot to play rock paper scissors with you WHEN IT CAN'T EVEN DM YOU BACK",
                                      color=discord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            if msg == ctx.author:
                embed = discord.Embed(title=f"Oh you lonely kid",
                                      description=f"If you got no friends to play with, try `{ctx.prefix}rock` or something",
                                      color=discord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            await msg.send(embed=embed2)
            await ctx.author.send(embed=embed1)
            await ctx.send("<a:ZO_DMS:871341236236193792>")

            def check1(message):
                return message.author == ctx.author and str(message.channel.type) == "private"
                print(message.type)

            def check2(message):
                return message.author == msg and str(message.channel.type) == "private"

            try:
                reply1 = await self.bot.wait_for('message', check=check1, timeout=60)
                reply2 = await self.bot.wait_for('message', check=check2, timeout=60)
                player = reply2.content.lower()
                challenger = reply1.content.lower()
                playerName = msg.name
                challengerName = ctx.author.name
                if player == challenger:
                    embed = discord.Embed(
                        title="Tie",
                        description=f"Both played {player}!")
                    embed.color = discord.Color.random()
                    embed.set_footer(text="Its not over yet...")
                    await ctx.send(embed=embed)

                elif player == "rock" or player == "r":
                    if challenger == "paper" or challenger == "p":
                        embed = discord.Embed(
                            title=f"{challengerName} wins!",
                            description=f"Paper[{challengerName}] covers Rock[{playerName}]!!")
                        embed.color = discord.Color.random()
                        embed.set_footer(text=f"Sad life {playerName}...")
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title=f"{playerName} wins!",
                            description=f"Rock[{playerName}] breaks Scissors[{challengerName}]!!")
                        embed.color = discord.Color.random()
                        embed.set_footer(text=f"Sad life {challengerName}...")
                        await ctx.send(embed=embed)

                elif player == "paper" or player == "p":
                    if challenger == "scissors" or challenger == "s" or challenger == "scissor":
                        embed = discord.Embed(
                            title=f"{challengerName} wins!",
                            description=f"Scissors[{challengerName}] cut paper[{playerName}]!!")
                        embed.color = discord.Color.random()
                        embed.set_footer(text=f"Sad life {playerName}...")
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title=f"{playerName} wins!",
                            description=f"Paper[{playerName}] covers rock[{challengerName}]!!")
                        embed.color = discord.Color.random()
                        embed.set_footer(text=f"Sad life {challengerName}...")
                        await ctx.send(embed=embed)

                elif player == "scissors" or player == "s" or player == "scissor":
                    if challenger == "rock" or challenger == "r":
                        embed = discord.Embed(
                            title=f"{challengerName} wins!",
                            description=f"Rock[{challengerName}] breaks scissors[{playerName}]!!")
                        embed.color = discord.Color.random()
                        embed.set_footer(text=f"Sad life {playerName}...")
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title=f"{playerName} wins!",
                            description=f"Scissors[{playerName}] cut paper[{challengerName}]!!")
                        embed.color = discord.Color.random()
                        embed.set_footer(text=f"Sad life {challengerName}...")
                        await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        title="Well either you dont want to play or you have not spelled correctly",
                        description=f"Why are you like this.... :rolling_eyes:")
                    embed.color = discord.Color.random()
                    embed.set_footer(text="Imagine being such a spoil sport")
                    await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(title="That kid didn't answer in time",
                                                   description="THEY IGNORED MEEEEE <a:ZO_Cry:871340549725102081>",
                                                   color=discord.Color.random()))

        else:
            await ctx.send(embed=discord.Embed(title="You might wanna", description="CHOOSE SOMETHING USEFUL",
                                               color=discord.Color.random()))

    @commands.command(aliases=['oddeven', 'oe'])
    async def oddeve(self, ctx, *, msg=None):
        if msg is None:
            await ctx.send(
                embed=discord.Embed(title="You might wanna", description="CHOOSE SOMETHING!!\n try odd or even",
                                    color=discord.Color.random()))
            return

        if '@' in msg:
            msg = await commands.MemberConverter().convert(ctx, msg)

        if isinstance(msg, str):
            if msg.lower() == "odd" or msg.lower() == "o":
                euro = "odd"

            elif msg.lower() == "even" or msg.lower() == "e":
                euro = "even"

            else:
                embed = discord.Embed(
                    title="What the hell bruh",
                    description=f"You have managed to put an invalid option in odd n even.\nIts either odd or even :rolling_eyes:",
                    color=discord.Color.random()
                )
                embed.color = discord.Color.random()
                embed.set_footer(text="Imagine having just 3 brain cells")
                await ctx.send(embed=embed)
                return

            await ctx.send(embed=discord.Embed(title="Please select a number for 0 to 9", color=discord.Color.random()))

            def check1(message):
                return message.author == ctx.author

            try:
                msg1 = await self.bot.wait_for('message', check=check1, timeout=60)
                num1 = int(msg1.content)
                if num1 >= 10 or num1 < 0:
                    await ctx.send(
                        embed=discord.Embed(title="WHAT PART OF 0 TO 9 DO YOU NOT UNDERSTAND",
                                            color=discord.Color.random()))
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
            except asyncio.exceptions.TimeoutError:
                await ctx.send("Timed out :(")




        elif isinstance(msg, discord.Member):
            player = ""
            challenger = ""

            def check3(message):
                return message.author == ctx.author

            def check1(message):
                return message.author == ctx.author and str(message.channel.type) == "private"

            def check2(message):
                return message.author == msg and str(message.channel.type) == "private"

            if msg.bot:
                embed = discord.Embed(title=f"This is a bot.",
                                      description=f"I seriously don't know how you expect a bot to play oddeve with you WHEN IT CAN'T EVEN DM YOU BACK",
                                      color=discord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            if msg == ctx.author:
                embed = discord.Embed(title=f"Oh you lonely kid",
                                      description=f"If you got no friends to play with, try `{ctx.prefix}rock` or something",
                                      color=discord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            embed3 = discord.Embed(
                title=f"Hey {ctx.author.display_name}, as you have started the match, you get to choose....",
                description="Choose whether you want \"odd\" or \"even\"", color=discord.Color.random())
            await ctx.send(embed=embed3)
            try:
                reply3 = await self.bot.wait_for('message', check=check3, timeout=60)
                author_choice = reply3.content.lower()

                if author_choice == "odd" or author_choice == "o":
                    challenger = "odd"
                    player = "even"
                    await ctx.send(f"Alright you have chosen {challenger} so that makes {msg.display_name} {player}")

                elif author_choice == "even" or author_choice == "e":
                    challenger = "even"
                    player = "odd"
                    await ctx.send(f"Alright you have chosen {challenger} so that makes {msg.display_name} {player}")

                else:
                    embed = discord.Embed(
                        title="What the hell bruh",
                        description=f"You have managed to put an invalid option in odds n evens Its either odd or even :rolling_eyes:",
                        color=discord.Color.random())
                    embed.set_footer(text="Imagine having just 3 brain cells")
                    await ctx.send(embed=embed)
                    return
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

                reply1 = await self.bot.wait_for('message', check=check1, timeout=60)
                reply2 = await self.bot.wait_for('message', check=check2, timeout=60)
                playerno = int(reply2.content)
                challengerno = int(reply1.content)
                playerName = msg.name
                challengerName = ctx.author.name

                if playerno >= 10 or playerno < 0 or challengerno >= 10 or challengerno < 0:
                    await ctx.send(embed=discord.Embed(title="WHAT PART OF 0 TO 9 DO YOU NOT UNDERSTAND",
                                                       description="You ruined the game man",
                                                       color=discord.Color.random()))
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
                            embed=discord.Embed(title="Result Is even",
                                                description=f"{challengerName} wins! \n Poggers",
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

    @rps.error
    async def rps_error(self, ctx, error):
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
    async def oddeve_error(self, ctx, error):
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

    @guess.error
    async def guess_error(self, ctx, error):
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


def setup(bot):
    bot.add_cog(Games(bot))
