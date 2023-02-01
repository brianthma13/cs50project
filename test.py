import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://lasvegas.electricdaisycarnival.com/lineup/')
soup = BeautifulSoup(r.content, 'html.parser')
hrefs = soup.find_all('a', href = "#modal-lineup-artist")

artist_list = []

for artist in hrefs:
    temp = artist.get_text()
    suffix = ' (.*)'
    if re.search(suffix, temp) is not None:
        temp = re.sub(suffix, '', temp)
        artist_list.append(temp)
    else:
        artist_list.append(temp)

print(artist_list)