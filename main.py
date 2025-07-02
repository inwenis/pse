import requests
import re

def fix_pagination_link(to_fix, endpoint):
    return re.sub(r'http://.*?\?', f'{endpoint}?', to_fix)

def fetch_all(endpoint):
    all = []

    current_link = endpoint

    while True:
        response = requests.get(current_link)
        print(f'received response with len {len(response.content)}')
        all.append(response.text)
        parsed = response.json()
        if 'nextLink' not in parsed:
            break
        else:
            current_link = fix_pagination_link(parsed['nextLink'], endpoint)
    return all

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
