from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm, PasswordChangeForm
from accounts.models import Profile
# from webapp.forms import UserChangeForm, ProfileChangeForm, PasswordChangeForm
from webapp.models import Issue

User = get_user_model()


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webapp:index')
        else:
            context['has_error'] = True
    return render(request, 'registration/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:index')


class RegisterView(CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_obj'
    paginate_by = 3  # отображает 2 статьи
    paginate_orphans = 2  # отображает на последней страницы сколько будет статей

    def get_context_data(self, **kwargs):
        paginator = Paginator(self.get_object().users.all(), self.paginate_by, self.paginate_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['issues'] = page.object_list
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class ProfileList(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users.html'
    context_object_name = 'profiles'
    paginate_by = 4
    paginate_orphans = 0
    permission_required = 'accounts.view_users'

    def has_permission(self):
        return self.request.user.groups.filter(name__in=('manager', 'Манаджер', 'led')).exists()


#
# class ChangeProfileView(UpdateView):
#     # model = User
#     # form_class = UserChangeForm
#     # template_name = 'user_change.html'
#     # profile_form_class = ProfileChangeForm
#
#     model = get_user_model()
#     form_class = UserChangeForm
#     template_name = 'user_change.html'
#     context_object_name = 'user_obj'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['profile_form'] = self.profile_form_class(instance=self.get_object().profile)
#     #     return context
#
#     def get_context_data(self, **kwargs):
#         if 'profile_form' not in kwargs:
#             kwargs['profile_form'] = self.get_profile_form()
#         return super().get_context_data(**kwargs)
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         profile_form = self.get_profile_form()
#         if form.is_valid() and profile_form.is_valid():
#             return self.form_valid(form, profile_form)
#         else:
#             return self.form_invalid(form, profile_form)
#
#     def form_valid(self, form, profile_form):
#         response = super().form_valid(form)
#         profile_form.save()
#         return response
#
#     def form_invalid(self, form, profile_form):
#         context = self.get_context_data(form=form, profile_form=profile_form)
#         return self.render_to_response(context)
#
#     def get_profile_form(self):
#         form_kwargs = {'instance': self.object.profile}
#         if self.request.method == 'POST':
#             form_kwargs['data'] = self.request.POST
#             form_kwargs['files'] = self.request.FILES
#         return ProfileChangeForm(**form_kwargs)
#
#     def get_success_url(self):
#         return reverse('accounts:profile', kwargs={'pk': self.object.pk})


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:detail_user', kwargs={'pk': self.object.pk})


# class UserPasswordChangeView(PasswordChangeView):
#     template_name = 'user_password_change.html'
#
#     def get_success_url(self):
#         return reverse('accounts:detail', kwargs={'pk': self.request.user.pk})

class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:detail_user')
