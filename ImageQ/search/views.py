from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views import generic
from .forms import SearchForm
from .models import Prediction


class SearchView(FormView):
    template_name = "search/index.html"
    form_class = SearchForm
    success_url = '/results'

    def form_valid(self, form):
        prediction = form.predict()
        if not prediction:
            return HttpResponse('Something Just happened right now')
        return reverse('search:results', args=(prediction.id, ))


class ResultView(generic.DetailView):
    model = Prediction
    context_object_name = 'prediction'
    template_name = "search/results.html"

