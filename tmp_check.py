import requests
from scraper.parsers.thebodyshop import parse as parse_tb
from scraper.parsers.coles import parse as parse_coles

html = requests.get('https://www.thebodyshop.com.au/pages/offers', timeout=20, headers={'User-Agent':'Mozilla/5.0'}).text
print('TB', len(parse_tb(html, min_discount=30, site_url='https://www.thebodyshop.com.au/pages/offers')))

html = requests.get('https://www.coles.com.au/on-special?filter_Special=halfprice&page=1', timeout=20, headers={'User-Agent':'Mozilla/5.0'}).text
print('COL', len(parse_coles(html, min_discount=30, site_url='https://www.coles.com.au/on-special?filter_Special=halfprice&page=1')))
