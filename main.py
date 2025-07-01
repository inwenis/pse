import requests


r = requests.get('https://api.raporty.pse.pl/api/ogr-oper')

print(r)
print(r.json())
