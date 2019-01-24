"""@desc 
        Base Architecture, Reuest Handlers and Logger for Predictors

     @author 
         Domnan Diretnan
         Artificial Intelligence Enthusiast & Software Engineer.
         Email: diretnandomnan@gmail.com
         Github: https://github.com/deven96
         GitLab: https://gitlab.com/Deven96

     @project
         @create date 2018-12-28 02:03:05
         @modify date 2018-12-28 02:18:59

    @license
        MIT License
        Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """
import abc
import urllib3
import requests
import numpy as np
from ImageQ.processor.consts import FS, File, IMAGE_TYPES


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__all__ = [
    'BasePredictor', 'RequestHandler'
]

class BasePredictor(object):
    """This is the basic predictor extended by all other predictors
        Two main properties/attributes must be declared by subclasses

        image_path[str]: path to the image saved locally
        prediction_api[str]: url of the AI prediction API predict route

    """
    def __init__(self):
        """Constructor method
        """
        self.__metaclass__  = abc.ABCMeta
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

class RequestHandler:
    """Request handler
    """
    def __init__(self, image_url, image_name):
        """Constructor

        :param image_url: link to image
        :type image_url: str
        :param image_name: final name of image when downloaded
        :type image_name: str
        """
        self.image_url = image_url
        self.http = urllib3.PoolManager()
        self.ret_val = self.http.request('GET', image_url)
        # image type
        self.type = (self.ret_val.headers)['Content-Type']
        # image data
        self.data = self.ret_val.data
        # image location
        self.image_location = str(FS.SEARCH_CACHE + "/{0}.{1}").format(image_name, self.ext)

    def save(self):
        """Save the image
        """
        File.make_dirs(FS.SEARCH_CACHE)
        with open(self.image_location, 'wb') as stream:
            stream.write(self.data)
