import asyncio
import pandas
import requests_html
from urllib.parse import urljoin
from requests_html import AsyncHTMLSession
from scraping_info import scraping_data, auction_site


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
    def __init__(self, site_dict: dict[dict]):
        self.site_dict = site_dict
        

    async def save_links(self, parsed_links: list[str]) -> None:
        """
        Take a list of links and
        save each one to the disk.
        """
        try:
            with open(self.site_dict['links_file'], mode='w') as f:
                for link in parsed_links:
                    f.write(link + '\n')
        except (Exception, FileNotFoundError) as error:
            print(f'Couldn\'t save data because {error}')
        else:
            print(f'The links have been saved to the file {f.name}')

    async def retrieve_links(self, links=[]) -> list[str]:
        """
        Read the file where the links are
        stored and pull each one out to the list.
        """
        try:
            with open(self.site_dict['links_file'], newline='') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    links.append(row[0])
        except (Exception, FileNotFoundError) as error:
            print(f'Couldn\'t perform operation because {error}')
        else:
            return links


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

    async def extract_links(self, url: str):
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
        

    async def extract_data(self, urls:list[str], list_of_objs=[]) -> list[dict]:
        """
        Go through each response
        and scrape required data
        and return a bunch of 
        objects.
        """
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
    webcrawler = WebCrawler(auction_site)
    links = await webcrawler.extract_links(auction_site['source'])
    print(links)


if __name__ == '__main__':
    asyncio.run(main())