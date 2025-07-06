This is a scraper that scrapes all currently available endpoints from https://api.raporty.pse.pl/app/home

Data is saved to `out/*[C].json`

GUI for scraped data - https://raporty.pse.pl/

# TODOs
- add timeout for http requests
- add retires for http requests
- to enable more "parallelism" we can use dates to page through all available data instead of relying on pagination provided by `nextLink`
- add logging
- `watcher.py` clears the console so it will not work when we move to logging
- make it react to `Ctrl+C`

# How to run it?

```
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```
