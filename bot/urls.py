from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import Login, NewUser, index, chat, Logout
from django.contrib.auth.views import LoginView
urlpatterns = [
path("account/login/", Login.as_view(), name='login'),
path("account/register/", NewUser.as_view(), name='register'),
path("", index, name='index'),
path("chatroom/", login_required(chat, login_url='account/login/'), name='chatroom'),
path("logout/", Logout.as_view(), name='logout')

]