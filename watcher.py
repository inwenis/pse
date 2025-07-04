# since there are many endpoints for PSE and scraping all the data takes time
# I'm creating this watcher that will report the progress

import os
import threading
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Watcher:
    def __init__(self, urls):
        self.counter = {url: 0 for url in urls}
        self.lock = threading.Lock()
        self.start = None

    def report_scraped(self, url):
        if self.start is None:
            self.start = time.time()
        # because scraping a single url is sequential we can safely increment the counter
        # without worrying about thread safety
        self.counter[url] += 1
        # we don't need to print progress every time a file is scraped
        # so we print it only if no other thread is currently printing
        if not self.lock.locked():
            with self.lock:
                self.__print_progress()

    def report_scraped_all(self, url):
        self.counter[url] *= -1 # multiply by -1 to indicate that all files for this URL have been scraped

    def __print_progress(self):
        elapsed = time.time() - self.start
        msg = f"Scraping progress (elapsed time: {elapsed:.2f} seconds):\n"
        for url, count in self.counter.items():
            if count >= 0:
                msg += f"{url.ljust(60)}: {count:>5} files scraped\n"
            else:
                msg += f"{url.ljust(60)}: {-count:>5} files scraped (all done)\n"
        cls()
        print(msg)
