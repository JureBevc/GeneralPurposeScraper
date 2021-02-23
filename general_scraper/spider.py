from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
import threading
import sys

class Spider(threading.Thread):
    clean_and_exit = False
    def __init__(self, scraper, name, extractor, driver_path):
        threading.Thread.__init__(self)
        self.name = name
        self.scraper = scraper
        self.extractor = extractor

        # Init selenium driver
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options, executable_path=driver_path)
        self.driver.implicitly_wait(10)

        self.scraper.add_driver_instance(self.driver)
    
    def run(self):
        while not self.clean_and_exit:
            time.sleep(3)
            if self.clean_and_exit:
                break
            try:
                current_url = self.scraper.pop_queue()
                if not current_url:
                    continue
                self.visit_url(current_url)
            except Exception as e:
                pass
                print(e)
        self.driver.quit()

    def visit_url(self, current_url):
        print("[{}] Fetching {}".format(self.name, current_url))
        self.driver.get(current_url)
        
        
        previous_elements_count = -1
        extracted_elements = self.extractor.xpath_matches(self.driver)
        scroll_count = 0
        while previous_elements_count != len(extracted_elements):
            if scroll_count > 0:
                print("[{}] Scrolling {}: {}".format(self.name, scroll_count, current_url))
            # Extract relevant data
            self.extractor.extract_from_elements(extracted_elements)

            # Extract new urls
            link_elements = self.driver.find_elements_by_xpath("//a[@href]")
            if link_elements:
                print("[{}] Found {} urls on {}".format(self.name, len(link_elements), current_url))
                for element in link_elements:
                    element_url = element.get_attribute("href")
                    if not (element_url.startswith("//") or element_url.startswith("http://") or element_url.startswith("https://")):
                        element_url = current_url + element_url
                    if self.scraper.eligible_for_queue(element_url):
                        self.scraper.add_to_queue(element_url)
            
            # Scroll down and extract again
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            previous_elements_count = len(extracted_elements)
            extracted_elements = self.extractor.xpath_matches(self.driver)
            scroll_count += 1

    def stop(self):
        self.driver.quit()
        self.clean_and_exit = True