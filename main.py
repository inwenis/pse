import requests
import re
import concurrent.futures
import watcher

def fix_pagination_link(to_fix, full_endpoint_url):
    return re.sub(r'http://.*?\?', f'{full_endpoint_url}?', to_fix)

def save_to_file(url, counter, content):
    endpoint = url.split('/')[-1]
    with open(f'out/{endpoint}_{counter}.json', 'w', encoding='utf-8') as f:
        f.write(content)

# if necessary not you could automate getting all endpoints from the main page
# since we have code working for a hardcoded list of endpoints
urls = [
    'https://api.raporty.pse.pl/api/ogr-oper',
    'https://api.raporty.pse.pl/api/ogr-oper-head',
    'https://api.raporty.pse.pl/api/it-omb-rbb',
    'https://api.raporty.pse.pl/api/price-fcst',
    'https://api.raporty.pse.pl/api/price-cost',
    'https://api.raporty.pse.pl/api/pk5l-wp',
    'https://api.raporty.pse.pl/api/unav-pk5l'
]

# I don't like using a global watcher
# todo - stop using a global watcher in fetch_all()
watcher = watcher.Watcher(urls)

def fetch_all(url):
    all = []

    current_link = url

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

# I know little of parallel/concurency in python so I'm not sure if this is the way to go
# but it works
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(fetch_all, urls)
    for url, responses in results:
        print(f'got {len(responses)} results for {url}')
        for counter, content in enumerate(responses):
            save_to_file(url, counter, content)
