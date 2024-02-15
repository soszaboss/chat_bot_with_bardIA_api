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
                    return redirect('index')
        error = "Email ou mot de passe non valide"
        return render(request, 'bot/auth/login.html', {'error': error, 'form':form})


class NewUser(CreateView):
    template_name = 'bot/auth/register.html'
    form_class = RegisterUser
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(self.get_success_url())
        return render(request, self.template_name, {'form': form})


def index(request):
    return HttpResponse('<h1> Login Page </h1>')