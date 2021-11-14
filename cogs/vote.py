import discord
import asyncio
import csv
from discord.ext import commands,tasks
from datetime import datetime
import pytz

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.checkVoteTime.start()
        self.member_update.start()

    @tasks.loop(seconds=20)  # repeat after every 20 seconds
    async def checkVoteTime(self):
        channel=self.bot.get_channel(880639248292798465)
        now = datetime.now()
        dt_string = now.strftime("%-H")
        if int(dt_string) == 15 or int(dt_string) == 3:
            vote=discord.Embed(title="This is your reminder",description="You better vote for me, here and now", color=discord.Color.random())
            vote.add_field(name="1",value = f"[top.gg](https://top.gg/bot/864010316424806451/vote)")
            vote.add_field(name="2",value = f"[discordbotlist.com](https://discordbotlist.com/bots/chad-6621/upvote)")
            vote.set_thumbnail(url="https://i.imgur.com/QICgRpf.png")
            await channel.send(embed=vote,content="<@&881209363077943326>")
            await asyncio.sleep(3600)


    @tasks.loop(seconds=20)  # repeat after every 20 seconds
    async def member_update(self):
        now = datetime.now()
        dt_string = now.strftime("%-H")
        if int(dt_string) == 12:
            date1 = datetime.strftime(datetime.now(), "%a, %d/%m/%Y")
            data = [date1, len(self.bot.users)]
            with open("databases/members.csv", 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)

            date2 = datetime.strftime(datetime.now(), "%a, %d/%m/%Y")
            data = [date2, len(self.bot.guilds)]
            with open("databases/servers.csv", 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)
            print("Cheese")
            await asyncio.sleep(3600)


def setup(bot):
    bot.add_cog(Vote(bot))
