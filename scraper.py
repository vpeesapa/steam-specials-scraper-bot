#!/usr/bin/python3.10

import requests
from bs4 import BeautifulSoup
from table2ascii import table2ascii,PresetStyle

BASE_URL = "https://store.steampowered.com/search?"

# Scrapes all the specials in Steam
def scrape():
	URL = BASE_URL + "specials=1"

	page = requests.get(URL)

	# Create a scraper that parses HTML code
	soup = BeautifulSoup(page.content,'html.parser')

	# Get the portion of the page related to the relevant information about discounted games
	searchResultsContainer = soup.find('div',id='search_result_container')

	# Get all the search results
	searchResults = searchResultsContainer.find_all('a')

	relevantInfos = []

	for i in range(10):
		info = {}

		info['title'] = searchResults[i].find('span',class_='title').text

		discountContainer = searchResults[i].find('div',class_='search_discount')
		info['discount'] = discountContainer.find('span').text.split('-')[1]

		priceContainer = searchResults[i].find('div',class_='search_price')
		info['original_price'] = priceContainer.find('strike').text
		info['new_price'] = priceContainer.contents[3].strip()

		relevantInfos.append(info)

	outputTable = table2ascii(
			header = ["Title","Discount","Original Price","Discounted Price"],
			body = [
						[
							relevantInfo['title'],
							relevantInfo['discount'],
							relevantInfo['original_price'],
							relevantInfo['new_price']
						] for relevantInfo in relevantInfos
					],
			style = PresetStyle.ascii_box,
			column_widths = None
		)

	return outputTable

# Scrapes all the top sellers in steam
def top_scrape():
	URL = BASE_URL + "filter=topsellers"

	page = requests.get(URL)

	# Create a scraper that parses HTML code
	soup = BeautifulSoup(page.content,'html.parser')

	# Get the portion of the game related to the information containing the popular games
	searchResultsContainer = soup.find('div',id="search_result_container")

	# Get information about all the free games
	searchResults = searchResultsContainer.find_all('a')

	relevantInfos = []

	for i in range(10):
		info = {}

		info['title'] = searchResults[i].find('span').text
		info['release_date'] = searchResults[i].find('div',class_='search_released').text

		reviewContainer = searchResults[i].find('span',class_='search_review_summary')
		if reviewContainer != None:
			info['review'] = reviewContainer['data-tooltip-html'].split('<br>')[1].split(' ')[0]
		else:
			info['review'] = 'N/A'

		priceContainer = searchResults[i].find('div',class_='search_price')
		
		if "discounted" in priceContainer.get("class"):
			info['price'] = priceContainer.contents[3].strip()
		else:
			info['price'] = priceContainer.text.strip()

		relevantInfos.append(info)

	outputTable = table2ascii(
			header = ["Title","Release Date","Review","Price"],
			body = [
						[
							relevantInfo['title'],
							relevantInfo['release_date'],
							relevantInfo['review'],
							relevantInfo['price']
						] for relevantInfo in relevantInfos
					],
			style = PresetStyle.ascii_box,
			column_widths = None
		)

	return outputTable