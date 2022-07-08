from django import forms
from django.forms import widgets
from webapp.models import Status, Type


class IssueForm(forms.Form):
    summary = forms.CharField(max_length=100, required=True, label='summary')
    description = forms.CharField(max_length=2000, required=False, widget=widgets.Textarea, label='description')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='status')
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, label='type')


class SearchForm(forms.Form):
    summary = forms.CharField(max_length=60, required=False, label='summary')
