from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from ImageQ.processor.predictors import URLPredictor
from django.views import View
from django.views.generic.edit import FormView
from .forms import SearchForm


class SearchView(FormView):
    template_name = "search/index.html"
    form_class = SearchForm
    success_url = '/results'

    def form_valid(self, form):
        # the form predict values should be added to context and passed to the result rendering view
        form.predict()
        return super().form_valid(form)
