from django import forms
from .mixins import FilterFormTools


class FilterForm(forms.Form):
    """Form for filtering deals on the index page"""

    tools = FilterFormTools()

    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    deal_stages = forms.MultipleChoiceField(
        choices=tools.get_deals_stages(),
        widget=forms.SelectMultiple(attrs={'class': 'custom-select'}),
    )
