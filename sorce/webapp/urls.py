from django.urls import path

from webapp.views import IndexView, IssueDetailView, IssueCreateView, IssueDeleteView, IssueUpdateView, \
    CreateProjectView, DetailProjectView, ProjectView, UpdateProjectView, DeleteProjectView, IssueProjectCreateView, \
    IndexViewIndex

app_name = 'webapp'

urlpatterns = [
    path('', IndexViewIndex.as_view(), name='index'),
    path('task/', IndexView.as_view(), name='task'),
    path('product/<int:pk>', IssueDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', IssueDeleteView.as_view(), name='delete'),
    path('update/<int:pk>', IssueUpdateView.as_view(), name='update'),
    path('create/', IssueCreateView.as_view(), name='create'),
    path('create/<int:pk>/', IssueProjectCreateView.as_view(), name='create_project_issue'),
    path('projects/create/', CreateProjectView.as_view(), name='create_project'),
    path('projects/<int:pk>', DetailProjectView.as_view(), name='detail_project'),
    path('projects/<int:pk>/update', UpdateProjectView.as_view(), name='update_project'),
    path('projects/<int:pk>/delete', DeleteProjectView.as_view(), name='delete_project'),
    path('projects/', ProjectView.as_view(), name='project'),
]
