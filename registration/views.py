from django.shortcuts import render
from django.views.generic import TemplateView


# test
class HomeView(TemplateView):
    template_name = "index.html"

    def get(self, request):
        # return render(request, "index.html", {})
        return render(request, self.template_name, {})
