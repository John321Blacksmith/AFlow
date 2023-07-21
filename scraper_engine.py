import asyncio
import requests
import aiohttp
from urllib.parse import urljoin
import pandas as pd
import requests_html
from bs4 import BeautifulSoup as Bs
from requests_html import HTMLSession, AsyncHTMLSession
from typing import Union


async def get_aresponse(url, session):
    """
    Get a response from the source.
    """
    async with session.get(url) as response:
        return await response.text()


async def create_tasks(session, links: list[str], tasks=[]):
    """
    Forming the tasks.
    """
    for i in range(0, len(links)):
        task = asyncio.create_task(get_response(links[i], session))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results


async def aget_link_of_the_page(session, url: str, links=[]) -> list:
    """
    Extract a link of every page.
    """
    response = await get_aresponse(url, session)
    html = Bs(response, 'html.parser')
    next_link = html.select_one(scraping_data['books']['next_page'])
    if next_link:
        links.append(url) 
        return await aget_link_of_the_page(session, urljoin(url, next_link.get('href')), links) # recursive case
    else:
        return links # base case


async def get_response(url: str, session) -> None:
    """
    Send a single request to
    every address and return
    response objects,or NaN.
    """
    response = None
    try:
        session = AsyncHTMLSession()
        response = await session.get(url)
    except (Exception, requests.exceptions.RequestException) as exception:
        response = exception

    return response


async def save_links_of_multiple_pages(filename: str, links: list[str]) -> None:
    """
    Save links of the pages
    to the text file.
    """
    with open(filename, mode='w', encoding='utf-8') as f:
        try:
            for link in links:
                f.write(f'{link}\n')
            else:
                print(f'The links are loaded')
        except IndexError as error:
            print(f'Cannot perform the operation because {error}')


async def retrieve_saved_links(filename: str | None, links=[]) -> list:
    """
    Extract all the saved links
    from the file and put them
    into the list.
    """
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            saved_links = f.readlines()
            for link in saved_links:
                links.append(link)
    except (Exception, FileNotFoundError) as exception:
        print(f'Cannot perform the operation because {exception}')

    else:
        return links


async def get_objects(results, list_of_objects: Union[list[str], None] = []) -> list:
    """
    Fetch a list of articles and
    wade through all of them and
    extract the specified content
    via xpath params. Return a list
    of objects to be saved to the DB.
    """
    for i in range(0, len(results)):
        # items from the first page
        articles = results[i].html.xpath(scraping_data['books']['object'])

        for article in articles:
            obj = {
                'title': article.xpath(scraping_data['books']['title'])[0],
                'image': article.xpath(scraping_data['books']['image'])[0],
                'link': article.xpath(scraping_data['books']['link'])[0],
                'price': article.xpath(scraping_data['books']['price'])[0].text,
            }
            list_of_objects.append(obj)

    return list_of_objects


async def save_data(objects: Union[list[dict], None], filename: str) -> None:
    """
    Receive a list of scraped
    objects and apply the data
    frame for saving every one
    from the list.
    """
    dataframe = pd.DataFrame(data=objects, columns=scraping_data['books']['fields'])
    try:
        dataframe.to_csv(filename, mode='a')
        print(f'the data has been saved to the file {filename}')
    except Exception as excepion:
        print(exception)


async def start_asession():
    """
    Start the session. A main entrypoint.
    """
    async with aiohttp.ClientSession() as session:
        links = await retrieve_saved_links('links.txt')
        results = await create_tasks(session, links)
        objects = await get_objects(results)
        await save_data(objects, 'books.csv')



# async def main():
#     links = await retrieve_saved_links('links.txt')
#     print(links)


if __name__ == '__main__':
    asyncio.run(start_asession())