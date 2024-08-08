import requests
from bs4 import BeautifulSoup

page = requests.get("https://uk.trip.com/hotels/list?city=338&checkin=2024/8/2&checkout=2024/08/03")

soup = BeautifulSoup(page.text, 'html.parser')
print(soup.find_all('ul'))