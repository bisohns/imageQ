"""@desc 
        Base Architecture, Request Handlers and Logger for Predictors

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
from django.core import files
from io import BytesIO
import requests
import numpy as np
from ImageQ.processor.consts import FS, File, IMAGE_TYPES
from ImageQ.search.models import Prediction



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
    def __init__(self, image):
        """Constructor

        :param image:  A dictionary containing image data including it's url, type
        :type image: dict
        :param image_name: final name of image when downloaded
        :type image_name: str
        """
        self.image = image
        response = requests.get(image.get('url'))
        if response.status_code != requests.codes.ok:
            return Exception("Something just happened Right Now")
        self.fp = BytesIO()
        self.fp.write(response.content)

    def save(self):
        """Save the image in the Prediction Model
        """
        # Generate a random string as file_name
        image_name = uuid.uuid1().hex
        prediction = Prediction()
        # Save the Image without Downloading it
        prediction.image.save(f'{image_name}.{self.image.get("ext")}', files.File(self.fp))
        return prediction

class UploadHandler:
    """
    Uploaded Image Handler

    :param image: image to initialize class with
    :tyoe image: `django.core.files.uploadedfile.InMemoryUploadedFile`
    """
    def __init__(self, image):
        if image:
            self.image = image
        else:
            raise AttributeError(f"cannot init class with image of type {type(image)}")
        if self.image.content_type.startswith("image/"):
            self.ext = self.image.content_type[7:]
        else:
            raise ValueError("content-type <image/*> expected")

    def save(self):
        """Save the image in the Prediction Model
        """
        image_name = uuid.uuid1().hex
        prediction = Prediction()
        # Save the Image without Downloading it
        prediction.image.save(f'{image_name}.{self.ext}', self.image)
        return prediction
