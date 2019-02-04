from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormView
# from django.views import generic
from .forms import SearchForm
from .models import Prediction
from django.views import View
from urllib.parse import urlparse
from ImageQ.processor.search import GoogleSearch, YahooSearch, BingSearch


class SearchView(FormView):
    template_name = "search/index.html"
    error_template_name = "search/error.html"
    form_class = SearchForm
    success_url = '/results'

    def form_valid(self, form):
        # returns the prediction model and engine to use
        prediction, engine = form.predict()
        if not prediction:
            return render(self.request, self.error_template_name)
        return redirect(reverse('search:results', args=[prediction.id, engine, ]))


class ResultView(View):
    template_name = "search/results.html"
    # default handler is google search
    search_handler = GoogleSearch()

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
        if select_index < 0 or select_index >= 3:
            raise ValueError(f"prediction index {select_index} does not exist")
        else:
            top_prediction = prediction_list[select_index]
            for i in range(len(prediction_list)):
                if i != select_index:
                    prediction_list[i]["index"] = i
                    other_predictions.append(prediction_list[i])
            return top_prediction, other_predictions

    def search(self, search_term):
        """
        Utilize search parser to scrape google for results

        :param search_term: search term to use (obtained from prediction)
        :type search_term: str
        :return: dictionary [titles, links, netlocs and descriptions] and sucess value
        :rtype: dict, bool
        """
        search_results = self.search_handler.search(search_term, 1)
        search_success = True
        return search_results, search_success

    def get(self, request, pk, engine="Google", select_index=0):
        """
        Render results 

        :param request: request object
        :type request: `django.core.handlers.wsgi.WSGIRequest`
        :param pk: primary key of prediction object to retrieve
        :type pk: int
        :param engine: the search parsing engine to use for the search
        :type engine: str
        :param select_index: index of prediction to choose from (defaults to 0)
        :type select_index: int
        """
        if engine == "Google":
            self.search_handler = GoogleSearch()
        if engine=="Yahoo":
            self.search_handler = YahooSearch()
        if engine=="Bing":
            self.search_handler = BingSearch()

        prediction = Prediction.objects.get(pk=pk)
        image_url = prediction.image.url
        date_stored = prediction.date_stored
        top_prediction, other_predictions = ResultView.select_prediction(
            prediction_list=prediction.predictions["predictions"],
            select_index=select_index)
        probability = top_prediction["probability"]
        search_term = top_prediction["label"].replace("_", " ")
        main_args = {
            "image_url": image_url,
            "pk": pk,
            "search_term": search_term,
            "other_predictions": other_predictions,
            "other_predictions_range": range(len(other_predictions)),
            "select_index": select_index,
            "date_stored": date_stored,
            "probability": probability,
            "engine": engine,
        }
        try:
            search_results, search_success = self.search(search_term)
            return render(request, self.template_name, {
                **main_args,
                "range": range(len(search_results["titles"])),
                "search_success": search_success,
                "search_results": search_results,
            })

        except Exception as e:
            search_success = False
            error = e
            print(search_success)
            return render(request, self.template_name, {
                **main_args,
                "search_success": search_success,
                "error": error
            })
