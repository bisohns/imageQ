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

    @staticmethod
    def select_prediction(prediction_list, select_index):
        """
        Selects the right prediction from the prediction list

        :param prediction_list: list of predictions
        :type prediction_list: list
        :param select_index: index of prediction to choose from
        :type select_index: int
        :returns: dict of chosen prediction, list of other predictions
        :rtype: dict, list
        """
        other_predictions = list()
        # only 3 predictions are ever returned from API
        if select_index<0 or select_index >=3:
            raise ValueError(f"prediction index {select_index} does not exist")
        else:
            top_prediction = prediction_list[select_index]
            for i in range(len(prediction_list)):
                if i != select_index:
                    other_predictions.append(prediction_list[i])
            return top_prediction, other_predictions


    @staticmethod
    def search(search_term):
        """
        Utilize search parser to scrape google for results

        :param search_term: search term to use (obtained from prediction)
        :type search_term: str
        :return: dictionary [titles, links, netlocs and descriptions] and sucess value
        :rtype: dict, bool
        """
        google_search_handler = Search()
        search_results = google_search_handler.search(search_term, 1)
        search_success = True
        return search_results, search_success

    def get(self, request, pk, select_index=0):
        """
        Render results 
        
        :param request: request object
        :type request: `django.core.handlers.wsgi.WSGIRequest`
        :param pk: primary key of prediction object to retrieve
        :type pk: int
        :param select_index: index of prediction to choose from (defaults to 0)
        :type select_index: int
        """
        prediction = Prediction.objects.get(pk=pk)
        image_url = prediction.image.url
        date_stored = prediction.date_stored
        top_prediction, other_predictions = ResultView.select_prediction(
                        prediction_list=prediction.predictions["predictions"],
                        select_index=select_index)
        probability = top_prediction["probability"]
        search_term = top_prediction["label"].replace("_", " ")
        try:
            search_results, search_success = ResultView.search(search_term)
            return render(request, self.template_name, {'image_url': image_url, 
                                "search_success": search_success,
                                "search_term": search_term,
                                "range": range(len(search_results["titles"])),
                                "search_results": search_results,
                                "other_predictions": other_predictions,
                                "date_stored": date_stored,
                                "probability": probability,
                                })
        except:
            search_success = False
            return render(request, self.template_name, {'image_url': image_url, 
                                "search_success": search_success,
                                "search_term": search_term,
                                "other_predictions": other_predictions,
                                "date_stored": date_stored,
                                "probability": probability,
                                })

