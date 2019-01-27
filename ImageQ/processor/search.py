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


class Search(object):
    """
    """

    def __init__(self):
        self.googleSearchURL = 'https://www.google.com/search?q={}&start={}'

    def search(self, query, page):
        """
        Parses Google for a search query.
        :param query: Search query sentence or term
        :type query: string
        :param page: Page to be displayed.
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        # replace spaces in query string
        query = query.replace(" ", "%20")
        self.googleSearchURL = self.googleSearchURL.format(query, page)
        html = Search.getSource(self.googleSearchURL)
        soup = BeautifulSoup(html, 'lxml')
        # # find all class_='g' => each result
        results = soup.find_all('div', class_='g')
        if not results:
            raise ValueError("The result parsing was unsuccessful, flagged as unusual traffic")
        titles = []
        links = []
        netlocs = []
        descs = []
        for each in results:
            title=link=desc=netloc = " "
            try:
                title, link, desc = Search.parse_results(each)
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
    def parse_results(single_result):
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


if __name__ == '__main__':
    search = Search()
    results = search.search('preaching to the choir', 1)
    print(results)