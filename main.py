# scrapes data from https://api.raporty.pse.pl/app/home

import requests
import re
import os
import concurrent.futures
import watcher
from urls import urls

def fix_pagination_link(to_fix, full_endpoint_url):
    return re.sub(r'http://.*?\?', f'{full_endpoint_url}?', to_fix)

def save_to_file(url, counter, content):
    endpoint = url.split('/')[-1]
    with open(f'out/{endpoint}_{counter}.json', 'w', encoding='utf-8') as f:
        f.write(content)

# I don't like using a global watcher
# todo - stop using a global watcher in fetch_all()
watcher = watcher.Watcher(urls)

def fetch_all(url):
    all = []

    current_link = url

    try:
        while True:
            response = requests.get(current_link, timeout=2)
            watcher.report_scraped(url)
            all.append(response.text)
            parsed = response.json()
            if 'nextLink' not in parsed:
                break
            else:
                current_link = fix_pagination_link(parsed['nextLink'], url)
        # todo - fix bug - it seems some urls are never marked as done
        # i suspect it is because the watcher is not fully thread-safe
        watcher.report_scraped_all(url)
        return url, all
    except Exception:
        # temporarily swallow all exceptions so the scraper doesn't crash when one url fails
        # todo - handle exceptions properly, e.g. log them
        # todo - add retires and use exponential backoff and
        watcher.report_scraped_all(url)
        return url, all

os.makedirs('out', exist_ok=True) # Ensure the output directory exists before saving files

# I know little of parallel/concurrency in python so I'm not sure if this is the way to go
# but it works
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(fetch_all, urls)
    for url, responses in results:
        print(f'got {len(responses)} results for {url}')
        for counter, content in enumerate(responses):
            # todo - saving will fail if there is no 'out' directory
            # saving to files could be handled in a separate class called FileSaver/Dumper/etc
            save_to_file(url, counter, content)
