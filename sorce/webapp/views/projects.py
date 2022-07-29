from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from webapp.forms import ProjectForm
from webapp.models import Issue


class CreateProjectView(CreateView):
    form_class = ProjectForm
    template_name = 'project/create_project.html'

    def form_valid(self, form):
        issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        form.instance.issue = issue
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.issue.pk})


# class IssueUpdateView(UpdateView):
#     form_class = IssueForm
#     template_name = "update.html"
#     model = Issue
#     context_object_name = 'issues'
#
#     def get_success_url(self):
#         return reverse("detail", kwargs={"pk": self.object.pk})