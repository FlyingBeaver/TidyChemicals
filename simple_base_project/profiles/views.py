from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from simple_base_project.settings import LOGIN_URL


# class AuthView(View):
#     @classmethod
#     def as_view(cls, *args, **kwargs):
#         def result(request):
#             if isinstance(request.user, AnonymousUser):
#                 return redirect(LOGIN_URL)
#             else:
#                 return super().as_view(*args, **kwargs)
#         return result


# class AnonymousOnlyView(View):
#     @classmethod
#     def as_view(cls, *args, **kwargs):
#         def result(request):
#             if not isinstance(request.user, AnonymousUser):
#                 return redirect('')
#             else:
#                 return cls.(View.as_view)(cls, *args, **kwargs)
#                 # return cls.parents_as_view(*args, **kwargs)
#         return result


class Mixin:
    template = None
    form = None
    issues_message = None
    page_kind = None

    def get(self, request):
        return render(request, self.template,
                      {"form": self.form,
                       "page_kind": self.page_kind,
                       "username": request.user.username})

    def try_again(self, request):
        return render(request, self.template,
                      {"form": self.form,
                       "message": self.issues_message,
                       "page_kind": self.page_kind,
                       "username": request.user.username})


class LoginPage(Mixin, View):
    template = 'authentificate/login.html'
    form = forms.LoginForm
    issues_message = "Не удолось совершить вход. " \
                     "Проверьте правильность введённых данных"
    page_kind = "login"

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/search')
        else:
            return self.try_again(request)


class RegistrationPage(Mixin, View):
    form = UserCreationForm
    template = 'registration/registration.html'
    issues_message = "Проверьте корректность введённых данных"
    page_kind = "reg"

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            return redirect('')
        else:
            self.try_again(request)


@login_required
def logout_invisible(request):
    logout(request)
    return redirect('/login/')


@login_required
def HomePage(request):
    return redirect('/search/')

##################################################


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/search')
        else:
            form = forms.LoginForm()
            message = "Вы ввели что-то не то"
            return render(request, 'authentificate/login.html',
                          {"form": form, 'message': message})
    elif not isinstance(request.user, AnonymousUser):
        return HttpResponse(f'<h1>Уже залогинился, брат: {request.user}</h1>')
    else:
        form = forms.LoginForm()
        return render(request,
                      'authentificate/login.html',
                      context={"form": form})


def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse(f'<h1>Регистрация прошла успешно!</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'registration/registration.html',
                      context={"form": form})



