from bs4 import BeautifulSoup
from Spider import Spider
from Postman import Postman
from datetime import datetime
import requests
import json
from multiprocessing import Pool
import time

def parse_main_menu():

    with open("navigation.html", "r") as ff:
        page_source = ff.read()
        soup = BeautifulSoup(page_source, "html.parser")

        soup_a = soup.find_all("a")
        links = [{ "name" : link.text, "url" : link["href"]} for link in soup_a]

        return links

def parse_listing(categories):

    postman = Postman.init()

    for category in categories:
        print(category)
        spider = Spider( url = category["url"] )

        with open("page.html", "a") as f:
            f.write(spider.get_page())

        soup = BeautifulSoup(spider.get_page(), "html.parser")
        soup_a = soup.find_all("a", class_="item _item")
        products = [a["href"] for a in soup_a]

        print(products)

        for num,url in enumerate(products):
            parse_detail( category, url, postman )
            print(category, num, len(products))
            print("sleep 3")
            time.sleep(1)
            print("sleep 2")
            time.sleep(1)
            print("sleep 1")
            time.sleep(1)
            
        break

def parse_detail( category, url, postman ):

    check = postman.get('SELECT `idx` FROM `products` WHERE `url` = %s ', [url])

    if 'idx' in check:
        print(category, 'skip')
        return

    spider = Spider( url = url )

    soup = BeautifulSoup(spider.get_page(), "html.parser")

    # product name
    product_name = soup.find("h1", class_="product-name")

    # remove mark
    name_span = product_name.find("span")
    name_span.extract()

    # product name
    product_info = soup.find("div", class_="product-info-wrapper")

    # product images
    soup_images = soup.find_all("img", class_="image-big _img-zoom")
    product_images = [soup_img["src"] for soup_img in soup_images]

    # check if image is properly brought
    skip_product = False
    for image in product_images:
        if 'base64' in image:
            skip_product = True
            print("base64", image)
            break

    if skip_product:
        with open("skip.txt", "a") as f:
            print("skip.txt", url)
            f.write(url)
            f.write("\n")
        return

    # insert into db
    sql = 'INSERT INTO `products` (`mall_idx`, `category`, `item_id`, `name`, `name_org`, `detail`, `url`, `created_date_time`, `status`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s )'
    params = ['1', category["name"], '', product_name.get_text(), product_name.get_text(), product_info.prettify(), url, str(datetime.now().strftime("%Y-%m-%d %H:%I:%S")), '1']
    product_idx = postman.create(sql, params)
    print("created: ", product_idx)

    # insert into db
    for image in product_images:
        url_comp = image.split('/')
        filename = url_comp[ (len(url_comp) - 1) ]
        filename = filename.split('?')[0]
        sql = ''' INSERT INTO `product_images` (`mall_idx`, `product_idx`, `filename`, `url`, `downloaded`, `should_use`, `created_date_time`, `status`)  VALUES ( %s, %s, %s, %s, %s, %s, %s, %s ) '''
        params = ['1', product_idx, filename, "http:" + image, '0', '1', str(datetime.now().strftime("%Y-%m-%d %H:%I:%S")), '1']
        postman.execute(sql, params)

    with Pool(100) as p:
        list(p.map(download_image, product_images))

def download_image(image):

    url_comp = image.split('/')
    filename = url_comp[ (len(url_comp) - 1) ]
    filename = filename.split('?')[0]
    path_filename = '/mnt/ssd3/fashion_up/image/' + filename

    r = requests.get("http:" + image, allow_redirects=True)

    with open(path_filename, 'wb') as fp:
        fp.write(r.content)

categories = parse_main_menu()
print(categories)
parse_listing(categories)
