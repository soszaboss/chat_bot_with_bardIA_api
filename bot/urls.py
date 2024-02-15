from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import Login, NewUser, index
from django.contrib.auth.views import LoginView
urlpatterns = [
path("account/login/", Login.as_view(), name='login'),
path("account/register/", NewUser.as_view(), name='register'),
path("", login_required(index, login_url='account/login/'), name='index'),

]