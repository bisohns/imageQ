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
import numpy as np
from keras.applications.resnet50 import (ResNet50, decode_predictions,
                                         preprocess_input)
from keras.preprocessing import image
from ImageQ.processor.consts import FS, File, IMAGE_TYPES


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__all__ = [
    'BasePredictor', 'RequestHandler'
]

class BasePredictor(object):
    """This is the basic predictor extended by all other predictors
    """
    def __init__(self):
        """Constructor method
        """
        self.__metaclass__  = abc.ABCMeta
        self.model = ResNet50(weights='imagenet')

    @property
    def image_path(self):
        raise NotImplementedError


    def process_image(self):
        """Image preprocessing method for image at path

        :return processed: processed and resized image array
        :rtype: `np.ndarray`
        """
        img = image.load_img(self.image_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        processed = preprocess_input(x)
        
        return processed


    def get_prediction(self, top=3):
        """Returns the prediction for the image

        :param top: number of top classifications to return, defaults to 3
        :type top: int
        :return predictions: top predictions
        :rtype: list
        """
        predictions = list()
        preds = self.model.predict(self.process_image())
        for i in decode_predictions(preds, top=top)[0]:
            predictions.append(i[1])
        
        return predictions

class RequestHandler:
    """Request handler
    """
    def __init__(self, url, image_name):
        """Constructor

        :param url: link to image
        :type url: str
        :param image_name: final name of image when downloaded
        :type image_name: str
        """
        self.url = url
        self.http = urllib3.PoolManager()
        self.ret_val = self.http.request('GET', url)
        self.type = (self.ret_val.headers)['Content-Type']
        self.data = self.ret_val.data
        self.image_location = str(FS.SEARCH_CACHE + "/{0}.{1}").format(image_name, self.ext)
    
    @property
    def is_image(self):
        """Is resource at link an image?
        """
        if self.type in IMAGE_TYPES.keys():
            return True
        else:
            return False

    @property
    def ext(self):
        for i in IMAGE_TYPES.values():
            if self.type.endswith(i):
                return i

    def save(self):
        """Save the image
        """
        File.make_dirs(FS.SEARCH_CACHE)
        with open(self.image_location, 'wb') as stream:
            stream.write(self.data)

if __name__ == "__main__":
    a = RequestHandler("https://images.pexels.com/photos/67636/rose-blue-flower-rose-blooms-67636.jpeg?cs=srgb&dl=beauty-bloom-blue-67636.jpg&fm=jpg", "test_flower")
    a.save()