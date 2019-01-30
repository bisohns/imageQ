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

from ImageQ.processor.base import BaseSearch


class GoogleSearch(BaseSearch):
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

class YahooSearch(BaseSearch):
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

