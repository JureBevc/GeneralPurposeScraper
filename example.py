from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
import threading
import sys
from general_scraper.scraper import Scraper
from general_scraper.extractor import Extractor


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

def print_status(status):
    print(status)

if __name__=="__main__":
    # write_thread = threading.Thread(target=write_images)
    # write_thread.daemon = True
    # write_thread.start()
    extract = Extractor("//div[@data-testid='tweet' and (contains(string(), 'covid') or contains(string(), 'korona'))]")
    s = Scraper(["https://twitter.com/slovenija"], extract, url_match=["twitter.com", "www.twitter.com"], thread_count=3, status_callback=print_status)
    try:
        s.start()
    except Exception as e:
        print(e)
        s.quit_all_drivers()
