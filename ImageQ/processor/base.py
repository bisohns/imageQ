"""@desc 
        Provides base architectures to be extended:
        BasePredictor, BaseSearch and BaseHandler

     @author 
         Domnan Diretnan
         Artificial Intelligence Enthusiast & Software Engineer.
         Email: diretnandomnan@gmail.com
         Github: https://github.com/deven96
         GitLab: https://gitlab.com/Deven96

         Manasseh Mmadu
         Email: mmadumanasseh@gmail.com
         Github: https://github.com/MeNsaaH
         Gitlab: https://gitlab.com/MeNsaaH

     @project
         @create date 2018-12-28 02:03:05
         @modify date 2018-12-28 02:18:59

    @license
        MIT License
        Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """
import abc
import uuid
from abc import ABCMeta, abstractmethod
from io import BytesIO
from urllib.parse import urlparse

import numpy as np
import requests
from bs4 import BeautifulSoup

from ImageQ.processor.consts import FS, IMAGE_TYPES, SEARCH_QUERY
from ImageQ.search.models import Prediction


__all__ = [
    'BaseSearch',
    'BasePredictor',
    'BaseHandler',
]


class BaseSearch(object):

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
        raise NotImplementedError(
            "subclasses must define method <parse_results>")

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
            title = link = desc = netloc = " "
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

    # TODO Use urllib's parse url
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
    def get_source(url):
        """
        Returns the source code of a webpage.

        :rtype: string
        :param url: URL to pull it's source code
        :return: html source code of a given URL.
        """
        import requests
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        # prevent caching
        headers = {'Cache-Control': 'no-cache'}
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
        query = BaseSearch.parse_query(raw_query)
        search_fmt_string = SEARCH_QUERY[engine]
        if engine == "Google":
            search_url = search_fmt_string.format(query, page)
        if engine == "Yahoo":
            offset = (page * 10) - 9
            search_url = search_fmt_string.format(query, offset)
        if engine=="Bing":
            # structure pages in terms of 
            first= (page * 10) - 9
            search_url = search_fmt_string.format(query, first)
        html = BaseSearch.get_source(search_url)
        return BeautifulSoup(html, 'lxml')


class BasePredictor(object):
    """This is the basic predictor extended by all other predictors
        Two main properties/attributes must be declared by subclasses

        image_path[str]: path to the image saved locally
        prediction_api[str]: url of the AI prediction API predict route

    """

    def __init__(self):
        """Constructor method
        """
        self.__metaclass__ = abc.ABCMeta
        self.prediction_api = None

    @property
    def image_path(self):
        raise NotImplementedError

    def predict(self):
        """ send requests to the prediction api

        :returns: json response from the api
        :rtype: dict
        """
        files = {'image': open(self.image_path, 'rb')}
        if not isinstance(self.prediction_api, type(None)):
            r = requests.post(self.prediction_api, files=files)
        else:
            raise AttributeError("Attribute <prediction_api> is of type None")
        return r.content


class BaseHandler(object):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def image_data(self):
        return NotImplementedError("self.image_data must be defined")

    @property
    @abstractmethod
    def ext(self):
        return NotImplementedError("self.ext must be defined")

    def save(self):
        """Save the image in the Prediction Model
        """
        image_name = uuid.uuid1().hex
        prediction = Prediction()
        # Save the Image without Downloading it
        prediction.image.save(f'{image_name}.{self.ext}', self.image_data)
        return prediction
