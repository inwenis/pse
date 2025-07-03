# since there are many endpoints for PSE and scraping all the data takes time
# I'm creating this watcher that will report the progress

import os
import threading

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Watcher:
    def __init__(self, urls):
        self.counter = {url: 0 for url in urls}
        self.lock = threading.Lock()

    def report_scraped(self, url):
        # because scraping a single url is sequential we can safely increment the counter
        # without worrying about thread safety
        self.counter[url] += 1
        # we don't need to print progress every time a file is scraped
        # so we print it only if no other thread is currently printing
        if not self.lock.locked():
            with self.lock:
                self.print_progress()

    def report_scraped_all(self, url):
        self.counter[url] *= -1 # multiply by -1 to indicate that all files for this URL have been scraped

    def print_progress(self):
        cls()
        for url, count in self.counter.items():
            if count >= 0:
                print(f"{url.ljust(60)}: {count} files scraped")
            else:
                print(f"{url.ljust(60)}: {-count} files scraped (all done)")
