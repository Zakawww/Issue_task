from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Issue





class IssueForm(forms.ModelForm):
    # summary = forms.CharField(max_length=60, required=True, label='summary', validators=[validate_title])

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'type']
        widgets = {"type": widgets.CheckboxSelectMultiple,
                   "description": widgets.Textarea(attrs={"placeholder": "Введите контент"})
                   }

    # def clean_title(self):
    #     summary = self.cleaned_data.get("summary")
    #     if len(summary) > 7:
    #         raise ValidationError("This field should be at least %(length)d symbols long!", code="too_short",
    #                               params={"length": 7})
    #     return summary

    # def clean(self):
    #     if len(self.cleaned_data.get("summary")) > 7:
    #         raise ValidationError("Название больше 7 символов")
    #     return super().clean()

    # def clean(self):
    #     if self.cleaned_data.get("summary") == self.cleaned_data.get("description"):
    #         raise ValidationError("Название и описание не могут совпадать")
    #     return super().clean()


class SearchForm(forms.Form):
    summary = forms.CharField(max_length=30, required=False, label='summary')
