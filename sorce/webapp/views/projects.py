from django.views.generic import ListView

from webapp.forms import Project


class ProjectForm(ListView):
    form_class = Project
    template_name = 'project/create_project.html'
    context_object_name = 'projects'

    def get_success_url(self):
        pass
