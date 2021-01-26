# General Purpose Scraper
Web scraper for arbitrary data

## Requirements
The scraper requires: 
- the [geckodriver](https://github.com/mozilla/geckodriver/releases)
- python modules listed in [requirements.txt](https://github.com/JureBevc/GeneralPurposeScraper/blob/main/requirements.txt)

## Usage
A simple GUI is available by running `python gui.py`. Alternatively you can run the scraper programatically by importing `Scraper` from `general_scraper.scraper` and `Extractor` from `general_scraper.extractor`. You can also run the example script `example.py` that will scrape twitter and look for the keyword `covid`.
