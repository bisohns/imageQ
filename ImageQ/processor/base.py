"""@desc 
        Provides base architectures to be extended:
        BasePredictor and BaseHandler

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
import uuid
from abc import ABCMeta, abstractmethod
from io import BytesIO

import numpy as np
import requests

from django.core import files
from ImageQ.processor.consts import FS, IMAGE_TYPES, File
from ImageQ.search.models import Prediction


__all__ = [
    'BasePredictor',
    'BaseHandler',
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