"""@desc 
		Handlers for each scenario, e.g upload 

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
 		@create date 2019-01-30 21:18:30
 		@modify date 2019-01-30 21:18:30

	@license
		MIT License
		Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """
import uuid
from io import BytesIO

import requests

from django.core import files
from ImageQ.processor.base import BaseHandler
from ImageQ.search.models import Prediction


class RequestHandler(BaseHandler):
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
            raise Exception("Something just happened Right Now")
        self.fp = BytesIO()
        self.fp.write(response.content)

    @property
    def ext(self):
        return self.image.get('ext')

    @property
    def image_data(self):
        return files.File(self.fp)


class UploadHandler(BaseHandler):
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
        print(self.image)

    @property
    def ext(self):
        return self.image.content_type[7:]
    
    @property
    def image_data(self):
        return self.image
