from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import login_view, logout_view, register_view

app_name = 'accounts'

# urlpatterns = [
#     path('accounts/login', login_view, name='login'),
#     path('accounts/logout/', logout_view, name='logout'),
# ]




urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', register_view, name='create'),
    # path('create/', RegisterView.as_view(), name='create')
]
