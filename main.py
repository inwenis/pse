# scrapes all endpoints from https://api.raporty.pse.pl/app/home and saves responses to out/*[C].json
# GUI for data - https://raporty.pse.pl/

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
    with open(f'out/{endpoint}_{str(counter).zfill(3)}.json', 'w', encoding='utf-8') as f:
        f.write(content)

# I don't like using a global watcher
# todo - stop using a global watcher in fetch_all()
watcher = watcher.Watcher(urls)

def fetch_all(url):
    all = []

    current_link = url

    try:
        while True:
            response = requests.get(current_link)
            watcher.report_scraped(url)
            all.append(response.text)
            parsed = response.json()
            if 'nextLink' not in parsed:
                break
            else:
                current_link = fix_pagination_link(parsed['nextLink'], url)
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
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(fetch_all, urls)

print(f'Fetched {len(urls)} urls')

for url, responses in results:
    print(f'got {len(responses)} results for {url}')
    for counter, content in enumerate(responses):
        save_to_file(url, counter, content)
