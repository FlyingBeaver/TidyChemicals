from django.contrib import admin
from django.urls import path, include
import base_app.views
import profiles.views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', login_required(base_app.views.search_view)),
    path('', profiles.views.HomePage),
    path('registration/', profiles.views.RegistrationPage.as_view()),
    path('login/', profiles.views.LoginPage.as_view()),
    path('logout/', profiles.views.logout_invisible),
]
