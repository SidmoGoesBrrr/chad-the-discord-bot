import os
import os
import discord
from discord.ext import commands
from discord_components import Button
from discord_components import *
import math
import wolframalpha
from modules import calculation_filter as cf
import os


class Nerd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, *, arguments=""):
        if arguments == "":
            await ctx.send(embed=discord.Embed(title=f"Not this again",
                                               description=f"I need numbers to add and not thin air!",
                                               color=discord.Color.random()))
            return
        split = arguments.split(' ')
        if len(split) == 1:
            await ctx.send(embed=discord.Embed(title=f"To add numbers,",
                                               description=f"you need number**s**\nEmphasis on the 's'",
                                               color=discord.Color.random()))
            return
        if len(split) > 10:
            await ctx.send(embed=discord.Embed(title=f"I shall not add these many numbers",
                                               description=f"My limit is not more than 10 numbers at a time.\nCause I have better things to do.",
                                               color=discord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '+')
        if ans is None:
            return
        string = split[0]
        count = True
        for i in split:
            if count is True:
                count = False
                continue
            string = string + " + " + i
        embed = discord.Embed(title=str(ans),
                              description=f"This is the answer to {string}.",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['subs'])
    async def subtract(self, ctx, *, arguments=""):
        if arguments == "":
            await ctx.send(embed=discord.Embed(title=f"Not this again again",
                                               description=f"I need numbers to subtract and not thin air!",
                                               color=discord.Color.random()))
            return
        split = arguments.split(' ')
        if len(split) == 1:
            embed = discord.Embed(title=f"To subtract numbers,",
                                  description=f"you need number**s**\nEmphasis on the 's'",
                                  color=discord.Color.random())
            embed.set_footer(text="And I thought you would have learned by now.")
            await ctx.send(embed=embed)
            return
        elif len(split) > 2:
            await ctx.send(embed=discord.Embed(title=f"What you ask is just not possible",
                                               description=f"I just can't subtract {len(split)} numbers from each other!",
                                               color=discord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '-')
        if ans is None:
            return
        embed = discord.Embed(title=str(ans),
                              description=f"This is the answer to {split[0]} - {split[1]}.",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['multi'])
    async def multiply(self, ctx, *, arguments=""):
        if arguments == "":
            await ctx.send(embed=discord.Embed(title=f"Not this again again again",
                                               description=f"I need numbers to multiply and not thin air!",
                                               color=discord.Color.random()))
            return
        split = arguments.split(' ')
        if len(split) == 1:
            await ctx.send(embed=discord.Embed(title=f"To multiply numbers,",
                                               description=f"you need number**s**\nEmphasis on the 's'",
                                               color=discord.Color.random()))
            return
        if len(split) > 10:
            await ctx.send(embed=discord.Embed(title=f"I shall not multiply these many numbers",
                                               description=f"My limit is not more than 10 numbers at a time.\nCause I have better things to do.",
                                               color=discord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '*')
        if ans is None:
            return
        string = split[0]
        count = True
        for i in split:
            if count is True:
                count = False
                continue
            string = string + " * " + i
        embed = discord.Embed(title=str(ans),
                              description=f"This is the answer to {string}.",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['div'])
    async def divide(self, ctx, *, arguments=""):
        if arguments == "":
            await ctx.send(embed=discord.Embed(title=f"Not this again again again again",
                                               description=f"I need numbers to divide and not thin air!\nIs this starting to get old?",
                                               color=discord.Color.random()))
            return
        split = arguments.split(' ')
        if len(split) == 1:
            embed = discord.Embed(title=f"To divide numbers,",
                                  description=f"you need number**s**\nEmphasis on the 's'",
                                  color=discord.Color.random())
            embed.set_footer(text="And I thought you would have learned by now.")
            await ctx.send(embed=embed)
            return
        elif len(split) > 2:
            await ctx.send(embed=discord.Embed(title=f"What you ask is just not possible",
                                               description=f"I just can't divide {len(split)} numbers from each other!",
                                               color=discord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '/')
        if ans is None:
            return
        embed = discord.Embed(title=str(ans),
                              description=f"This is the answer to {split[0]} / {split[1]}.",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['peri'])
    async def perimeter(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        await ctx.send(
            "Please choose one of the following options",
            components=[
                Button(style=ButtonStyle.blue, label="Circle"),
                Button(style=ButtonStyle.red, label="Triangle"),
                Button(style=ButtonStyle.green, label="Quadrilateral")
            ]
        )

        response = await self.bot.wait_for("button_click", check=check)
        await ctx.channel.send(f"You have clicked on {response.component.label}")
        if response.component.label == "Circle":
            await ctx.send("Please enter the radius")
            r = await self.bot.wait_for("message", check=check)
            if r.mentions:
                await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                   description=f"That a circle have a mention as a radius?",
                                                   color=discord.Color.random()))
                return
            r = r.content
            for i in r:
                if not i.isdigit() and i != ".":
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a circle can have a radius {r}?\nThe '{i}' there makes it useless",
                                                       color=discord.Color.random()))
                    return
            perimeter = round((2 * 22 * float(r)) / 7, 3)
            if perimeter.is_integer() is True:
                perimeter = int(perimeter)
            embed = discord.Embed(title=f"{perimeter}",
                                  description=f"Is the perimeter of a circle with radius {r}\nDid you know that a perimeter of a circle is the same as its circumference?",
                                  color=discord.Color.random())
            embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif response.component.label == "Triangle":
            await ctx.send(
                "Please choose the type of triangle you want to use",
                components=[
                    Button(style=ButtonStyle.blue, label="Equilateral Triangle"),
                    Button(style=ButtonStyle.red, label="Isosceles Triangle"),
                    Button(style=ButtonStyle.green, label="Scalene Triangle")
                ]
            )
            response = await self.bot.wait_for("button_click", check=check)
            await ctx.channel.send(f"You have clicked on {response.component.label}")
            if response.component.label == "Equilateral Triangle":
                await ctx.send("Please enter the length of the side of the triangle.")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a triangle have a mention as a side?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a triangle can have a side {s}?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                perimeter = round(3 * float(s), 3)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = discord.Embed(title=f"{perimeter}",
                                      description=f"Is the perimeter of an equilateral triangle with side {s}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Isosceles Triangle":
                await ctx.send(
                    "Please enter the equal and the non-equal sides in this format\n`<equalside> <non-equalside>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a triangle can have a mention as one of its SIDES?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                e = split[0]
                n = split[1]
                perimeter = (2 * float(e)) + float(n)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = discord.Embed(title=f"{perimeter}",
                                      description=f"Is the perimeter of an isosceles triangle with equal sides of length {e} and a non-equal side of length {n}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Scalene Triangle":
                await ctx.send("Please enter the three sides in this format\n`<side1> <side2> <side3>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a triangle can have a mention as one of its SIDES?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 3:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only three numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                s1 = split[0]
                s2 = split[1]
                s3 = split[2]
                perimeter = float(s1) + float(s2) + float(s3)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = discord.Embed(title=f"{perimeter}",
                                      description=f"Is the perimeter of a scalene triangle with sides of length {s1}, {s2} and {s3}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

        elif response.component.label == "Quadrilateral":
            await ctx.send(
                "Please choose the type of quadrilateral you want to use",
                components=[
                    Button(style=ButtonStyle.blue, label="Parallelogram/Rectangle"),
                    Button(style=ButtonStyle.red, label="Rhombus/Square"),
                    Button(style=ButtonStyle.green, label="Irregular Quadrilateral")
                ]
            )
            response = await self.bot.wait_for("button_click", check=check)
            await ctx.channel.send(f"You have clicked on {response.component.label}")
            if response.component.label == "Parallelogram/Rectangle":
                await ctx.send(
                    "Please enter the two sets of opposite sides in this format\n`<oppositeside1> <oppositeside2>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a parallelogram or a rectangle can have a mention as one of its SIDES?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a parallelogram or a rectangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                os1 = split[0]
                os2 = split[1]
                perimeter = 2 * (float(os1) + float(os2))
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = discord.Embed(title=f"{perimeter}",
                                      description=f"Is the perimeter of a parallelogram or a rectangle with opposite sides of length {os1} and {os2}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Rhombus/Square":
                await ctx.send("Please enter the side of the rhombus or square")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a rhombus or square have a mention as a side?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a That a rhombus or square can have a side {s}?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                perimeter = 4 * float(s)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = discord.Embed(title=f"{perimeter}",
                                      description=f"Is the perimeter of a rhombus or square with side {s}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Irregular Quadrilateral":
                await ctx.send(
                    "Please enter the sides of the quadrilateral in this format\n`<side1> <side2> <side3> <side4>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a quadrilateral can have a mention as one of its SIDES?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a quadrilateral can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 4:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only four numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                s1 = split[0]
                s2 = split[1]
                s3 = split[2]
                s4 = split[3]
                perimeter = float(s1) + float(s2) + float(s3) + float(s4)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = discord.Embed(title=f"{perimeter}",
                                      description=f"Is the perimeter of an irregular quadrilateral with sides {s1}, {s2}, {s3} and {s4}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command()
    async def area(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        await ctx.send(
            "Please choose one of the following options",
            components=[
                Button(style=ButtonStyle.blue, label="Circle"),
                Button(style=ButtonStyle.red, label="Triangle"),
                Button(style=ButtonStyle.green, label="Quadrilateral")
            ]
        )

        response = await self.bot.wait_for("button_click", check=check)
        await ctx.channel.send(f"You have clicked on {response.component.label}")
        if response.component.label == "Circle":
            await ctx.send("Please enter the radius")
            r = await self.bot.wait_for("message", check=check)
            if r.mentions:
                await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                   description=f"That a circle have a mention as a radius?",
                                                   color=discord.Color.random()))
                return
            r = r.content
            for i in r:
                if not i.isdigit() and i != ".":
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a circle can have a radius {r}?\nThe '{i}' there makes it useless",
                                                       color=discord.Color.random()))
                    return
            area = round(22 * float(r) * float(r) / 7, 3)
            if area.is_integer() is True:
                area = int(area)
            embed = discord.Embed(title=f"{area}",
                                  description=f"Is the area of a circle with radius {r}",
                                  color=discord.Color.random())
            embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif response.component.label == "Triangle":
            await ctx.send(
                "Please choose the type of triangle you want to use",
                components=[
                    Button(style=ButtonStyle.blue, label="Equilateral Triangle"),
                    Button(style=ButtonStyle.red, label="Isosceles Triangle"),
                    Button(style=ButtonStyle.green, label="Scalene Triangle"),
                    Button(style=ButtonStyle.grey, label="Right-Angled Triangle")
                ]
            )
            response = await self.bot.wait_for("button_click", check=check)
            await ctx.channel.send(f"You have clicked on {response.component.label}")
            if response.component.label == "Equilateral Triangle":
                await ctx.send("Please enter the length of the side of the triangle.")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a triangle have a mention as a side?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a triangle can have a side {s}?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                area = round(math.sqrt(3) * float(s) * float(s) / 4, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = discord.Embed(title=f"{area}",
                                      description=f"Is the area of an equilateral triangle with side {s}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Isosceles Triangle":
                await ctx.send(
                    "Please enter the equal and the non-equal sides in this format\n`<equalside> <non-equalside>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a triangle can have a mention as one of its SIDES?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                e = split[0]
                n = split[1]
                area = round(float(n) * (math.sqrt(math.pow(float(e), 2) - (math.pow(float(e), 2) / 4))) / 2, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = discord.Embed(title=f"{area}",
                                      description=f"Is the area of an isosceles triangle with equal sides of length {e} and a non-equal side of length {n}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Scalene Triangle":
                await ctx.send("Please enter the three sides in this format\n`<side1> <side2> <side3>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a triangle can have a mention as one of its SIDES?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 3:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only three numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                s1 = split[0]
                s2 = split[1]
                s3 = split[2]
                s_heron = float(s1) + float(s2) + float(s3)
                area = round(math.sqrt(s_heron * (s_heron - float(s1)) * (s_heron - float(s2)) * (s_heron - float(s3))),
                             3)
                if area.is_integer() is True:
                    area = int(area)
                embed = discord.Embed(title=f"{area}",
                                      description=f"Is the area of a scalene triangle with sides of length {s1}, {s2} and {s3}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Right-Angled Triangle":
                await ctx.send("Please enter the two sides other then the hypotenuse.\n`<side1> <side2>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a triangle can have a mention as one of its SIDES?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                b = split[0]
                h = split[1]
                area = round((float(b) * float(h)) / 2, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = discord.Embed(title=f"{area}",
                                      description=f"Is the area of an isosceles triangle with the sides {b} and {h}, as long as they aren't the hypotenuses of the triangle!",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

        elif response.component.label == "Quadrilateral":
            await ctx.send(
                "Please choose the type of quadrilateral you want to use",
                components=[
                    Button(style=ButtonStyle.blue, label="Parallelogram"),
                    Button(style=ButtonStyle.red, label="Rectangle"),
                    Button(style=ButtonStyle.green, label="Rhombus"),
                    Button(style=ButtonStyle.gray, label="Square"),
                    Button(style=ButtonStyle.blue, label="Trapezium")
                ]
            )
            response = await self.bot.wait_for("button_click", check=check)
            await ctx.channel.send(f"You have clicked on {response.component.label}")
            if response.component.label == "Parallelogram":
                await ctx.send("Please enter the base and height of the parallelogram.\n`<base> <height>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a parallelogram can have a mention as one of its SIDES?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a parallelogram can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                b = split[0]
                h = split[1]
                area = float(b) * float(h)
                if area.is_integer() is True:
                    area = int(area)
                embed = discord.Embed(title=f"{area}",
                                      description=f"Is the area of an parallelogram with opposite sides of length {b} and {h}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Rectangle":
                await ctx.send("Please enter the length and breadth of the rectangle.\n`<length> <breadth>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a rectangle can have a mention as one of its SIDES?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a rectangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                l = split[0]
                b = split[1]
                area = float(l) * float(b)
                if area.is_integer() is True:
                    area = int(area)
                embed = discord.Embed(title=f"{area}",
                                      description=f"Is the area of an rectangle with opposite sides of length {l} and {b}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Rhombus":
                await ctx.send("Please enter the diagonals of the rhombus in this format\n`<diagonal1> <diagonal2>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a rhombus have a mention as a side?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a rhombus can have a side {s}?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                d1 = split[0]
                d2 = split[1]
                area = float(d1) * float(d2)
                if area.is_integer() is True:
                    area = int(area)
                embed = discord.Embed(title=f"{area}",
                                      description=f"Is the area of a rhombus with  diagonals {d1} and {d2}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Square":
                await ctx.send("Please enter the side of the square")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a square have a mention as a side?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a square can have a side {s}?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                area = math.pow(float(s), 2)
                if area.is_integer() is True:
                    area = int(area)
                embed = discord.Embed(title=f"{area}",
                                      description=f"Is the area of a square with side {s}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            elif response.component.label == "Trapezium":
                await ctx.send(
                    "Please enter the unequal sides of the trapezium, along with its height(altitude), in this format\n`<unequalside1> <unequalside2> <height/altitude>`")
                s = await self.bot.wait_for("message", check=check)
                if s.mentions:
                    await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                       description=f"That a trapezium can have a mention as one of its dimensions?",
                                                       color=discord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=discord.Embed(title=f"Why do you think",
                                                           description=f"That a trapezium can have {s} as one of its DIMENSIONS?\nThe '{i}' there makes it useless",
                                                           color=discord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 3:
                    await ctx.send(embed=discord.Embed(
                        title=f"Only three numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=discord.Color.random()))
                    return
                a = split[0]
                b = split[1]
                h = split[2]
                area = round(((float(a) + float(b)) * float(h)) / 2, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = discord.Embed(title=f"{area}",
                                      description=f"Is the area of a trapezium with unequal sides of length {a}, {b} and height of length{h}",
                                      color=discord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(aliases=['aaq'])
    async def question(self, ctx, *, question=""):

        if question == "":
            await ctx.send(embed=discord.Embed(title=f"You need to ASK something.",
                                               description=f"So that I can ANSWER it.\nIf you genuinely didn't think of this, then use !roast to see what I'm thinking.",
                                               color=discord.Color.random()))
        app_id = os.getenv("wolfy_lmao")
        client = wolframalpha.Client(app_id)

        res = client.query(question)

        try:

            answer = next(res.results).text
            await ctx.send(embed=discord.Embed(description=f"{answer}",
                                               color=discord.Color.random()))

        except:
            await ctx.send(
                embed=discord.Embed(title=f"Couldn't find sh*t for {question}", color=discord.Color.random()))

    @commands.command(aliases=['sq'])
    async def square(self, ctx, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="2", power_or_root="power")
        power = 2
        if ans is None:
            return
        embed = discord.Embed(title=f"{ans}",
                              description=f"Is the square of {number}.",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cb'])
    async def cube(self, ctx, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="3", power_or_root="power")
        power = 3
        if ans is None:
            return
        embed = discord.Embed(title=f"{ans}",
                              description=f"Is the cube of {number}.",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sqrt'])
    async def squareroot(self, ctx, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="2", power_or_root="root")
        power = 2
        if ans is None:
            return
        embed = discord.Embed(title=f"{ans}",
                              description=f"Is the square root of {number}.",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cbrt'])
    async def cuberoot(self, ctx, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="3", power_or_root="root")
        power = 3
        if ans is None:
            return
        embed = discord.Embed(title=f"{ans}",
                              description=f"Is the cube root of {number}",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pow'])
    async def power(self, ctx, number="", power=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power=power, power_or_root="power")
        if ans is None:
            return
        embed = discord.Embed(title=f"{ans}",
                              description=f"Is the value of {number} to the power {power}",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def root(self, ctx, number="", power=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power=power, power_or_root="root")
        if ans is None:
            return
        embed = discord.Embed(title=f"{ans}",
                              description=f"Is the value of root {power} of {number}",
                              color=discord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def trig(self, ctx):
        string = "sin A = Perpendicular/Hypotenuse\ncos A = Base/Hypotenuse\ntan A = Perpendicular/Base\nsec A = Hypotenuse/Base\ncosec A = Hypotenuse/Perpendicular\ncot A = Base/Perpendicular"
        embed = discord.Embed(title=f"Trignometric values are as follows:",
                              description=f"{string}",
                              color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(aliases=['sine'])
    async def sin(self, ctx):
        embed = discord.Embed(title=f"Info on the trignometric value 'sin'",
                              color=discord.Color.random())
        embed.add_field(name="Full Form:", value="sine", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Perpendicular/Hypotenuse", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="sin A = 1/cosec A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="sin² A = 1 - cos² A", inline=False)
        embed.add_field(name="Relation to Other Trignometric Function:",
                        value="sin A = tan A cos A\nsin A = cos A/cot A\nsin A = tan A/ sec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cosine'])
    async def cos(self, ctx):
        embed = discord.Embed(title=f"Info on the trignometric value 'cos'",
                              color=discord.Color.random())
        embed.add_field(name="Full Form:", value="cosine", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Base/Hypotenuse", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="cos A = 1/sec A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="cos² A = 1 - sin² A", inline=False)
        embed.add_field(name="Relation to Other Trignometric Function:",
                        value="cos A=sin A cot A\ncos A = sin A/tan A\ncos A = cot A/ sec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['tangent'])
    async def tan(self, ctx):
        embed = discord.Embed(title=f"Info on the trignometric value 'tan'",
                              color=discord.Color.random())
        embed.add_field(name="Full Form:", value="tangent", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Perpendicular/Base", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="tan A = 1/cot A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="tan² A = sec² A - 1 ", inline=False)
        embed.add_field(name="Relation to Other Trignometric Function:",
                        value="tan A = sin A sec A\ntan A = sin A/cos A\ntan A = sec A/ cosec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['secant'])
    async def sec(self, ctx):
        embed = discord.Embed(title=f"Info on the trignometric value 'sec'",
                              color=discord.Color.random())
        embed.add_field(name="Full Form:", value="secant", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Hypotenuse/Base", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="sec A = 1/cos A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="sec² A = 1 + tan² A", inline=False)
        embed.add_field(name="Relation to Other Trignometric Function:",
                        value="sec A=sin A cot A\nsec A = cot A/cosec A\nsec A = cos A/ tan A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cosecant'])
    async def cosec(self, ctx):
        embed = discord.Embed(title=f"Info on the trignometric value 'cosec'",
                              color=discord.Color.random())
        embed.add_field(name="Full Form:", value="cosecant", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Hypotenuse/Perpendicular", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="cosec A = 1/sin A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="cosec² A = 1 + cot² A", inline=False)
        embed.add_field(name="Relation to Other Trignometric Function:",
                        value="cosec A = tan A cos A\ncosec A = tan A/sec A\ncosec A = cos A/ cot A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cotan', 'cotangent'])
    async def cot(self, ctx):
        embed = discord.Embed(title=f"Info on the trignometric value 'cot'",
                              color=discord.Color.random())
        embed.add_field(name="Full Form:", value="cotangent", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Base/Perpendicular", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="cot A = 1/tan A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="cot² A = cosec² A - 1", inline=False)
        embed.add_field(name="Relation to Other Trignometric Function:",
                        value="cot A = cos A cosec A\ncot A = cos A/sin A\ncot A = cosec A/ sec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Nerd(bot))
