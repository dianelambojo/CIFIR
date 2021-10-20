from bs4 import BeautifulSoup
import requests

page_url = 'https://www.npmjs.com/package/request'
source_code = requests.get(page_url)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, features="lxml")
for bold in soup.findAll('h1'):
    print(bold.contents)