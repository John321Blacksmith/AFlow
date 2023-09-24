import sys
import pytest
sys.path.append('..\\..\\data_machine\\configs\\html_tags')
from scraping_info import books


class TestWebCrawlingLogic:
	"""
	This test checks the work
	of the LinksLoaderManager.
	"""

	def test_the_links_are_properly_scraped(self):
		"""
		Check if the page links are
		properly extracted from the
		web.
		"""
		...

	def test_the_scraped_links_are_properly_cached(self):
		"""
		Check if the links from the web
		are saved to the CSV file well.
		"""
		...

	def test_the_the_cached_links_are_retrieved(self):
		"""
		Check if all the links are
		taken from the HD and formed
		to a python DS.
		"""
		...


class DataFetcherTest:
	"""
	This test checks the work
	of the data extraction unit
	"""
	...
