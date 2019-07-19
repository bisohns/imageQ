"""@desc 
        Predictors definition -> URL and Upload

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
         @create date 2018-12-28 02:03:47
         @modify date 2018-12-28 02:03:47

    @license
        MIT License
        Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """

from ImageQ.processor.base import BasePredictor

class URLPredictor(BasePredictor):
    """This is a URL class predictor for the ResNet model 

    :param prediction_api: url of the prediction api to send requests to
    :type prediction_api: str
    :param image: image to be predicted
    :type image: `django.db.models.fields.files.ImageFieldFile`

    Example:
        >>> from ImageQ.search.models import Prediction
        >> prediction_model = Prediction.objects.get(pk=1)
        >>> predictor = URLPredictor(prediction_api="172.104.78.30/predict", image=prediction_model.image)
        >>> predictor.predict()
    """
    def __init__(self, prediction_api, image):
        """ Constructor method
        """
        self.prediction_api = prediction_api
        self.image = image

    @property
    def image_path(self):
        """Image path from url downloaded by urllib3
        
        :returns: path of the image
        :rtype: str
        """
        return self.image.path

