from django.contrib import admin
from django.urls import path, include
import chemicals.views
import profiles.views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', login_required(chemicals.views.search_view)),
    path('tree_api/', login_required(chemicals.views.tree_api)),
    path('new_search/', login_required(chemicals.views.new_search)),
    path('chemical/<int:chemical_id>/', login_required(chemicals.views.chemical_view)),
    path('', profiles.views.HomePage),
    path('chemicals-images/<str:filename>/', chemicals.views.chemical_image_view),
    path('registration/', profiles.views.RegistrationPage.as_view()),
    path('login/', profiles.views.LoginPage.as_view()),
    path('logout/', profiles.views.logout_invisible),
]
