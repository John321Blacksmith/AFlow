"""
This testual module adheres the asynchronous conception.
There are five functions which do a whole
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

		# html data of the response
		# html = await response.text()

		# status code of the response
		# status = response.status

		# return {'html': html, 'status': status}

		return await response.text()


async def collect_tasks_from_each_page(session, item):
	"""
	This function goes through each page and collects tasks to
	be performed asynchronously.
	"""

	# define a task bag
	tasks = []

	# define a number of pages to be processed
	num_of_pages = await find_pages_amount(session, item)
	
	# # wade through the urls list
	for i in range(0, num_of_pages):
		# get the task
		n = i + 1
		task = asyncio.create_task(get_response(session, books[item]['source'].format(n)))
		tasks.append(task)

	# gather all the tasks in one object corountine
	result = await asyncio.gather(*tasks)

	return result


async def find_pages_amount(session, item):
	"""
	This async function invokes a parser method that finds an amount 
	of pages and so defines a quantity of tasks to be performed.
	"""
	amount = None

	# get a single response
	response = await get_response(session, books[item]['source'].format(1))
	if response:
		# utilize a parser
		amount = Df.get_pages_amount(response, item, books)

	return amount


async def begin_session(item):
	"""
	This function performs these two above,
	giving a session object and initializing the web data.
	Returns a bunch of materials based on requests and enclosed
	as tasks to be performed asynchronously
	"""
	async with aiohttp.ClientSession() as session:
		# gather a list of responses
		data = await collect_tasks_from_each_page(session, item)

		return data


async def main():
	"""
	This function gives a life to the other ones
	and makes the tasks be performed in a loop.
	"""
	# inquire a name of the internet bookstore,
	# excel file name, 
	item = input('Enter the source name: ')
	
	# specify the name of the excel sheet
	sheetname = input('enter the name of the sheet: ')

	# the directory of the excel file is generated via substraction of both 
	# 'tables' directory and a name of the internet bookmarket
	file_name = 'tables/' + item + '.xlsx'

	fields = books[item]['excel_fields']

	# take tasks
	results = await begin_session(item)

	# define a parsing object
	scraper = Df(results, item, fields, books)

	# get unstructured data from each task
	content = scraper.fetch_content()

	# get structured data
	books_list = scraper.structure_data(content)

	# write the gotten objects to the excel sheet
	data_manager.write_objs_to_excel(file_name, sheet=sheetname, list_of_objs=books_list, columns=scraper.data_fields)


if __name__ == '__main__':

	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	asyncio.run(main())
	