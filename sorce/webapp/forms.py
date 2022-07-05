from django import forms
from django.forms import widgets
from .models import category_choices


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Name')
    description = forms.CharField(max_length=2000, required=False, widget=widgets.Textarea, label='Description')
    category = forms.ChoiceField(required=True, choices=category_choices, label='Category')
    count = forms.IntegerField(required=True, min_value=0, label='Count')
    price = forms.DecimalField(required=True, max_digits=7, decimal_places=2, label='Price')



class SearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Name')