from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
import threading
import sys
from scraper import Scraper
from extractor import Extractor


image_id = 0
all_data = []

def write_images():
    global image_id
    while True:
        if len(all_data) > image_id:
            data = all_data[image_id]
            with open("images/image{}.png".format(image_id), "wb") as f:
                f.write(data)
            image_id += 1


def element_extraction(element):
    try:
        bites = element.screenshot_as_png
        if bites not in all_data: 
            all_data.append(element.screenshot_as_png)
    except Exception as e:
        pass

if __name__=="__main__":
    # write_thread = threading.Thread(target=write_images)
    # write_thread.daemon = True
    # write_thread.start()
    extract = Extractor("//div[@data-testid='tweet']")
    s = Scraper(["https://twitter.com/georgemofficial"], extract, url_match=["twitter.com", "www.twitter.com"], thread_count=10)
    try:
        s.start()
    except Exception as e:
        s.quit_all_drivers()
