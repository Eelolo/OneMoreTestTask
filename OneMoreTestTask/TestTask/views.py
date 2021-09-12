from django.shortcuts import render
from django.views import View
from .forms import FilterForm


class IndexPageView(View):
    def get(self, request):
        form = FilterForm()

        return render(request, 'index.html', {'form': form})

    def post(self, request):
        pass
