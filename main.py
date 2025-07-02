import requests
import re

def fix_link(to_fix, endpoint):
    return re.sub(r'http://.*?\?', f'{endpoint}?', to_fix)

def fetch_all(endpoint):
    r = requests.get(endpoint)
    parsed = r.json()
    count = 0
    # todo - also parse/handle first response
    while 'nextLink' in parsed:
        fixed_link = fix_link(parsed['nextLink'], endpoint)
        r = requests.get(fixed_link)
        parsed = r.json()
        print(f'received response with len {len(r.content)}')
        filename = f"out/{endpoint.split('/')[-1]}_{count}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(r.text + '\n')
        count += 1

# if necessary not you could automate getting all endpoints from the main page
# since we have code working for a hardcoded list of endpoints
endpoints = [
    'https://api.raporty.pse.pl/api/ogr-oper',
    'https://api.raporty.pse.pl/api/ogr-oper-head',
    'https://api.raporty.pse.pl/api/it-omb-rbb',
    'https://api.raporty.pse.pl/api/price-fcst',
    'https://api.raporty.pse.pl/api/price-cost',
    'https://api.raporty.pse.pl/api/pk5l-wp',
    'https://api.raporty.pse.pl/api/unav-pk5l'
]

# I know little of parallel/concurency in python so I'm not sure if this is the way to go
# but it works
import concurrent.futures

def fetch_and_print(endpoint):
    print(f"Fetching data from {endpoint}")
    fetch_all(endpoint)
    print("Done fetching data.")

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(fetch_and_print, endpoints)
