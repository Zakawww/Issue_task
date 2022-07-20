from django.urls import path

from webapp.views import IndexView, DetailView, CreateView, DeleteView, UpdateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>', DetailView.as_view(), name='detail'),
    path('delete/<int:pk>', DeleteView.as_view(), name='delete'),
    path('update/<int:pk>', UpdateView.as_view(), name='update'),
    path('create/', CreateView.as_view(), name='create'),
]
