import requests
from bs4 import BeautifulSoup
import json

page = requests.post('https://uk.trip.com/hotels/?locale=en-GB&curr=GBP')

soup = BeautifulSoup(page.text, 'html.parser')

print(soup.prettify())