import discord
import asyncio
from discord.ext import commands
import random
import os
import giphy_client
from giphy_client.rest import ApiException
import datetime
import pyfiglet
from tinydb import TinyDB, Query
from modules import encrypt as enc, decrypt as dec
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import time
from discord.utils import get
import re
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

def checkping(guild_id_var):
    db = TinyDB('databases/pings.json')
    query = Query()
    values = str(list(map(lambda entry: entry["pingstate"],
                      db.search(query.guild_id == str(guild_id_var))))[0])
  
    return values.lower()

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def ask(self,ctx, *, question):
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


    @commands.command()
    async def gif(self,ctx, *, q="random"):

        api_key = os.environ['giphy_api']
        api_instance = giphy_client.DefaultApi()
        try: 
        # Search Endpoint
            
            api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
            lst = list(api_response.data)
            giff = random.choice(lst)

            emb = discord.Embed(title=q)
            emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            emb.color=discord.Color.random()

            await ctx.channel.send(embed=emb)
        except ApiException as e:
            emb = discord.Embed(title=q,description="Sorry could not find anything matching that",color=discord.Color.random())
            await(ctx.send(embed=emb))


    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command()
    async def repeat(self,ctx, times, *, msg):
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


    @commands.command()
    async def dice(self,ctx):
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


    @commands.command()
    async def epicgamerrate(self,ctx, member: discord.Member = None):
        num = random.randint(1, 100)
        if member is None:
            member = ctx.author

        if checkping(ctx.message.guild.id)=='true':

            membervar=member.mention

        else:
            membervar=member.display_name


        embed = discord.Embed(
            title=f"Epic Gamer Rate :sunglasses:",
            description=f"{membervar} is {num}% epic gamer."
        )
        embed.color = discord.Color.random()
        embed.set_footer(text="Gamers = Poggers")
        await ctx.send(embed=embed)


    @commands.command()
    async def simprate(self,ctx, member: discord.Member = None):
        num = random.randint(1, 100)
        if member is None:
            member = ctx.author

        if checkping(ctx.message.guild.id)=='true':
            membervar=member.mention

        else:
            membervar=member.display_name

            
        embed = discord.Embed(
            title=f"Simp Rate :blush:",
            description=f"{membervar} is {num}% simp."
        )
        embed.color = discord.Color.random()
        embed.set_footer(text="Their favourite show be the SIMPsons")
        await ctx.send(embed=embed)


    @commands.command()
    async def poll(self,ctx, duration: TimeConverter, *, argument: str):
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
                description=description, color=discord.Color.random()
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
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=1.0, check=check)
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

    
    @commands.command()
    async def ascii(self,ctx, *, txt: str):
        txt = await commands.clean_content().convert(ctx, txt)
        split_text = txt.split(' ', maxsplit=1)
        if split_text[0].lower() == 'remove':
            await ctx.message.delete()
        else:
            result = pyfiglet.figlet_format(txt)
        await ctx.send("```" + result + "```")


    @commands.command()
    async def act(self,ctx, member: discord.Member, *, message=None):
        
            if message == None:
                await ctx.send(embed=discord.Embed(title= f'Please provide a message with that!',color=discord.Color.random()))
                return

            if '@' in str(message):
                await ctx.send(embed=discord.Embed(title=f"Imagine exploiting the act command like dis...\nNo pinging anyone please", color=discord.Color.random()))
                return

            
            try:
                await ctx.message.delete()
                webhook = await ctx.channel.create_webhook(name=member.name)
                await webhook.send(
                    message, username=member.display_name, avatar_url=member.avatar_url
                    )
                webhooks = await ctx.channel.webhooks()
                for webhook in webhooks:
                        try:
                            await webhook.delete()
                        except:
                            print("Cant delete 'hook'")
            except discord.errors.HTTPException:

                await ctx.send("Ouch! I'm sorry but max webhooks reached. I can't do the act command!")

            except discord.errors.Forbidden:
                await ctx.send("Ouch! I'm sorry but I got no perms. I can't do the act command!")


    @commands.command()
    async def encrypt(self,ctx, *, text_to_encrypt: str):
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

        await self.bot.wait_for('reaction_add', check=check)

        await message.delete()


    @commands.command()
    async def decrypt(self,ctx, *, text_to_decrypt: str):
        embed = discord.Embed(title="Decoding your message <a:zo_typing:873129455483256832>",
                            description="This is your message. :face_with_monocle:\n Hope you have what you need. :slight_smile:")
        embed.color = discord.Color.dark_blue()

        embed.add_field(name="Encrypted Text", value='```' + dec.decrypt_text(text_to_decrypt) + '```')
        message = await ctx.send(embed=embed)
        await message.add_reaction('<:trash:867001275634417714>')

        def check(reaction, user):
            return reaction.message == message and str(
                reaction.emoji) == '<:trash:867001275634417714>' and user == ctx.author

        await self.bot.wait_for('reaction_add', check=check)
        await message.delete()




    @commands.command()
    async def binary(self,ctx, *, string: str):
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


    @commands.command()
    async def choose(self,ctx, *choices: str):
        embed = discord.Embed(
            title=f"I choose...",
            description=f"{random.choice(choices)}"
        )
        embed.color = discord.Color.random()
        embed.set_footer(
            text=f"It is better and I am awesome")
        await ctx.send(embed=embed)


    @commands.command()
    async def coinflip(self,ctx, *, option=None):
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
                embed.color = discord.Color.random()

            elif boolean is True:
                embed = discord.Embed(
                    title=f"{result}",
                    description=f"Please enter either heads or tails next time. \nIt was {r}."
                )
                embed.color = discord.Color.random()
        else:
            embed = discord.Embed(
                title=f"Your kidding. :angry:",
                description="You gotta choose an option. \nIf you don't wanna play then go away.\n Don't bother me.",
            )
            embed.color = discord.Color.random()
            embed.set_footer(text=f"The Freeloaders are here")

        await ctx.send(embed=embed)


    @commands.command()
    async def hack(self,ctx, member: discord.User):
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


        
    @commands.command()
    async def imagememes(self,ctx):
        embed = discord.Embed(title="Image Memes List",
                            description="Here is the list of POG image memes you can use.",
                            inline=False)
        embed.add_field(name="List", value=f"1. {ctx.prefix}worthless\n2. {ctx.prefix}wanted\n3. {ctx.prefix}rip\n4. {ctx.prefix}chad")
        await ctx.send(embed=embed)


    @commands.command()
    async def worthless(self,ctx, *, worthless_text):
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


    @commands.command()
    async def wanted(self,ctx, user: discord.Member = None):
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


    @commands.command()
    async def rip(self,ctx, user: discord.Member = None):
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


    @commands.command()
    async def chad(self,ctx, user: discord.Member = None):
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
    
    @commands.command()
    async def vcmeme(self,ctx, *, meme: str):
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
    async def vcmeme_error(self,ctx, error):
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

    @commands.command()
    async def quote(self,ctx, quoter, *, quote):
        embed = discord.Embed(
            description=f"\"*{quote}*\""
        )
        embed.color = discord.Color.random()
        quote = await commands.clean_content().convert(ctx, quoter)
        embed.set_footer(text=f"- {quote.replace('@', '')}")
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Fun(bot))