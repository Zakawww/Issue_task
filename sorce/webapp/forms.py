from django import forms
from django.forms import widgets
from webapp.models import Issue


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'type']
        widgets = {"type": widgets.CheckboxSelectMultiple,
                   "description": widgets.Textarea(attrs={"placeholder": "Введите контент"})
                   }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label='Search')
