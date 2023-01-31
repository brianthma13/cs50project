import requests
from bs4 import BeautifulSoup

r = requests.get('https://lasvegas.electricdaisycarnival.com/lineup/')
soup = BeautifulSoup(r.content, 'html.parser')
text = soup.findAll(text=True)

with open('output.txt', 'w') as f:
    for p in text:
        f.write(p)