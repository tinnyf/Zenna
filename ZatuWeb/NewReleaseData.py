import json
import re

from bs4 import BeautifulSoup
import requests


class NewReleaseData():
    def __init__(self):
        self.webpage = requests.get(f"https://www.board-game.co.uk/category/board-games/?popular=pre-order&order=newest")
        self.soup = BeautifulSoup(self.webpage.content, 'lxml')
        with open('releases.json') as json_file_r0:
            try:
                self.existing_products = json.load(json_file_r0)
            except Exception:
                self.existing_products = []

    def get_products(self):
        return self.soup.find_all(class_=re.compile("zg-product zg-product-"))

    def get_new_products(self):
        return [product for product in self.get_products() if self.get_title(product) not in self.existing_products]

    def get_title(self, product):
        return product.find(class_='zg-product-image')["title"]

    def update_products(self):
        self.existing_products = [self.get_title(product) for product in self.get_products()]
        with open("releases.json", 'w') as json_file:
            json.dump(self.existing_products,json_file)
        print("Written to Json")



