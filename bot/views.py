from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from .forms import LoginUser, RegisterUser
from django.views.generic.edit import CreateView, View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _
from .models import Message, Discussion
from django.http import JsonResponse
from openai import OpenAI
# Create your views here.

class Login(auth_views.LoginView):
    template_name = 'bot/auth/login.html'
    authentication_form = LoginUser
    error = ''
    def post(self, request, *args, **kwargs):
        global error
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
                else:
                    try:
                        raise ValidationError(
                            _("Email ou Mot de Passe Non Valide."),
                            code="password_or_email_no_correct",
                        )
                    except ValidationError as e:
                        error = e.messages

        return render(request, 'bot/auth/login.html', {'form': form, 'error': error})


class NewUser(CreateView):
    template_name = 'bot/auth/register.html'
    form_class = RegisterUser
    success_url = '/bot/chatroom/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        error = ''
        if form.is_valid():
            try:
                email = form.cleaned_data.get("email")
                email_used = User.objects.filter(email=email).first()
                if email_used:
                    raise ValidationError(" Email Already Used")
            except ValidationError as e:
                error = e.messages
            else:
                self.object = form.save()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    print("registred")
                    return redirect(self.get_success_url())
        return render(request, self.template_name, {'form': form, 'errors': form.errors, 'error': error})


class Logout(auth_views.LogoutView):
    next_page = '/bot/account/login/'


def index(request):
    return render(request, 'bot/chat/index.html')

class ChatView(CreateView):
    template_name = 'bot/chat/chat.html'
    model = Message

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            textarea = request.POST.get('textarea')
            btn_disabled = request.POST.get("btn_disabled")
            if btn_disabled:
                response = self.chat_completion(textarea)
                discussion = Discussion(user_id=request.user.id)
                discussion.save()
                messages = Message(message_user=textarea, discussion=discussion, message_ia=response)
                messages.save()
                data = {
                    'response': response,'discussion_id': discussion.uuid
                }
                return JsonResponse(data)
            else:
                textarea = request.POST.get('textarea')
                discussion_id = request.POST.get('discussion_id')
                response = self.chat_completion(textarea)
                discussion = Discussion.objects.get(uuid=discussion_id)
                messages = Message(message_user=textarea, discussion=discussion, message_ia=response)
                messages.save()
                data = {
                    'response': response
                }
                return JsonResponse(data)
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'bot/chat/chat.html')

    def chat_completion(self, user_question: str):
        import environ  # Import the environ module
        env = environ.Env()  # Create an instance of the Env class
        environ.Env.read_env()  # Read the .env file

        KEY = env("API_KEY")  # Retrieve the value of the API_KEY environment variable
        client = OpenAI(api_key=KEY)  # Use the API key to authenticate with the OpenAI API

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{user_question}"},
            ]
        )
        return response.choices[0].message.content







