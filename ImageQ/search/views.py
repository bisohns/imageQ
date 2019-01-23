from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from ImageQ.processor.predictors import URLPredictor
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """ Default index view
    """
    template_name = "search/index.html"

class SearchView(View):
    """Handles the incoming image url passed from index page
    """
    def post(self, request):
        querydict = request.POST.dict()
        # create a urlpredictor using the url in the im=search field 
        urlpredictor = URLPredictor(
                        prediction_api=settings.PREDICTION_API,
                        image_url=querydict["im-search"])
        print(urlpredictor.predict())
        return render(request, "search/index.html")