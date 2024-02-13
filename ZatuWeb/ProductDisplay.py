import traceback

import discord


class ProductDisplay:

    def __init__(self, bot, products):
        print("Product Display Init")
        try:
            self.bot = bot
            self.products = products
            self.index = 0
        except Exception:
            print(traceback.format_exc())

    def get_embed(self):
        try:
            product = self.products[self.index]
            embed = discord.Embed(title=product.find(class_='zg-product-image')["title"])
            embed.colour = discord.Colour.from_str('#f87295')
            embed.set_image(url=product.find('img')['data-src'])
            embed.url = product.find(class_ = 'zg-product-image')['href']
            embed.add_field(name=f"Price", value=f"£{product.find(class_='zg-price-box zg-price-box-now')['data-now']}")
            try:
                embed.add_field(name="Stock", value=f"{product.find(class_='zg-product-notice').find('span').get_text()}")
            except AttributeError:
                pass
            embed.set_footer(text = f"Item {self.index + 1} out of {len(self.products)}")
        except Exception:
            print(traceback.format_exc())
        return embed

    def next(self):
        self.index = self.index + 1
        self.index = self.index % len(self.products)
        return self.get_embed()

    def previous(self):
        self.index = self.index - 1
        self.index = self.index % len(self.products)
        return self.get_embed()