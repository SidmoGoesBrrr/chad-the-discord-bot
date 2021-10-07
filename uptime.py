import discord, datetime, time
from discord.ext import commands

start_time = time.time()


class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=discord.Color.random())
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="Chad")
        try:
           # await ctx.send(embed=embed)
            await ctx.send(embed=discord.Embed(title=f"Chad has been online for:",description=f"{text}<a:zo_tick_anim:886924589546995803>",color=discord.Color.random()))
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)


def setup(bot):
    bot.add_cog(Uptime(bot))
