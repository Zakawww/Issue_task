from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms import widgets

from accounts.models import Profile
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
        fields = ['summary', 'description', 'create_date', 'end_date']
        # fields = '__all__'


class IssueProjectForm(forms.ModelForm):
    class Meta:
        model = Issue
        exclude = ['create_date', 'project', 'updated_date']

#
# class AddProjectUsersForm(forms.ModelForm):
#     users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False, label='Участники',
#                                            widget=forms.CheckboxSelectMultiple)
#
#     class Meta:
#         model = User
#         fields = ['users']
#
#
# class UserChangeForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['first_name', 'last_name', 'email']
#         labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}
#
#
# class ProfileChangeForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['birthday', 'avatar']
#
#
# class PasswordChangeForm(forms.ModelForm):
#     password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
#     password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
#     old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)
#
#     def clean_password_confirm(self):
#         password = self.cleaned_data.get("password")
#         password_confirm = self.cleaned_data.get("password_confirm")
#         if password and password_confirm and password != password_confirm:
#             raise forms.ValidationError('Пароли не совпадают!')
#         return password_confirm
#
#     def clean_old_password(self):
#         old_password = self.cleaned_data.get('old_password')
#         if not self.instance.check_password(old_password):
#             raise forms.ValidationError('Старый пароль неправильный!')
#         return old_password
#
#     def save(self, commit=True):
#         user = self.instance
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user
#
#     class Meta:
#         model = get_user_model()
#         fields = ['password', 'password_confirm', 'old_password']
