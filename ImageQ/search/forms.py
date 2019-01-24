from django import forms
import http.client
from urllib.parse import urlparse

class SearchForm(forms.Form):
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
        conn = http.client.HTTPConnection(parse_url.netloc)
        conn.request("HEAD", parse_url.path)
        res = conn.getresponse()
        for e in res.getheaders():
            if e[0] == 'Content-Type':
                if e[1].split('/')[0] == 'image':
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




 
