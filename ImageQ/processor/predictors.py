"""@desc 
        Predictors definition -> URL and Upload

     @author 
         Domnan Diretnan
         Artificial Intelligence Enthusiast & Software Engineer.
         Email: diretnandomnan@gmail.com
         Github: https://github.com/deven96
         GitLab: https://gitlab.com/Deven96

     @project
         @create date 2018-12-28 02:03:47
         @modify date 2018-12-28 02:03:47

    @license
        MIT License
        Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """


import urllib3
from ImageQ.processor.base import BasePredictor, RequestHandler
from keras.applications.resnet50 import decode_predictions  

# decode the results into a list of tuples (class, description, probability)
# (one such list for each sample in the batch)
print('Predicted:', decode_predictions(preds, top=3)[0])

class URLPredictor(BasePredictor):
    """This is a URL class predictor for the ResNet model 

    :param image_url: url to the image to be predicted
    :type image_url: str
    """
    def __init__(self, image_url):
        """Constructor method
        """
        self.image_url = image_url
        self.request_handler = RequestHandler(self.image_url, "current")

    @property
    def image_path(self):
        """Image path from url downloaded by urllib3
        """
        if self.request_handler.is_image:
            return self.request_handler.image_path
        else:
            raise TypeError(f"Expected one of image/(png, jpeg, jpg) \
                            Got {self.request_handler.type}")


class UploadPredictor(BasePredictor):
    """This is an Upload class predictor for the ResNet model 

    :param image_location: url to the image to be predicted
    :type image_location: str
    """
    pass

