import requests
import re

def fix_link(to_fix, endpoint):
    return re.sub(r'http://.*?\?', f'{endpoint}?', to_fix)

def fetch_all(endpoint):
    r = requests.get(endpoint)
    parsed = r.json()
    # todo - also parse/handle first response
    while 'nextLink' in parsed:
        fixed_link = fix_link(parsed['nextLink'], endpoint)
        r = requests.get(fixed_link)
        parsed = r.json()
        print(f'received response with len {len(r.content)}')

endpoints = [
    'https://api.raporty.pse.pl/api/ogr-oper',
    'https://api.raporty.pse.pl/api/ogr-oper-head'
]

for endpoint in endpoints:
    print(f"Fetching data from {endpoint}")
    fetch_all(endpoint)
    print("Done fetching data.")
