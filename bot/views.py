from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from .forms import LoginUser, RegisterUser
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy


# Create your views here.

class Login(auth_views.LoginView):
    template_name = 'bot/auth/login.html'
    authentication_form = LoginUser
    error = ''

    def post(self, request, *args, **kwargs):
        form = self.authentication_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = User.objects.filter(email=email).first()
            if user is not None:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    print('login')
                    return redirect('chatroom')
        error = "Email ou mot de passe non valide"
        return render(request, 'bot/auth/login.html', {'error': error, 'form': form})


class NewUser(CreateView):
    template_name = 'bot/auth/register.html'
    form_class = RegisterUser
    success_url = '/bot/chatroom/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("registred")
                return redirect(self.get_success_url())
        return render(request, self.template_name, {'form': form})


class Logout(auth_views.LogoutView):
    next_page = '/bot/account/login/'


def index(request):
    return render(request, 'bot/chat/index.html')


def chat(request):
    return render(request, 'bot/chat/chat.html')
