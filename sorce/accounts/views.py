from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from accounts.forms import MyUserCreationForm
from accounts.models import Profile
from webapp.models import Issue


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
        return self.request.user.has_perm('accounts.view_user')

# def register_view(request, *args, **kwargs):
#     if request.method == 'POST':
#         form = MyUserCreationForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('webapp:index')
#     else:
#         form = MyUserCreationForm()
#     return render(request, 'user_create.html', context={'form': form})
