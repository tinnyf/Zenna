import re

import requests
from bs4 import BeautifulSoup


class WebData():
    def __init__(self, bot, query):
        self.webpage = requests.get(f"https://www.board-game.co.uk/search-results/?query={query}")
        self.soup = BeautifulSoup(self.webpage.content, 'lxml')
        self.bot = bot

    def get_products(self):
        return self.soup.find_all(class_=re.compile("zg-product zg-product-"))

