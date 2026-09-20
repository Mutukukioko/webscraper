from django import forms


class ScrapeForm(forms.Form):
    url = forms.URLField(
        label="website URL",
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )


class BulkScrapeForm(forms.Form):
    urls = forms.CharField(
        label="URLs (one per line)",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 8,
            "placeholder": "One URL per line, e.g. https://example.com",
        }),
    )
