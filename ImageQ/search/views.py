from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from ImageQ.processor.predictors import URLPredictor
from django.views import View
from django.views.generic.edit import FormView
from .forms import SearchForm


# class SearchView(View):
    # def post(self, request):
        # querydict = request.POST.dict()
        # urlpredictor = URLPredictor(
                        # prediction_api=settings.PREDICTION_API,
                        # image_url=querydict["im-search"])
        # print(urlpredictor.predict())
        # return render(request, "search/index.html")

class SearchView(FormView):
    template_name = "search/index.html"
    form_class = SearchForm
    success_url = '/results'

    def form_valid(self, form):
        print(form.data);
        return super().form_valid(form)
