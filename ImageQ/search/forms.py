import json
import http.client
from django import forms
from django.conf import settings
from urllib.parse import urlparse
from ImageQ.processor.predictors import URLPredictor, RequestHandler
from ImageQ.search.models import Prediction

class SearchForm(forms.Form):
    image_type = ""
    image = forms.ImageField(required=False)
    url = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['placeholder'] = "Enter a url to an Image"

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url: 
            return
        if not self.validate_url_resource(url):
            raise forms.ValidationError('URL does not contain a valid image')
        return url

    def validate_url_resource(self, url):
        """ Verifies that a url contains image data"""
        parse_url = urlparse(url)
        # Establish connection to the Image Resource
        try:
            conn = http.client.HTTPConnection(parse_url.netloc)
            conn.request("HEAD", parse_url.path)
            res = conn.getresponse()
        except:
            raise forms.ValidationError('Could not verify Image Resource')
        else:
            for e in res.getheaders():
                if e[0] == 'Content-Type':
                    if e[1].split('/')[0] == 'image':
                        self.image_type = e[1].split('/')[1]
                        return True
                # For Redirects and shortened URLS
                if e[0] == 'location':
                    self.validate_url_resource(e[1])
                    break
        return

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        url = cleaned_data.get('url')

        if not (url or image):
            raise forms.ValidationError("You must provide either an image or a url to an image")
        return cleaned_data

    def predict(self):
        """ Run the prediction over the uploaded image/ URL 
        """
        url = self.cleaned_data.get('url')
        image = self.cleaned_data.get('image')
        if url: 
            image_data = { "url": url, "ext": self.image_type }
            prediction = None
            # Downloads the Image
            try: 
                req = RequestHandler(image_data)
            except Exception as e:
                raise(e)
            else:
                # Get the Downloaded Image Model for prediction
                prediction_model = req.save()
                # Predicts the IMage and stores data in database
                urlpredictor = URLPredictor(
                               prediction_api=settings.PREDICTION_API,
                               image=prediction_model.image)
                # Store the decoded JSON Predictions
                _predictions = json.loads(bytes.decode(urlpredictor.predict()))
                prediction_model.predictions = _predictions
                prediction_model.save()
                prediction = prediction_model
        return prediction
        
