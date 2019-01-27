from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormView
# from django.views import generic
from .forms import SearchForm
from .models import Prediction
from django.views import View
from urllib.parse import urlparse
from ImageQ.processor.search import Search



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
        prediction = Prediction.objects.get(pk=pk)
        image_url = prediction.image.url
        date_stored = prediction.date_stored
        top_prediction = prediction.predictions["predictions"][0]
        other_predictions = prediction.predictions["predictions"][1:]
        probability = top_prediction["probability"]
        search_term = top_prediction["label"].replace("_", " ")
        try:
            google_search_handler = Search()
            search_results = google_search_handler.search(search_term, 1)
            search_sucess = True
            return render(request, self.template_name, {'image_url': image_url, 
                                "search_success": search_sucess,
                                "search_term": search_term,
                                "range": range(len(search_results["titles"])),
                                "search_results": search_results,
                                "other_predictions": other_predictions,
                                "date_stored": date_stored,
                                "probability": probability,
                                })
        except:
            search_sucess = False
            return render(request, self.template_name, {'image_url': image_url, 
                                "search_success": search_sucess,
                                "search_term": search_term,
                                "other_predictions": other_predictions,
                                "date_stored": date_stored,
                                "probability": probability,
                                })

