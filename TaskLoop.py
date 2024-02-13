import traceback

from discord.ext import commands, tasks

from ZatuWeb.NewReleaseData import NewReleaseData
from ZatuWeb.ProductDisplay import ProductDisplay
from ZatuWeb.ProductSelect import ProductSelect


class TaskLoop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild = 1078653950821158953
        self.channel = 1206761025131642900
        self.new_data = NewReleaseData()
        self.embed_sender.start()
        self.counter = 0

    @tasks.loop(hours = 1)
    async def embed_sender(self):
        self.counter = self.counter + 1
        print(f"Iteration {self.counter} of restart")
        try:
            print("Inside the Try block now!")
            products = self.new_data.get_new_products()
            print([self.new_data.get_title(product) for product in products])
            display = ProductDisplay(self.bot, products)
            print("boo!")
            print(display.get_embed())
            await self.bot.get_guild(self.guild).get_channel(self.channel).send(embeds=[display.get_embed()], view=ProductSelect(products, display))
            self.new_data.update_products()
        except Exception():
            print(traceback.format_exc())


    @embed_sender.before_loop
    async def before_sender(self):
        await self.bot.wait_until_ready()
        await self.embed_sender()