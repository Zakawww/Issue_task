from django import forms
from django.forms import widgets
from webapp.models import Issue, Project


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        # fields = ['summary', 'description', 'status', 'type']
        fields = '__all__'
        widgets = {"type": widgets.CheckboxSelectMultiple,
                   "description": widgets.Textarea(attrs={"placeholder": "Введите контент"})
                   }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label='Search')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class IssueProjectForm(forms.ModelForm):

    class Meta:
        model = Issue
        exclude = ['create_date', 'project', 'updated_date']