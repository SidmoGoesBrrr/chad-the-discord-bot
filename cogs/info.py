import discord
import asyncio
from discord.ext import commands
import wikipedia
from modules import languages
from PyDictionary import PyDictionary
import requests
import urbandict
from googletrans import Translator, constants


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dictionary(self, ctx, *, keyword):
        dictionary = PyDictionary()

        def check(what_to_do):
            return ctx.author == what_to_do.author and what_to_do.channel == ctx.channel

        await ctx.send(embed=discord.Embed(title="What would you like to find?", color=discord.Color.random()))
        what_to_do = await self.bot.wait_for("message", check=check)

        try:
            if "meaning" in str(what_to_do.content).lower():
                try:
                    meaning = dictionary.meaning(keyword)
                    embed = discord.Embed(
                        title=f"The Meaning of {keyword}.", color=discord.Color.random())

                    if meaning.get('Noun') is not None:
                        for i in range(0, len(meaning['Noun'])):
                            embed.add_field(name=f"Meaning {i + 1}:", value=f"{(meaning['Noun'])[i]}",
                                            inline=False)
                    if meaning.get('Verb') is not None:
                        for i in range(0, len(meaning['Verb'])):
                            embed.add_field(name=f"Meaning {i + 1}:", value=f"{(meaning['Verb'])[i]}",
                                            inline=False)
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(embed=discord.Embed(title='Meaning not found', color=discord.Color.random()))

            if "synonym" in str(what_to_do.content).lower():
                try:
                    synonym_list = dictionary.synonym(keyword)
                    string = ""
                    for i in range(0, len(synonym_list)):
                        string += f"{i + 1}. {synonym_list[i]}\n"
                    embed = discord.Embed(
                        title=f"The Synonyms of {keyword}.", description=string, color=discord.Color.random())
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(embed=discord.Embed(title='Synonym not found', color=discord.Color.random()))

            if "antonym" in str(what_to_do.content).lower():
                try:
                    antonym_list = dictionary.antonym(keyword)
                    string = ""
                    for i in range(0, len(antonym_list)):
                        string += f"{i + 1}. {antonym_list[i]}\n"
                    embed = discord.Embed(
                        title=f"The Antonyms of the {keyword}.", description=string, color=discord.Color.random())
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(embed=discord.Embed(title='Antonym not found', color=discord.Color.random()))

        except:
            embed = discord.Embed(title="Error! Could not find")
            await ctx.send(embed=embed)

    @commands.command()
    async def translate(self, ctx, *, keyword):
        translator = Translator()
        def check(translate_to):
            return ctx.author == translate_to.author and translate_to.channel == ctx.channel

        await ctx.send(embed=discord.Embed(title="Choose your language"))
        translate_to = await self.bot.wait_for("message", check=check)
        translate_to = translate_to.content
        translate_to = languages.translate(str(translate_to))
        translation = translator.translate(keyword, dest=translate_to)
        if translate_to == "Undetected":
            embed = discord.Embed(
                title="Translate", description="This language is not supported by us.")
            embed.add_field(name="Possible Issues",
                            value=f"1. You have typed an invalid language.\n2. We don't support this language (if this is the case, come to our support server)")
        else:
            embed = discord.Embed(title="Translate",
                                  description=f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
        embed.color = discord.Color.random()

        await ctx.send(embed=embed)

    @commands.command()
    async def wiki(self,ctx, *, question):
        try:
            wiki = wikipedia.summary(question, 2)
            embed = discord.Embed(
                title="According to Wikipedia: ",
                description=f"{wiki}"
            )
            embed.set_footer(text="Information requested by: {}".format(
                ctx.author.display_name))
            embed.color = discord.Color.random()
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"Could not find wikipedia results for: {question}")

    @commands.command()
    async def weather(self,ctx, *, place):
        api_key = "6d7ac869f461ec0dc59fdf3a7da78262"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + place
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            current_temperature_kelvin = y["temp"]
            current_temperature_fahrenheit = round(
                (current_temperature_kelvin - 273.15) * 9 / 5 + 32)
            current_temperature_celsius = round(
                current_temperature_kelvin - 273.15)
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
            embed.set_footer(text="Information requested by: {}".format(
                ctx.author.display_name))
            embed.color = discord.Color.random()
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title=f"Sorry could not find the weather in {place}", color=discord.Color.dark_teal())
            await ctx.send(embed=embed)

    @commands.command()
    async def urban(self,ctx, *, keyword: str):
        try:
            list = (urbandict.define(keyword))
            embed = discord.Embed(
                title=f"Meaning of {keyword} in urban dict.", color=discord.Color.random())
            for i in range(0, len(list) - 1):
                embed.add_field(name=f"Type {i + 1}:",
                                value=f"Word: {(list[i])['word']}\n Definition: {(list[i])['def']}\n Examples: {(list[i])['example']}",
                                inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed=discord.Embed(title=f"Sorry mate i couldn't find sh*t for", description=f"```{keyword}```",
                                               color=discord.Color.random()))

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
def setup(bot):
    bot.add_cog(Info(bot))
