import asyncio

import discord
from discord.ext.commands import Bot

from AdminCommands import AdminCommands
from CommandHandler import CommandHandler
from TaskLoop import TaskLoop


class BotInit(Bot):
    def __init__(self, *, intents, application_id):
        super().__init__(command_prefix="~", intents=intents, application_id=application_id)
        with open("Secret.txt", 'r') as token_doc:
            self.token = token_doc.readline()

    async def setup_hook(self):
        print("setup_hook initiated!")
        await self.tree.sync()



    print("Bot online!")


intents = discord.Intents.all()

bot = BotInit(intents=intents, application_id=1205105813111181372)


async def main(bot):
    await cogloader(bot)

    async with bot:
        await bot.start(bot.token)


async def cogloader(bot):
    await bot.add_cog(AdminCommands(bot))
    await bot.add_cog(CommandHandler(bot))
    await bot.add_cog(TaskLoop(bot))


asyncio.run(main(bot))
