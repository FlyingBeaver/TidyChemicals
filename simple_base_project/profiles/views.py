from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


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
    # TODO: Форма регистрации перенаправляет на логин,
    # но было бы здорово, если бы при этом ещё и
    # показывалось сообщение об успешной регистрации

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                print(user)
                print("user is not none")
                return redirect('/search')
            else:
                print('user is none')
                return self.try_again(request)
        else:
            return self.try_again(request)


class RegistrationPage(Mixin, View):
    # TODO: Форма регистрации не показывает сообщения, исправить
    form = UserCreationForm
    template = 'registration/registration.html'
    issues_message = "Проверьте корректность введённых данных"
    page_kind = "reg"

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return self.try_again(request)


@login_required
def logout_invisible(request):
    logout(request)
    return redirect('/login/')


@login_required
def HomePage(request):
    return redirect('/search/')
