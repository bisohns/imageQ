from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from ImageQ.processor.predictors import URLPredictor
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "search/index.html"

class SearchView(View):
    def post(self, request):
        querydict = request.POST.dict()
        urlpredictor = URLPredictor(
                        prediction_api=settings.PREDICTION_API,
                        image_url=querydict["im-search"])
        print(urlpredictor.predict())
        return render(request, "search/index.html")