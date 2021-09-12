from django import forms
from .models import DealStage


class FilterForm(forms.Form):
    """Form for filtering deals on the index page"""

    stages = []
    for stage in DealStage.objects.all().order_by('probability'):
        stages.append((stage.id, f'{stage.name} {str(stage.probability)}%'))

    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    deal_stages = forms.MultipleChoiceField(
        choices=stages,
        widget=forms.SelectMultiple(attrs={'class': 'custom-select'}),
    )
