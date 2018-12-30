from django.http import HttpResponse
from django.views.generic import TemplateView
from ImageQ.processor.predictors import URLPredictor


class IndexView(TemplateView):
    template_name = "search/index.html"

    def get(self, request):
        """classify the image at the url using processor handler
        """
        if request.method == "GET":
            url = request.GET.get('im-search')
            if url != None :
                predictor = URLPredictor(image_url=url)
                #get top predictions
                predictions = predictor.get_prediction()
                html = f"<html><body>Top posibilities are {predictions}</body></html>"
                return HttpResponse(html)
