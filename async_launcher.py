"""
This testual module adheres the asynchronous conception.
There are three functions which do a whole
process of asynchronous web scraping.

"""
import asyncio
import aiohttp
import data_manager
from data_miner import DataFetcher as Df
from scraping_info import books


async def get_response(session, url):
	"""
	This function fetches the response data from the current page.
	"""
	async with session.get(url) as response:
		return await response.text()


async def collect_tasks_from_each_page(session):
	"""
	This function goes through each page and collects tasks to
	be performed asynchronously.
	"""

	# define a task bag
	tasks = []

	# define a number of pages to be processed
	num_of_pages = await find_pages_amount(session)
	
	# # wade through the urls list
	for i in range(0, num_of_pages):
		# get the task
		n = i + 1
		task = asyncio.create_task(get_response(session, books['russian-books']['source'].format(n)))
		print(books['russian-books']['source'].format(n))
		tasks.append(task)

	# gather all the tasks in one object corountine
	result = await asyncio.gather(*tasks)

	return result


async def find_pages_amount(session):
	"""
	This async function invokes a parser method that finds an amount 
	of pages and so defines a quantity of tasks to be performed.
	"""

	# get a single response
	response = await get_response(session, books['russian-books']['source'].format(1))

	# utilize a parser
	amount = Df.get_pages_amount(response,'russian-books', books)

	return amount


async def begin_session():
	"""
	This function performs these two above,
	giving a session object and initializing the web data.
	Returns a bunch of materials based on requests and enclosed
	as tasks to be performed asynchronously
	"""
	async with aiohttp.ClientSession() as session:
		# gather a list of responses
		data = await collect_tasks_from_each_page(session)

		return data


async def main():
	"""
	This function gives a life to the other ones
	and makes the tasks be performed in a loop.
	"""

	# take tasks
	results = await begin_session()

	# define a parsing object
	scraper = Df(results, 'russian-books', books)

	# get unstructured data from each task
	content = scraper.fetch_content()

	# get structured data
	books_list = scraper.structure_data(content)

	# write the gotten objects to the excel sheet
	data_manager.write_objs_to_excel('tables//russian-books.xlsx', list_of_objs=books_list)


if __name__ == '__main__':

	# define an event loop
	loop = asyncio.get_event_loop()
	
	# start a machine
	loop.run_until_complete(main())