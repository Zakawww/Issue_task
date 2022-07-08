from django.urls import path

from webapp.views import index, delete, detail, create, update, search

urlpatterns = [
    path('', index, name='index'),
    path('product/<int:pk>', detail, name='detail'),
    path('create/', create, name='create'),
    path('update/<int:pk>', update, name='update'),
    path('delete/<int:pk>', delete, name='delete'),
    path('search/', search, name='search'),
]
