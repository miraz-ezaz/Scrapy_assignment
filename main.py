import requests
from bs4 import BeautifulSoup
import json

page = requests.post("https://uk.trip.com/hotels/list?city=338&checkin=2024/8/9&checkout=2024/08/10")

print(page.text)

with open('text.txt', 'w') as f:
    f.write(page.text)

# soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.)