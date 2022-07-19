#!/usr/bin/python3.10

import requests
from bs4 import BeautifulSoup
from table2ascii import table2ascii,PresetStyle

URL = "https://store.steampowered.com/search/?specials=1"

page = requests.get(URL)

# Create a scraper that parses HTML code
soup = BeautifulSoup(page.content,'html.parser')

# Get the portion of the page related to the relevant information about discounted games
searchResultsContainer = soup.find('div',id='search_result_container')

# Get all the search results
searchResults = searchResultsContainer.find_all('a')

relevantInfos = []

for i in range(20):
	info = {}

	info['link'] = searchResults[i]['href'].split('?')[0]

	info['title'] = searchResults[i].find('span',class_='title').text

	discountContainer = searchResults[i].find('div',class_='search_discount')
	info['discount'] = discountContainer.find('span').text.split('-')[1]

	priceContainer = searchResults[i].find('div',class_='search_price')
	info['original_price'] = priceContainer.find('strike').text
	info['new_price'] = priceContainer.contents[3].strip()

	relevantInfos.append(info)

outputTable = table2ascii(
		header = ["Title","Discount","Original Price","Discounted Price","Link"],
		body = [
					[
						relevantInfo['title'],
						relevantInfo['discount'],
						relevantInfo['original_price'],
						relevantInfo['new_price'],
						relevantInfo['link']
					] for relevantInfo in relevantInfos
				],
		style = PresetStyle.ascii_box
	)

print(outputTable)