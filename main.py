import requests
import re

def fix_link(link):
    return re.sub(r'http://.*ogr\-oper\?', 'https://api.raporty.pse.pl/api/ogr-oper?', link)

r = requests.get('https://api.raporty.pse.pl/api/ogr-oper')
parsed = r.json()

fixed_link = fix_link(parsed['nextLink'])

for i in range(100):
    r = requests.get(fixed_link)
    parsed = r.json()
    dates = [item['from_dtime'] for item in parsed['value']]
    dates = sorted(dates)
    first = dates[0]
    last = dates[-1]
    print(f"from-to: {first} {last}")
    fixed_link = fix_link(parsed['nextLink'])
