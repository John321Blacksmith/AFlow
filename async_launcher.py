import re
import time
import csv
import random
import asyncio
import aiohttp
import pandas as pd
from urllib.parser import urljoin
from scraping_info import agents


async def get_links(file_name):
	links = []
	try:
		with open(file_name, mode='r', encoding='utf-8') as f:
			reader = csv.reader(f)

			for i, row in enumerate(reader):
				links.append(row[0])
	except FileNotFoundError:
		print(f'File {file_name} not found')
	else:
		return links


async def get_response(session, url):
	async with session.get(url) as response:
		return await response.text()
		 


async def create_tasks():
	"""
	This function receives a list of links to be requested, starts a session and
	catches a response from each link and gathers the responses as tasks.
	"""
	async with aiohttp.ClientSession(headers={'User-Agent': random.choice(agents)}) as session:
		tasks = []
		links = await get_links('links.csv')
		for link in links:
			tasks.append(asyncio.create_task(get_response(session, link)))
		results = await asyncio.gather(*tasks)

		return results

	
async def extract_data(results) -> list:
	"""
	This function receives a bunch of results to be scraped,
	goes through each one and extracts data and forms a dictionary object.
	It then returns a list of objects which come to the database.
	"""
	list_ofobjects = []
	for i in range(0, len(results)):
		soup = Bs(results[i], 'html.parser')
		objs = soup.select(site_dict[item]['object'])
		for j in range(0, len(objs)):
			title = objs[j].select(site_dict[item]['title'])
			price = objs[j].select(site_dict[item]['price'])
			link = objs[j].select(site_dict[item]['link'])
			image = objs[j].select(site_dict[item]['image'])

			obj = {
				'title' = title.text,
				'price' = price.text,
				'link' = urljoin(site_dict[item]['source'], link),
				'image' = urljoin(site_dict[item]['source'], image)
			}

			list_of_objects.append(obj)

	return list_of_objects


async def main():
	"""
	This function performs a data saving operation 
	and indicates an amount of working time the program has taken.
	"""
	start_time = time.time()
	# get the results to be processed
	results = await create_tasks()

	# get a list of objects to be dumped to an excel file
	objects = await extract_data(results)

	# create a data frame via the pandas library
	df = pd.DataFrame(filename='tables/books.xlsx')

	print(f'Process finished at {(time.time() - start_time):.2f} seconds')


if __name__ == '__main__':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	asyncio.run(main())