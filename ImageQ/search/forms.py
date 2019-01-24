from django import forms

class SearchForm(forms.Form):
    image = forms.ImageField()
    url = forms.URLField(widget=forms.TextInput(attrs={placeholder:"Enter a url to an Image"})

    def clean_image(self):
        "validate uploaded image"
        pass

    def clean_url(self):
        pass
