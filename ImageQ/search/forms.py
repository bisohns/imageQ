from django import forms

class SearchForm(forms.Form):
    image = forms.ImageField()
    url = forms.URLField()

    def clean_image(self):
        "validate uploaded image"
        pass

    def clean_url(self):
        pass
