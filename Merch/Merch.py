import traceback

import discord

class Merch():


    def __init__(self, name, cost, query_str):
        self.name = name
        self.query_str = query_str
        self.cost = cost
        pass

    def return_string(self, interaction, code, user):
        if user.nick:
            name = user.nick
        else:
            name = user.display_name
        return(f"Hi {name}, thanks for being an active member of the Zatu community. Here's a code for your free {self.name}: {code}. \n \nJust add the item to your basket, along with a minimum spend of £{self.cost}, and insert the code into the coupon section at checkout. The cost of the item will be deducted from the total. \n \nHappy Gaming!")

    def return_embed(self, interaction, code, user):
        try:
            embed = discord.Embed(title = f"Here's your free {self.name}!")
            embed.description = (f"Hi {user.display_name}, thanks for being an active part of the Zatu community! To thank you, please accept this code: {code}. \n It will allow you to redeem a {self.name} on the Zatu site!")
            embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)
            embed.colour = discord.Color.from_str("#F47721")
            embed.set_footer(text = f"This code is redeemable with any order of at least £{self.cost}!")
            return embed
        except Exception:
            print(traceback.format_exc())