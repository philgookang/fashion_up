import requests
from bs4 import BeautifulSoup

class Zara:

    def __init__(self):
        pass

    def get_html(self, url):
        document = requests.get(url).content
        return BeautifulSoup(document, "html.parser")

    def parse_detail(self):

        url = "https://www.zara.com/kr/ko/%EB%B2%A0%EC%9D%B4%EC%A7%81-%EB%8D%B0%EB%8B%98-%EC%9E%AC%ED%82%B7-p04454322.html?v1=8389517&v2=1181233"

        soup = self.get_html(url)

        # product name
        product_name = soup.find("h1", class_="product-name")

        # product images
        soup_images = soup.find_all("img", class_="image-big _img-zoom")
        product_images = [soup_img["src"] for soup_img in soup_images]

        print(product_images)



z = Zara()
z.parse_detail()