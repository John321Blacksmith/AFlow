import asyncio
import requests_html
from requests_html import AsyncHTMLSession
from scraping_info import scraping_data

# tasks iterator here


class LinksLoadingManager:
    """
    The object loads the links
    from the website and saves
    them to the flat file.
    It also takes the saved links
    from the file for crawling.

    async def save_links(source, file_name):
        :source: str
        :file_name: str
        :returns: str
    
    async def retrieve_links(file_name):
        :file_name: str
        :returns: list[str]

    """
    ...


class WebRequestManager:
    """
    The object takes a list of
    urls and sends async requests
    to each of them and returns
    a list of responses.

    async def get_request(url, session):
        :url: str
        :session: requests_html.AsyncHTMLSession

        :returns: requests_html.Response
    
    async def start_session():
        :returns: requests_html.AsyncHTMLSession

    async def create_tasks(urls, session):
        :urls: list[str]
        :session: requests_html.AsyncHTMLSession
        
        :returns: list[awaitables]

    """
    def __init__(self, urls: list[str]):
        self.urls = urls

    async def start_session(self, session=None) -> None:
        """
        Create a new session object.
        """
        try:
            session = requests_html.AsyncHTMLSession()
        except (Exception, requests_html.exceptions.RequestException) as exception:
            print(f'Cannot launch the session because: {exception}')
        else:
            return session

    async def get_request(self, url: str, session) -> None:
        """
        Send a request with the url.
        """
        try:
            response = await session.get(url)
            return response
        except (Exception) as exception:
            return None

    async def create_tasks(self, tasks=[]) -> list:
        """
        Apply getting a request to 
        each url and create a new
        task that goes to a list
        of tasks.
        """
        session = await self.start_session()
        for i in range(0, len(self.urls)):
            task = asyncio.create_task(self.get_request(self.urls[i], session))
            tasks.append(task)
        results = await asyncio.gather(*tasks)

        return results


class DataFetcher:
    """
    The object takes a list 
    of responses and returns
    a list of pythonic objects.

    
    async def extract_data(site_dict, item):
        :results: list[awaitables]
        :site_dict: dict[dict[str]]
        :item: str

        :returns: list[dict]
    
    """
    
    def __init__(self, urls: list[str], site_dict: dict[dict], item: str):
        self._web_manager = WebRequestManager(urls)
        self.site_dict = site_dict
        self.item = item

    async def extract_data(self, list_of_objs=[]) -> list[dict]:
        """
        Go through each response
        and scrape required data
        and return a bunch of 
        objects.
        """
        results = await self._web_manager.create_tasks()
        for i in range(0, len(results)):
            objects = results[i].html.xpath(self.site_dict[self.item]['object'])
            for j in range(0, len(objects)):
                obj = {
                    'title': objects[j].xpath(self.site_dict[self.item]['title'])[0],
                    'price': objects[j].xpath(self.site_dict[self.item]['price'])[0].text,
                    'image': objects[j].xpath(self.site_dict[self.item]['image'])[0],
                    'link': objects[j].xpath(self.site_dict[self.item]['link'])[0],
                }
                list_of_objs.append(obj)

        return list_of_objs
