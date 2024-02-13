from discord.ext import commands


class CommandHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
