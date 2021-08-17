import logging
from traceback import format_exception
from tinydb import TinyDB, Query
import discord
from discord.ext import commands

def checkping(guild_id_var):
    db = TinyDB('databases/pings.json')
    query = Query()
    values = str(list(map(lambda entry: entry["pingstate"],
                          db.search(query.guild_id == str(guild_id_var))))[0])

    return values.lower()


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)


    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):

        if hasattr(ctx.command, 'on_error'):
            return


        if isinstance(err, commands.ConversionError):
            await ctx.send(err)

        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: `{err.param}`")

        elif isinstance(err, commands.BadArgument):
            await ctx.send(err)

        elif isinstance(err, commands.ArgumentParsingError):
            await ctx.send(err)

        elif isinstance(err, commands.PrivateMessageOnly):
            await ctx.send("This command can only be used in DMs.")

        elif isinstance(err, commands.NoPrivateMessage):
            await ctx.send("This command can only be used in Guilds.")

        elif isinstance(err, commands.MissingPermissions):
            perms = ", ".join(
                f"`{perm.replace('_', ' ').title()}`" for perm in err.missing_perms
            )

            await ctx.send(f"You're missing the permissions: {perms}")

        elif isinstance(err, commands.BotMissingPermissions):
            perms = ", ".join(
                f"`{perm.replace('_', ' ').title()}`" for perm in err.missing_perms
            )

            await ctx.send(f"I'm missing the permissions: {perms}")

        elif isinstance(err, commands.DisabledCommand):
            await ctx.send(f"`{ctx.command.qualified_name}` is currently disabled.")

        elif isinstance(err, discord.HTTPException):
            await ctx.send(
                "An error occurred while I was trying to execute a task. Are you sure I have the correct permissions?"
            )

        elif isinstance(err, commands.MaxConcurrencyReached):
            await ctx.send(
                f"`{ctx.command.qualified_name}` can only be used {err.number} command at a time under {str(err.per)}"
            )

        self.logger.error("".join(format_exception(err, err, err.__traceback__)))


def setup(bot):
    bot.add_cog(Errors(bot))