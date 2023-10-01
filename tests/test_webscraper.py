import os
import sys
import asyncio
import unittest

scraper_path = os.getcwd()[:48] + '\\' + 'data_machine\\managers\\scraping_manager'
sys.path.append(scraper_path)

from engine import (
		LinksLoadingManager,
		DataFetcher
	)

class TestWebCrawlingLogic(unittest.TestCase):
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


class TestLinksLoaderLogic(unittest.TestCase):
	"""
	This test checks the work
	of the LinksLoading Manager.
	"""

	def setUp(self):
		self.mock_links = [
			'https://www.test0.com',
			'https://www.test1.com',
			'https://www.test2.com',
			'https://www.test3.com',
			'https://www.test4.com',
		]
		self.wrong_file = 'wrong.csv'
		self.file = os.getcwd()[:48] + '\\' + 'tests\\mock_files\\links.csv'
		self.empty_file = os.getcwd()[:48] + '\\' + 'tests\\mock_files\\empty_file.csv'
		self.successful_manager = LinksLoadingManager(self.file)
		self.unsuccessful_manager = LinksLoadingManager(self.empty_file)

	async def test_the_scraped_links_are_properly_cached(self):
		"""
		Check if the links from the web
		are saved to the CSV file well.
		"""
		await self.successful_manager.save_links(self.mock_links)
		with open(self.file, 'r') as f:
			self.assertEqual(len(f.readlines()), len(self.mock_links))

	async def test_the_manager_throws_false_if_links_not_cached(self):
		"""
		Check if the False
		is thrown.
		"""
		self.assertIs(await self.unsuccessful_manager.save_links(self.wrong_file), False)

	async def test_the_cached_links_are_retrieved_successfully(self):
		"""
		Check if all the links are
		taken from the HD and formed
		to a python DS.
		"""
		retrieved_links = await self.successful_manager.retrieve_links()
		self.assertEqual(len(retrieved_links), len(self.mock_links))
		self.assertEqual(retrieved_links, self.mock_links)

	async def test_if_none_is_returned_when_no_links_retrieved(self):
		"""
		Check if the links manager
		throws the None.
		"""
		self.assertIs(await self.unsuccessful_manager.retrieve_links(), None)

	async def test_the_filechecker_returns_false_if_empty_csv(self):
		"""
		Check if the LinksLoader
		retrieves False when csv
		is empty.
		"""
		self.assertIs(await self.unsuccessful_manager.csv_is_full(), False)

	async def test_the_filechecker_returns_true_if_filled_csv(self):
		"""
		# Check if the LinksLoader
		retrieves False when csv
		is empty.
		"""
		self.assertIs(await self.successful_manager.csv_is_full(), True)


class TestDataFetcherLogic(unittest.TestCase):
	"""
	This test checks the work
	of the data extraction unit
	"""
	...


if __name__ == '__main__':
	unittest.main()



# PASSED