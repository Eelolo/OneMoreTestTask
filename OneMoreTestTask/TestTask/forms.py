from django import forms
from .mixins import FilterFormMixin
from datetime import datetime


class FilterForm(forms.Form, FilterFormMixin):
    """Form for filtering deals on the index page"""

    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    deal_stages = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'class': 'custom-select'}),
    )

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        self.fields['date_from'].initial = self.get_default_date_from(datetime.now())
        self.fields['date_to'].initial = self.get_default_date_to(datetime.now())

        self.fields['deal_stages'].choices = self.get_deals_stages()
        self.fields['deal_stages'].initial = self.get_default_deals_stages()
