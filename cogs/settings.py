import discord
import asyncio
from discord.ext import commands
from tinydb import TinyDB, Query

def checkping(guild_id_var):
    db = TinyDB('databases/pings.json')
    query = Query()
    values = str(list(map(lambda entry: entry["pingstate"],
                      db.search(query.guild_id == str(guild_id_var))))[0])
  
    return values.lower()


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def pingsettings(self,ctx, condition: str):
        db = TinyDB('databases/pings.json')
        query = Query()
        guild_id_var = ctx.message.guild.id
        if condition.lower() == "true":
            if checkping(guild_id_var) == 'true':
                await ctx.send("Already true idiot!")
            else:
                await ctx.send("Alright, i shall ping you!")
                try:
                    db.update({'pingstate': True}, query.guild_id == str(guild_id_var))
                except:
                    db.insert({'guild_id': str(guild_id_var), 'pingstate': True})

        elif condition.lower() == "false":
            if checkping(guild_id_var) == 'false':
                await ctx.send("Already False idiot.")
            else:

                await ctx.send("Alright, wont ping you again")
                try:
                    db.update({'pingstate': False}, query.guild_id == str(guild_id_var))
                except:
                    db.insert({'guild_id': str(guild_id_var), 'pingstate': False})


        else:
            await ctx.send("Invalid option shoo")



    @commands.command()
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
        db2 = TinyDB('databases/pings.json')
        query=Query()
        if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
            active_servers = bot.guilds
            guilds=[]
            for guild in active_servers:
                await ctx.send(f"{str(guild)} has {len(guild.members)} members")
                guild_id_var = guild.id

                if db2.search(query['guild_id'] == str(guild.id) == []):
                    pass
                else:
                    db2.insert({'guild_id': str(guild.id), 'pingstate': True})

        else:
            await ctx.send(embed=discord.Embed(title="Imagine trying to see stats of someone else's bot",color=discord.Color.random()))




def setup(bot):
    bot.add_cog(settings(bot))