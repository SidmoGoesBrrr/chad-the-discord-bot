import discord
import asyncio
from discord.ext import commands,tasks
from tinydb import TinyDB, Query
from datetime import datetime

def checkping(guild_id_var):
    db = TinyDB('databases/pings.json')
    query = Query()
    values = str(list(map(lambda entry: entry["pingstate"],
                      db.search(query.guild_id == str(guild_id_var))))[0])
  
    return values.lower()


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['pingset', 'pset', 'pings', 'ps'])
    async def pingsettings(self,ctx, condition: str):
        db = TinyDB('databases/pings.json')
        query = Query()
        guild_id_var = ctx.message.guild.id
        if condition.lower() == "true":
            if checkping(guild_id_var) == 'true':
                await ctx.send(embed=discord.Embed(title="Already true idiot!", color=discord.Color.random()))
            else:
                await ctx.send(embed=discord.Embed(title="Alright, I now have permission!", description="I shall ping you as and when it is required.", color=discord.Color.random()))
                try:
                    db.update({'pingstate': True}, query.guild_id == str(guild_id_var))
                except:
                    db.insert({'guild_id': str(guild_id_var), 'pingstate': True})

        elif condition.lower() == "false":
            if checkping(guild_id_var) == 'false':
                await ctx.send(embed=discord.Embed(title="Already False idiot.", color=discord.Color.random()))
            else:

                await ctx.send(embed=discord.Embed(title="Alright, I don't have permission anymore", description="I will not ping you again.", color=discord.Color.random()))
                try:
                    db.update({'pingstate': False}, query.guild_id == str(guild_id_var))
                except:
                    db.insert({'guild_id': str(guild_id_var), 'pingstate': False})


        else:
            await ctx.send(embed=discord.Embed(title="Shoo silly child", description="Invalid option", color=discord.Color.random()))


    @commands.command(aliases=['pref', 'pre', 'pr'])
    async def prefix(self,ctx, *, prefix=None):
        if ctx.author.guild_permissions.administrator:
            db = TinyDB('databases/prefix.json')
            query = Query()
            guild_id_var = ctx.guild.id
            if prefix is None:
                await ctx.send(embed=discord.Embed(title=f"My prefix is `{ctx.prefix}`"))

            else:
                if db.search(query.guild_id == str(guild_id_var)):
                    db.update({'prefix': prefix}, query.guild_id == str(guild_id_var))
                    await ctx.send(embed=discord.Embed(title=f"Updated prefix of \"{ctx.guild.name}\" to {prefix}"))
                else:
                    db.insert({'guild_id': str(guild_id_var), 'prefix': str(prefix)})
                    await ctx.send(embed=discord.Embed(title=f"Changed prefix of \"{ctx.guild.name}\" to {prefix}"))

        else:
            embed = discord.Embed(title="Hold up",
                                description="You can't do that, your not an admin!",
                                color=discord.Color.red())
            await ctx.send(embed=embed)




    @commands.command()
    async def stats(self,ctx):
        if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
            active_servers = self.bot.guilds
            for guild in active_servers:
                await ctx.send(f"{str(guild)} has {len(guild.members)} members")
                
        else:
            await ctx.send(embed=discord.Embed(title="Imagine trying to see stats of someone else's bot",color=discord.Color.random()))

    @commands.command(aliases=["voteremind","remindvote"])
    async def votereminder(self, ctx):
        if ctx.guild.id != 869173101131337748:
            await ctx.send(embed=discord.Embed(title=f"{ctx.author.name} You are an idiot. ",description="I do this only [here](https://discord.gg/h3Mg4CD7)",color=discord.Color.random()))
        role = discord.utils.find(lambda r: r.name == 'voteping', ctx.message.guild.roles)
        await ctx.author.add_roles(role)
        await ctx.send(embed=discord.Embed(title=f"Ok {ctx.author.name}. I shall remind you to vote for me every 12 hours!",description="Forgetful boi",color=discord.Color.random()))
        

    

def setup(bot):
    bot.add_cog(settings(bot))