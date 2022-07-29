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
    paginate_by = 5  # отображает 2 статьи
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


# class IssueDeleteView(View):
#     def get(self, request, pk):
#         issue = get_object_or_404(Issue, pk=pk)
#         return render(request, 'index.html', {'issue': issue})
#
#     def post(self, request, pk):
#         issue = get_object_or_404(Issue, pk=pk)
#         issue.delete()
#         return redirect('index')

class IssueDeleteView(DeleteView):
    model = Issue

    def get_success_url(self):
        return reverse('index')


class IssueCreateView(CreateView):
    template_name = 'create.html'
    form_class = IssueForm

    # def form_valid(self, form):
    #     self.issue = form.save()
    #     return super().form_valid(form)

    # def get_redirect_url(self):
    #     return reverse('detail', kwargs={'pk': self.object.pk})

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class IssueUpdateView(UpdateView):
    form_class = IssueForm
    template_name = "update.html"
    model = Issue
    context_object_name = 'issues'

    # def get_success_url(self):
    #     return reverse("detail", kwargs={"pk": self.object.pk})


# class IssueUpdateView(FormView):
#     form_class = IssueForm
#     template_name = "update.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         self.issue = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['issues'] = self.issue
#         return context
#
#     def get_form_kwargs(self):
#         form_kwargs = super().get_form_kwargs()
#         form_kwargs['instance'] = self.issue
#         return form_kwargs
#
#     def form_valid(self, form):
#         self.issue = form.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse("detail", kwargs={"pk": self.issue.pk})
#
#     def get_object(self):
#         return get_object_or_404(Issue, pk=self.kwargs.get("pk"))


class IssueProjectCreateView(CreateView):
    model = Project
    template_name = 'create.html'
    form_class = IssueProjectForm

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        types = form.cleaned_data.pop('type')
        issue = project.projects.create(**form.cleaned_data)
        issue.type.set(types)
        return redirect('detail_project', pk=project_pk)


class ProjectView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'


class DetailProjectView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['project'] = self.projects
    #     return context

    def get_queryset(self):
        return Project.objects.all()


# class CommentUpdateView(UpdateView):
#     model = Comment
#     template_name = 'comment/update.html'
#     form_class = ArticleCommentForm
#     context_object_name = 'comment'
#
#     def get_success_url(self):
#         return reverse('article_view', kwargs={'pk': self.object.article.pk})


class UpdateProjectView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_update.html'
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('update_project', kwargs={'pk': self.object.pk})


class CreateProjectView(CreateView):
    model = Project
    template_name = 'project/create_project.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.object.pk})


class DeleteProjectView(DeleteView):
    model = Project

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.object.projects.pk})
