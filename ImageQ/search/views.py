from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormView
# from django.views import generic
from .forms import SearchForm
from .models import Prediction
from django.views import View



class SearchView(FormView):
    template_name = "search/index.html"
    form_class = SearchForm
    success_url = '/results'

    def form_valid(self, form):
        prediction = form.predict()
        if not prediction:
            return HttpResponse('Something Just happened right now')
        return redirect(reverse('search:results', args=[prediction.id, ]))


class ResultView(View):
    template_name = "search/results.html"

    def get(self, request, pk):
        """ Render results """
        return render(request, self.template_name, {'prediction': Prediction.objects.get(pk=pk) })

