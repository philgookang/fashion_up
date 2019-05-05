import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import codecs
import os

class Spider:

    # Selenium Web Driver
    driver = None

    # Page To Load
    url = None

    # Whether or not to save output to file
    save_log = False

    # Log output location
    log_location = "/mnt/ssd3/fashsion_up/log/"

    # log output filename
    log_filename = "log.txt"

    def __init__(self, **kwargs):

        chromebrowser  = kwargs['chromebrowser']  if 'chromebrowser' in kwargs else '/mnt/ssd3/appls/chromium-browser'
        chromedriver   = kwargs['chromedriver']   if 'chromedriver'  in kwargs else '/mnt/ssd3/appls/chromedriver'

        self.log_location   = kwargs['log_location']    if 'log_location'   in kwargs else '/mnt/ssd3/court/headless/log/'
        self.log_filename   = kwargs['log_filename']    if 'log_filename'   in kwargs else 'log.txt'
        self.save_log       = kwargs['save_log']        if 'save_log'       in kwargs else False

        self.url            = kwargs['url']             if 'url'            in kwargs else ''

        options = webdriver.ChromeOptions()
        #options.add_argument('--screenshot')
        #options.add_argument('--disable-gpu')
        #options.add_argument('--window-size=1280,1696')
        #options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-application-cache')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--web-security=no')
        options.binary_location = chromebrowser


        try:
            # create driver
            self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
        except:
            print("spider.py", "Sleep for 30 seconds")
            time.sleep(240)
            print("spider.py", "Wake up from sleep, try again to alloc webdriver")

            # create driver
            self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)


        # driver more options
        self.driver.maximize_window()

    def get_page(self):

        if self.url == None:
            raise ValueError("Url missing")

        try:
            self.driver.get(self.url);
        except:
            print("spider.py", "self.driver.get Error", "going to sleep")
            time.sleep(1800)
            self.driver.get(self.url);

        page_source = self.driver.page_source

        if self.save_log:
            self.save_to_log(page_source)

        return page_source

    def save_to_log(self, page_source):
        with open(self.log_location + self.log_filename, "w") as ff:
            ff.write(page_source)

    def open_log(self):
        s = ""
        with open(self.log_location + self.log_filename, "r") as f:
            s = f.read()
        return s

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
