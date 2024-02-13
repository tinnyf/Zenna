import traceback

from discord import ui

class ProductSelect(ui.View):

    def __init__(self, products, display):
        self.products = products
        self.display = display
        super().__init__(timeout = None)
        pass

    @ui.button(emoji = '⬅️')
    async def previous(self, interaction, button:ui.Button):
        print("Button been pressed!")
        try:
            embed = self.display.previous()
            await interaction.response.edit_message(embed=embed)
        except Exception():
            print(traceback.format_exc())

    @ui.button(emoji= '➡️')
    async def next(self,interaction, button:ui.Button):
        try:
            print("Button been pressed!")
            embed = self.display.next()
            await interaction.response.edit_message(embed=embed)
        except Exception():
            print(traceback.format_exc())