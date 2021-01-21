import time
import os
import threading
import sys
from urllib.parse import urlparse
from spider import Spider


class Scraper:

    thread_count = 0
    threads = []
    driver_instances = []

    url_queue = []
    visited = []
    initial_urls = []
    driver_path = None

    start_time = 0

    def __init__(self, initial_urls, extractor, url_match=[], thread_count=1, driver_path=None):
        self.initial_urls = initial_urls
        self.url_match = url_match
        self.extractor = extractor
        self.driver_path = driver_path
        self.thread_count = thread_count

    def start(self):
        self.start_time = time.time()
        # Add initial urls to queue
        self.url_queue.extend(self.initial_urls)

        # Set default driver path
        if not self.driver_path:
            self.driver_path = os.path.dirname(os.path.realpath(__file__)) + "\\geckodriver.exe"
        print("Driver path: {}".format(self.driver_path))
        # Create spider threads
        print("Creating {} threads.".format(self.thread_count))
        for i in range(self.thread_count):
            spider_thread = Spider(self, "Spider {}".format(i+1), self.extractor, self.driver_path)
            spider_thread.daemon = True
            self.threads.append(spider_thread)
        
        try:
            # Start spider threads
            for i in range(self.thread_count):
                self.threads[i].start()
            
            # Wait for threads
            while self.alive_count() > 0:
                print(self.status_string())
                time.sleep(10)
        except (KeyboardInterrupt, SystemExit):
            for i in range(self.thread_count):
                self.threads[i].stop()
            while self.alive_count() > 0:
                print("Stopping {}...".format(self.alive_count()))
                time.sleep(1)

    def pop_queue(self):
        if len(self.url_queue) == 0:
            return None
        url = self.url_queue.pop(0)
        self.visited.append(url)
        return url
    
    def add_to_queue(self, url):
        self.url_queue.append(url)

    def eligible_for_queue(self, url):
        if url in self.url_queue or url in self.visited:
            return False
        if len(self.url_match) > 0:
            base_url = urlparse(url).netloc
            for match in self.url_match:
                if base_url == match:
                    return True
            return False
        return True

    def alive_count(self):
        count = 0
        for thread in self.threads:
            if thread.is_alive():
                count += 1
        return count
    
    def add_driver_instance(self, driver):
        self.driver_instances.append(driver)
    
    def quit_all_drivers(self):
        for driver in self.driver_instances:
            try:
                driver.quit()
            except Exception as e:
                pass

    def status_string(self):
        return "\t---Status---\n\tElapsed time: {}\n\tAlive threads: {}\n\tQueue size: {}\n\tVisited: {}".format(
            str(int(time.time()-self.start_time)) + "s",
            self.alive_count(), 
            len(self.url_queue),
            len(self.visited))