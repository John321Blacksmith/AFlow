import sys
import time
import asyncio
import pandas as pd
import requests_html
from urllib.parse import urljoin
from requests_html import AsyncHTMLSession

sys.path.append('..\\..\\configs\\html_tags')
from scraping_info import books


class LinksLoadingManager:
    """
    The object takes a list of
    parsed links in order to 
    save them all to the csv file
    and, as the next step, pulls
    them out from the file to use
    each one in sending a request
    to the server.

    async def save_links(source, file_name):
        :source: str
        :file_name: str
        :returns: str
    
    async def retrieve_links(file_name):
        :file_name: str
        :returns: list[str]

    """
    def __init__(self, path_to_csv):
        self.path_to_csv = path_to_csv
        

    async def save_links(self, parsed_links: list[str]) -> bool:
        """
        Take a list of links and
        save each one to the disk.
        """
        try:
            with open(self.path_to_csv, mode='w') as f:
                df = pd.DataFrame(data=parsed_links)
                df.to_csv(f, header=False, index=False, lineterminator='\n')
        except (Exception, FileNotFoundError) as error:
            return False
        else:
            return True

    async def retrieve_links(self, links=[]) -> list[str]:
        """
        Read the file where the links are
        stored and pull each one out to the list.
        """
        try:
            with open(self.path_to_csv, mode='r') as f:
                links_frame = pd.read_csv(f, header=None)
                for i in range(0, len(links_frame[0])):
                    links.append(links_frame[0][i])
        except (Exception, FileNotFoundError) as error:
            print(f'Couldn\'t perform operation because {error}')
        else:
            return links

    def csv_is_full(self) -> bool:
        """
        Check if the file has already
        been stuffed with the links.
        """
        try:
            with open(self.path_to_csv, mode='r') as f:
                try:
                    links_frame = pd.read_csv(f, header=None)
                except pd.errors.EmptyDataError:
                    return False
                else:
                    return True
        except FileNotFoundError as error:
            print('No such file or directory')


class WebRequestManager:
    """
    The object takes a list of
    urls and sends async requests
    to each of them and returns
    a list of responses.

    Every time the object is
    created, a new session object
    is initialized for requests.

    async def get_request(url, session):
        :url: str
        :session: requests_html.AsyncHTMLSession

        :returns: requests_html.Response

    async def create_tasks(urls, session):
        :urls: list[str]
        :session: requests_html.AsyncHTMLSession
        
        :returns: list[awaitables]

    """
    def __init__(self):
        """
        Start a new session each time
        the object is initialized.
        """
        self._session = None
        try: 
            self._session = requests_html.AsyncHTMLSession()
        except (Exception, requests_html.exceptions.RequestException) as exception:
            print(f'Cannot establish connection because {exception}')

    async def get_response(self, url: str) -> None:
        """
        Send a request with the url.
        """
        try:
            response = await self._session.get(url)
            return response
        except (Exception) as exception:
            return None

    async def create_tasks(self, urls: list[str], tasks=[]) -> list:
        """
        Apply getting a request to 
        each url and create a new
        task that goes to a list
        of tasks.
        """
        for i in range(0, len(urls)):
            task = asyncio.create_task(self.get_response(urls[i]))
            tasks.append(task)
        results = await asyncio.gather(*tasks)

        return results

class WebCrawler:
    """
    This object picks all
    the links from a web
    site and returns a 
    list of them.

    async def crawl_links(url:str, counter=1):
        :url: str
        :counter: 1, int
        :returns: list[str]

    """
    def __init__(self, site_dict: dict):
        self.site_dict = site_dict
        self.web_manager = WebRequestManager()
        self.crawled_links = []

    async def crawl_links(self, url, counter=1) -> list[str]:
        """
        Go to a particular url
        and extract all the
        next page elements
        using an amount of 
        them to jump on another.
        """
        response = await self.web_manager.get_response(url)
        next_page_elements = response.html.find(self.site_dict['n_p_element'])

        amount = len(next_page_elements)
        
        if amount != 0:
            for i in range(0, amount):
                self.crawled_links.append(urljoin(self.site_dict['source'], next_page_elements[i].attrs['href']))
            counter += amount
            return await self.crawl_links(f'{self.site_dict["source"]}{self.site_dict["n_p_slug"]}{counter}', counter)
        else:
            return self.crawled_links

    async def extract_links(self, url: str) -> list[str]:
        """
        Go through each page and
        parse its url recursively.
        """
        self.crawled_links.append(url)
        response = await self.web_manager.get_response(url)
        next_page_slug = response.html.find(self.site_dict['n_p_element'])
        
        if next_page_slug:
            url = urljoin(url, next_page_slug[0].attrs['href'])
            return await self.extract_links(url) # recursive case
        else:
            return self.crawled_links # base case
 

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

    async def extract_links(site_dict, source):
        :site_dict: dict[dict]
        :source: str
        :returns: list[str]
    
    """
    
    def __init__(self, site_dict: dict[dict]):
        self.site_dict = site_dict
        self.web_manager = WebRequestManager()
        self.crawled_links = []
        

    async def extract_data(self, urls:list[str], list_of_objs=[], local=False) -> list[dict]:
        """
        Go through each response
        and scrape required data
        and return a bunch of 
        objects.
        """
        if local:
            results
        else:
            results = await self.web_manager.create_tasks(urls)
        for i in range(0, len(results)):
            objects = results[i].html.xpath(self.site_dict['object'])
            for j in range(0, len(objects)):
                obj = {
                    'title': objects[j].xpath(self.site_dict['title'])[0],
                    'price': objects[j].xpath(self.site_dict['price'])[0].text,
                    'image': urljoin(self.site_dict['source'], objects[j].xpath(self.site_dict['image'])[0]),
                    'link': urljoin(self.site_dict['source'], objects[j].xpath(self.site_dict['link'])[0]),
                }
                list_of_objs.append(obj)

        return list_of_objs



async def main():
    csv = '..\\..\\instant_files\\links.csv'
    # classes instantiation
    webcrawler = WebCrawler(site_dict=books)
    links_manager = LinksLoadingManager(path_to_csv=csv)
    # objects activities
    # checking if the csv file is full
    if links_manager.csv_is_full():
        print('it is full.\nthe webcrawler is idle. Using this file...')
        links = await links_manager.retrieve_links()
    else:
        print('it is empty, the webcrawler\'s gonna work...')
        links = await webcrawler.extract_links(webcrawler.site_dict['source'])
        await links_manager.save_links(parsed_links=links)



    # throwing requests to the server & scraping the HTMLs
    print('Parsing the data\n')
    print('initializing the scraper...')
    data_fetcher = DataFetcher(site_dict=books)
    time.sleep(2)
    objects = await data_fetcher.extract_data(urls=links)
    print('extracting the objects...\n\n\n\n')
    time.sleep(5)
    print('THE RESULT IS BELOW\n')
    try:
        for i in range(0, len(objects)):
            for key, value in objects[i].items():
                print(key + ' ::: ' + str(value))
            print('\n\n')
    except IndexError:
        print('No items found')


if __name__ == '__main__':
    asyncio.run(main())