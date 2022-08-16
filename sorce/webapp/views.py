from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, View, FormView, ListView, CreateView, DetailView, DeleteView, UpdateView

from .forms import SearchForm, IssueForm, ProjectForm, IssueProjectForm, AddProjectUsersForm
from .models import Issue, Project
from django.utils.http import urlencode


class IndexViewIndex(ListView):
    model = Issue
    template_name = 'index.html'
    context_object_name = 'issues'


class IndexView(ListView):
    model = Issue
    template_name = 'partial/view_products.html'
    context_object_name = 'issues'
    # ordering = '-updated_date'
    paginate_by = 3  # отображает 2 статьи
    paginate_orphans = 2  # отображает на последней страницы сколько будет статей
    # page_kwarg = "page"  # можно переопределить

    # def get(self, request, *args, **kwargs):
    #     self.form = self.get_search_form()
    #     self.search_value = self.get_search_value()
    #     return super().get(request, *args, **kwargs)
    #
    # def get_queryset(self):
    #     if self.search_value:
    #         return Issue.objects.filter(
    #             Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value))
    #     return Issue.objects.all()
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=object_list, **kwargs)
    #     context['form'] = self.form
    #     if self.search_value:
    #         query = urlencode({'search': self.search_value})
    #         context['query'] = query
    #         context['search'] = self.search_value
    #     return context
    #
    # def get_search_form(self):
    #     return SearchForm(self.request.GET)
    #
    # def get_search_value(self):
    #     if self.form.is_valid():
    #         return self.form.cleaned_data.get('search')


class IssueDetailView(TemplateView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get("pk")
        issues = get_object_or_404(Issue, pk=pk)
        context['issues'] = issues
        return context


class IssueDeleteView(PermissionRequiredMixin, DeleteView):
    model = Issue
    permission_required = 'webapp.delete_issue'
    search_fields = ['name__icontains']

    def get_success_url(self):
        return reverse('webapp:index')


class IssueCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    model = Issue
    form_class = IssueForm
    permission_required = 'webapp.add_issue'

    # def get_success_url(self):
    #     return reverse('webapp:detail', kwargs={'pk': self.object.pk})


class IssueUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = IssueForm
    template_name = "update.html"
    model = Issue
    context_object_name = 'issues'
    permission_required = 'webapp.change_issue'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('index')
        if not user.has_perm('webapp.update'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class IssueProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'create.html'
    form_class = IssueProjectForm
    permission_required = 'webapp.add_issue_project'


    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        types = form.cleaned_data.pop('type')
        issue = project.projects.create(**form.cleaned_data)
        issue.type.set(types)
        return redirect('webapp:detail_project', pk=project_pk)


class CreateProjectView(PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create_project.html'
    form_class = ProjectForm
    permission_required = 'webapp.add_project'

    def form_valid(self, form):
        project = form.save()
        project.users.add(self.request.user)
        project.save()
        return redirect('webapp:detail_project', pk=project.pk)




class ProjectView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'
    ordering = '-create_date'
    paginate_by = 3  # отображает 2 статьи
    paginate_orphans = 2  # отображает на последней страницы сколько будет статей
    page_kwarg = "page"  # можно переопределить


class DetailProjectView(DetailView):
    template_name = 'project/project_detail.html'
    model = Project
    context_key = 'project'

    def get_queryset(self):
        return Project.objects.all()


class UpdateProjectView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_update.html'
    context_object_name = 'project'
    permission_required = 'webapp.change_project'

    def has_permission(self):
        return self.request.user.has_perm('webapp.projects_list')

    # def get_success_url(self):
    #     return reverse('webapp:detail_project', kwargs={'pk': self.object.pk})


class DeleteProjectView(PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = 'webapp.delete_project'

    def has_permission(self):
        return self.request.user.has_perm('webapp.projects_list')

    def get_success_url(self):
        return reverse('webapp:project')


class AddProjectUsers(PermissionRequiredMixin, UpdateView):
    template_name = 'project/add_project_users.html'
    model = Project
    form_class = AddProjectUsersForm
    permission_required = 'webapp.add_project'
    permission_denied_message = "Доступ запрещён"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def form_valid(self, form):
        project = form.save()
        user_id = self.request.POST.get('user')
        user = self.request.user.pk
        project.users.add(user_id, user)
        project.save()
        return redirect('webapp:detail_project', pk=project.pk)


class DeleteProjectUser(PermissionRequiredMixin, DeleteView):
    permission_required = 'webapp.delete_user'
    permission_denied_message = "Доступ запрещён"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        user_id = request.POST.get('user')
        team = User.objects.get(project=project_id, user=int(user_id), end_date__isnull=True)
        team.save()
        return redirect(reverse('webapp:project_detail', kwargs={'pk': project_id}))


#
# class DeleteProjectView(PermissionRequiredMixin, DeleteView):
#     model = Project
#
#     def has_permission(self):
#         return self.request.user.has_perm('webapp.projects_list')
#
#     def get_success_url(self):
#         return reverse('webapp:project')