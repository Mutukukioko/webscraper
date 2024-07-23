from django import forms

class ScrapeForm(forms.Form):
    url = forms.URLField(label='website URL', widget=forms.URLInput(attrs={'class': 'form-control'}))