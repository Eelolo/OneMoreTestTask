from django.shortcuts import render
from django.views import View
from .forms import FilterForm


class IndexPageView(View):
    def get(self, request):
        form = FilterForm()

        return render(
            request, 'index.html',
            {'form': form, 'message': 'Click the calculate button to see detailed information'}
        )

    def post(self, request):
        form = FilterForm()
        deals_info, currencies_info = self.get_detailed_info(request)

        return render(
            request, 'index.html',
            {
                'form': form, 'deals_detail_info': deals_info,
                'currencies_detail_info': currencies_info
            }
        )