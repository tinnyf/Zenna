import datetime
import traceback
import re

import discord
from discord import app_commands
from discord.ext import commands

from GoogleSheets import GoogleSheets
from Merch.Meeples import ZedMeeples
from Merch.CardsPin import CardsPin
from Merch.Dice import Dice
from Merch.DiceTower import DiceTower
from Merch.DiceTray import DiceTray
from Merch.ZedPin import ZedPin
from ZatuWeb.ProductDisplay import ProductDisplay
from ZatuWeb.ProductSelect import ProductSelect
from ZatuWeb.WebData import WebData


class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.google_sheets = GoogleSheets()
        self.bot = bot
        self.bot.add_listener(self.on_message, "on_message")

    def get_merch(self):
        bindings ={
            "Dice" : Dice,
            "Dice Tray" : DiceTray,
            "Dice Tower": DiceTower,
            "Zed Pin": ZedPin,
            "Cards Pin": CardsPin,
            "Zed Meeples": ZedMeeples,
        }
        return bindings

    async def guild_check(self, interaction):
        if not (interaction.guild.id == 1078653950821158953 or interaction.guild.id == 1135877150155755555):
            print("This bot is being used in an illegal guild")
            return False
        else:
            return True
    @app_commands.default_permissions(manage_messages = True)
    @app_commands.command(name = "freebies")
    async def merch(self, interaction, item: str, user:discord.Member):
        try:
            if not await self.guild_check(interaction):
                return False
            channel = interaction.channel
            code, cell = self.get_item_code(item)
            if code is None:
                await interaction.response.send_message(f"{interaction.guild.get_member(1078652607406551120).mention} we are out of codes for {item}s, please can we have more!")
                return False
            merch = self.get_merch()[item]()
            await interaction.response.send_message(merch.return_string(interaction, code, user), ephemeral=False)
            self.mark_used(cell, user)
        #    await user.send(embed = merch().return_embed(interaction, code, user))
            remaining = self.get_remaining(item)
            await channel.send(f"There are {remaining} {item} codes left")
        except Exception:
            print(traceback.format_exc())


    @merch.autocomplete("item")
    async def merch_autocomplete(self, interaction: discord.Interaction, current:str):
        return [
            app_commands.Choice(name=key, value=key) for key in self.get_merch().keys() if
            current.lower() in key.lower()]

    async def on_message(self, message):
        if message.author.bot is True:
            return
        if message.guild is None:
            print("Message recieved!")
            try:
                embed = discord.Embed(title = "Received Message")
                embed.description = message.content
                embed.set_author(name = message.author.name, icon_url = message.author.avatar.url)
                embed.colour = discord.Colour.from_str("#F87295")
                embed.set_footer(text = f"Received at {datetime.datetime.now()}")
                await self.bot.get_guild(1078653950821158953).get_channel(1205168039935352872).send(embed = embed)
            except Exception:
                print(traceback.format_exc())
        try:
            if "[[" in message.content and "]]" in message.content:  # This should be regex
                queries = self.filter(message.content)
                for query in queries:
                    scrape = WebData(self.bot, query)
                    products = scrape.get_products()
                    display = ProductDisplay(self.bot, products)
                    await message.channel.send(embeds=[display.get_embed()], view=ProductSelect(products, display))

        except Exception:
            print(traceback.format_exc())

    def filter(self, message):  # Ernie is going to kill me
        queries = re.findall(r"\[\[(.*?)\]\]", message)
        print(queries)
        return queries

    @app_commands.default_permissions(manage_messages=True)
    @app_commands.command(name="codes")
    async def code(self, interaction, item:str, user:discord.Member):
        if not await self.guild_check(interaction):
            return False
        try:
            code, cell = self.get_item_code(item)
            if code is None:
                await interaction.response.send_message(f"{interaction.guild.get_member(1078652607406551120).mention} we are out of codes for {item}s, please can we have more!")
                return False
            self.mark_used(cell, user)
            await interaction.response.send_message(f"The next code is {code}. Assigned it to {user.name} on the sheet for you.")
        except Exception:
            print(traceback.format_exc())

    def get_item_code(self, item):
        merch = self.get_merch()[item]()
        column = self.google_sheets.find_cell(merch.query_str).col
        cell = self.google_sheets.first_blank(column)
        code = cell.value
        return code, cell

    def mark_used(self, cell, user):
        self.google_sheets.mark_used(cell)
        self.google_sheets.set_cell(self.google_sheets.get_next_cell(cell), user.name)
        self.google_sheets.mark_used(self.google_sheets.get_next_cell(cell))

    def get_remaining(self, item):
        code, cell = self.get_item_code(item)
        return self.google_sheets.get_remaining(cell.col)


    @app_commands.default_permissions(manage_messages = True)
    @app_commands.command(name = 'remaining')
    async def report_remaining(self, interaction, item:str):
        try:
            await interaction.response.defer(thinking = True)
            remaining = self.get_remaining(item)
            await interaction.followup.send(f"There are {self.get_remaining(item)} {item} codes left!")
        except Exception:
            print(traceback.format_exc())


    @code.autocomplete("item")
    async def code_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=key, value=key) for key in self.get_merch().keys() if current.lower() in key.lower()]

    @report_remaining.autocomplete("item")
    async def report_autocomplete(self, interaction:discord.Interaction, current: str):
        return [
            app_commands.Choice(name=key, value=key) for key in self.get_merch().keys() if
            current.lower() in key.lower()]