import requests
from bs4 import BeautifulSoup as Bs


class Category:
    def __init__(self):
        self.url = 'https://www.lagou.com/'

    def get_categories(self):
        response = requests.get(self.url)
        soup = Bs(response.content, 'html.parser')
        categories = soup.select('.menu_sub a')
        category_name = []
        for category in categories:
            category_name.append(category.get_text())
        return category_name
