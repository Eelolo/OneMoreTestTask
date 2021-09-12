from django import forms
from .mixins import FilterFormTools
from datetime import datetime


class FilterForm(forms.Form):
    """Form for filtering deals on the index page"""

    tools = FilterFormTools()

    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=tools.get_default_date_from(datetime.now())
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=tools.get_default_date_to(datetime.now())
    )
    deal_stages = forms.MultipleChoiceField(
        choices=tools.get_deals_stages(),
        widget=forms.SelectMultiple(attrs={'class': 'custom-select'}),
    )
