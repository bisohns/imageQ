"""@desc 
		Parser for google search results

 	@author 
 		Domnan Diretnan
 		Artificial Intelligence Enthusiast & Software Engineer.
 		Email: diretnandomnan@gmail.com
 		Github: https://github.com/deven96
 		GitLab: https://gitlab.com/Deven96

 	@project
 		@create date 2019-01-26 23:14:22
 		@modify date 2019-01-26 23:14:22

	@license
		MIT License
		Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from abc import ABCMeta, abstractmethod

from ImageQ.processor.consts import SEARCH_QUERY

SEARCH_QUERY = {
    "Google": 'https://www.google.com/search?q={}&start={}',
    "Yahoo": 'https://search.yahoo.com/search?p={}&b={}'
}



class SearchBase(object):

    __metaclass__ = ABCMeta

    """
    Search base to be extended by search parsers
    Every subclass must have two methods `search` amd `parse_single_result`
    """

    @abstractmethod
    def search(self, query, page=1):
        """
        Master method coordinating search parsing
        """
        raise NotImplementedError("subclasses must define method <search>")

    @abstractmethod
    def parse_single_result(self, single_result):
        """
        Every div/span containing a result is passed here to retrieve
        `title`, `link` and `descr`
        """
        raise NotImplementedError("subclasses must define method <parse_results>")
    
    def parse_result(self, results):
        """
        Runs every entry on the page through parse_single_result

        :param results: Result of main search to extract individual results
        :type results: list[`bs4.element.ResultSet`]
        :returns: dictionary. Containing titles, links, netlocs and descriptions.
        :rtype: dict
        """
        titles = []
        links = []
        netlocs = []
        descs = []
        for each in results:
            title=link=desc=netloc = " "
            try:
                title, link, desc = self.parse_single_result(each)
                netloc = urlparse(link).netloc
                ''' Append links and text to a list '''
                titles.append(title)
                links.append(link)
                netlocs.append(netloc)
                descs.append(desc)
            except Exception as e:
                print(e)
        search_results = {'titles': titles,
                          'links': links,
                          'netlocs': netlocs,
                          'descriptions': descs}
        return search_results
    
    @staticmethod
    def parse_query(query):
        """
        Replace spaces in query

        :param query: query to be processed
        :type query: str
        :rtype: str
        """
        return query.replace(" ", "%20")
    
    @staticmethod
    def getSource(url):
        """
        Returns the source code of a webpage.

        :rtype: string
        :param url: URL to pull it's source code
        :return: html source code of a given URL.
        """
        import requests
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        # prevent caching
        headers={'Cache-Control': 'no-cache'}
        try:
            response = requests.get(url, headers=headers)
            html = response.text
        except Exception as e:
            raise Exception('ERROR: {}\n'.format(e))
        return str(html)   

    @staticmethod
    def get_soup(raw_query, engine="Google", page=1):
        """
        Get the html soup of a query

        :param raw_query: unprocessed query string
        :type raw_query: str
        :param engine: search engine to make use of, defaults to google
        :type engine: str
        :param page: page to return
        :type page: int
        :rtype: `bs4.element.ResultSet`
        """
        # replace spaces in string
        query = SearchBase.parse_query(raw_query)
        search_fmt_string = SEARCH_QUERY[engine]
        if engine=="Google":
            search_url = search_fmt_string.format(query, page)
        if engine=="Yahoo":
            offset = (page * 10) - 9
            search_url = search_fmt_string.format(query, offset)
        html = SearchBase.getSource(search_url)
        return BeautifulSoup(html, 'lxml')



class GoogleSearch(SearchBase):
    """
    Searches Google for string
    """
    def search(self, query, page=1):
        """
        Parses Google for a search query.

        :param query: Search query sentence or term
        :type query: string
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        soup = GoogleSearch.get_soup(query, engine="Google", page=page)
        # # find all class_='g' => each result
        results = soup.find_all('div', class_='g')
        if not results:
            raise ValueError("The result parsing was unsuccessful, flagged as unusual traffic")
        search_results = self.parse_result(results)
        return search_results

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="g">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h3 = single_result.find('h3', class_='r')
        link_tag = h3.find('a')
        desc = single_result.find('span', class_='st')
        ''' Get the text and link '''
        title = h3.text

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        raw_link = link_tag.get('href')
        dead_index = raw_link.find("&sa=")
        link = raw_link[7:dead_index]

        desc = desc.text
        return title, link, desc

class YahooSearch(SearchBase):
    """
    Searches Yahoo for string
    """
    def search(self, query, page=1):
        """
        Parses Google for a search query.

        :param query: Search query sentence or term
        :type query: string
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        soup = YahooSearch.get_soup(query, engine="Yahoo", page=page)
        # find all divs
        results = soup.find_all('div', class_='Sr')
        if not results:
            raise ValueError("The result parsing was unsuccessful, flagged as unusual traffic")
        search_results = self.parse_result(results)
        return search_results 

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="Sr">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h3 = single_result.find('h3', class_='title')
        link_tag = h3.find('a')
        desc = single_result.find('p', class_='lh-16')
        ''' Get the text and link '''
        title = h3.text

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        link = link_tag.get('href')

        desc = desc.text
        return title, link, desc


if __name__ == '__main__':
    search_args = ('preaching to the choir', 3)
    gsearch = GoogleSearch()
    ysearch = YahooSearch()
    gresults = gsearch.search(*search_args)
    yresults = ysearch.search(*search_args)
    print(yresults["titles"][1])
    print(gresults["titles"][1])

