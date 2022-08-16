from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, ProfileView, ProfileList

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('create/', register_view, name='create'),
    path('create/', RegisterView.as_view(), name='create'),
    path('<int:pk>', ProfileView.as_view(), name='detail_user'),
    path('users/', ProfileList.as_view(), name='users_list')
]
