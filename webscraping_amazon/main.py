import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/'

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
           (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}

site = requests.get(url, headers= headers)
soup = BeautifulSoup(site.content, 'html.parser')
