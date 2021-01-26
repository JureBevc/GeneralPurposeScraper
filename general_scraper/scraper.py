import time
import os
import threading
import sys
from urllib.parse import urlparse
from general_scraper.spider import Spider


class Scraper:

    start_time = 0

    def __init__(self, initial_urls, extractor, url_match=[], thread_count=1, driver_path=None, status_callback=None):
        self.threads = []
        self.driver_instances = []
        self.url_queue = []
        self.visited = []
        self.initial_urls = initial_urls
        self.url_match = url_match
        self.extractor = extractor
        self.driver_path = driver_path
        self.thread_count = thread_count
        self.status_callback = status_callback

        for i in range(len(self.url_match)):
            self.url_match[i] = urlparse(self.url_match[i]).netloc

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
            print("Starting spider threads ({})".format(len(self.threads)))
            # Start spider threads
            for i in range(self.thread_count):
                self.threads[i].start()
            
            print("Threads running..." + str(self.alive_count()))
            # Wait for threads
            while self.alive_count() > 0:
                #print(self.status_string())
                if self.status_callback:
                    self.status_callback(self.status())
                time.sleep(10)
            print("Ending...")
        except (KeyboardInterrupt, SystemExit):
            print("Exiting...")
            self.stop()

    def stop(self):
        for i in range(self.thread_count):
            self.threads[i].stop()
        while self.alive_count() > 0:
            print("Stopping {}...".format(self.alive_count()))
            time.sleep(0.2)
        self.threads = []
        self.quit_all_drivers()

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

    def status(self):
        return {"elapsed_time": int(time.time()-self.start_time),
            "alive_threads": self.alive_count(),
            "queue_size": len(self.url_queue),
            "visited": len(self.visited),
            "extracted": self.extractor.total_extractions,
            "saved": self.extractor.total_saved}
