import sys
import pytest
sys.path += [
'..\\..\\data_machine\\configs\\html_tags',
'..\\..\\data_machine\\managers'
]
from scraping_manager.engine import (
									LinksLoadingManager,
									DataFetcher
								)
from scraping_info import books


class TestWebCrawlingLogic:
	"""
	This test checks the work
	of the WebCrawler.
	"""

	def test_the_links_are_properly_scraped(self):
		"""
		Check if the page links are
		properly extracted from the
		web.
		"""
		...


class TestLinksLoaderLogic:
	"""
	This test checks the work
	of the LinksLoading Manager.
	"""

	def __init__(self):
		self.mock_links = [
			'https://www.test0.com',
			'https://www.test1.com',
			'https://www.test2.com',
			'https://www.test3.com',
			'https://www.test4.com',
		]
		self.wrong_file = 'wrong.csv'
		self.file = 'mock_files\\links.csv'
		self.empty_file = 'mock_files\\links.csv'
		self.succsessful_manager = LinksLoadingManager(self.file)
		self.unsuccsessful_manager = LinksLoadingManager(self.empty_file)

	def test_the_scraped_links_are_properly_cached(self):
		"""
		Check if the links from the web
		are saved to the CSV file well.
		"""
		result = self.links_manager.save_links(self.mock_links)
		with open(self.file, 'r') as f:
			assert len(f.readlines()) == len(self.mock_links)

		assert result == True

	def test_the_manager_throws_false_if_links_not_cached(self):
		"""
		Check if the False
		is thrown.
		"""
		assert self.unsuccessful_manager.save_links(self.wrong_file) == False

	def test_the_cached_links_are_retrieved(self):
		"""
		Check if all the links are
		taken from the HD and formed
		to a python DS.
		"""
		retrieved_links = self.links_manager.retrieve_links()
		assert len(retrieved_links) == len(self.mock_links)
		assert retrieved_links == self.mock_links

	def test_the_filechecker_returns_false_if_empty_csv(self):
		"""
		Check if the LinksLoader
		retrieves False when csv
		is empty.
		"""
		with open(self.file, 'r') as f:

		assert self.links_manager.csv_is_full() == False

	def test_the_filechecker_returns_true_if_filled_csv(self):
		"""
		Check if the LinksLoader
		retrieves False when csv
		is empty.
		"""
		assert self.links_manager.csv_is_full() == True


class TestDataFetcherLogic:
	"""
	This test checks the work
	of the data extraction unit
	"""
	...
