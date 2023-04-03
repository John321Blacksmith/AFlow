import csv
import requests
from bs4 import BeautifulSoup as Bs
from urllib.parse import urljoin
from scraping_info import agents, books


def fetch_links(url, links=[]):
	response = requests.get(url)
	print(response.url, flush=True)

	soup = Bs(response.text, 'html.parser')
	for link in soup.select(books['test']['link']):
		links.append(urljoin(url, link.get('href')))

	next_page = soup.select_one(books['test']['next_p'])

	if next_page:
		return fetch_links(urljoin(url, next_page.get('href')), links)  # recursive case
	else:
		return links # base case


def refresh_links():
	links = fetch_links(books['test']['source'])

	with open('links.csv', mode='w') as f:
		for link in links:
			f.write(link + '\n')


def write_to_text(objects):
	"""
	This function receives a list of objects and dumps all of them tho the file.
	"""
	pass


if __name__ == '__main__':
	refresh_links()