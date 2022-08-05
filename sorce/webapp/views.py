from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, View, FormView, ListView, CreateView, DetailView, DeleteView, UpdateView

from .forms import SearchForm, IssueForm, ProjectForm, IssueProjectForm
from .models import Issue, Project
from django.utils.http import urlencode


class IndexView(ListView):
    model = Issue
    template_name = 'index.html'
    context_object_name = 'issues'
    ordering = '-updated_date'
    paginate_by = 3  # отображает 2 статьи
    paginate_orphans = 2  # отображает на последней страницы сколько будет статей
    page_kwarg = "page"  # можно переопределить

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Issue.objects.filter(
                Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Issue.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')


class IssueDetailView(TemplateView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get("pk")
        issues = get_object_or_404(Issue, pk=pk)
        context['issues'] = issues
        return context


class IssueDeleteView(DeleteView):
    model = Issue

    def get_success_url(self):
        return reverse('webapp:index')


# class IssueCreateView(CreateView):
#     template_name = 'create.html'
#     form_class = IssueForm
#
#     # def get_success_url(self):
#     #     return reverse('webapp:detail', kwargs={'pk': self.object.pk})
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('accounts:login')
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse('webapp:detail', kwargs={'pk': self.object.pk})


class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    model = Issue
    form_class = IssueForm

    # def get_success_url(self):
    #     return reverse('webapp:detail', kwargs={'pk': self.object.pk})


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    form_class = IssueForm
    template_name = "update.html"
    model = Issue
    context_object_name = 'issues'


class IssueProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'create.html'
    form_class = IssueProjectForm

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        types = form.cleaned_data.pop('type')
        issue = project.projects.create(**form.cleaned_data)
        issue.type.set(types)
        return redirect('webapp:detail_project', pk=project_pk)


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create_project.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('webapp:detail_project', kwargs={'pk': self.object.pk})


class ProjectView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'
    ordering = '-create_date'
    paginate_by = 3  # отображает 2 статьи
    paginate_orphans = 2  # отображает на последней страницы сколько будет статей
    page_kwarg = "page"  # можно переопределить


class DetailProjectView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'

    def get_queryset(self):
        return Project.objects.all()


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_update.html'
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('webapp:detail_project', kwargs={'pk': self.object.pk})


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    model = Project

    def get_success_url(self):
        return reverse('webapp:project')
