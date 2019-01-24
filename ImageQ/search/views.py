from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import SearchForm


class SearchView(FormView):
    template_name = "search/index.html"
    form_class = SearchForm
    success_url = '/results'

    def form_valid(self, form):
        # the form predict values should be added to context and passed to the result rendering view
        prediction_results = form.predict()
        return reverse('results', kwargs={'prediction_results': prediction_results})


class ResultView(TemplateView):

    def get_context_data(self, *args, **kwargs):
        print(*args, **kwargs)
        context = super().get_context_data(**kwargs)
        return context
