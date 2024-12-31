from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

import chemicals.views
import profiles.views
import api.urls


urlpatterns = [
    path('api/v1/', include(api.urls)),
    path('admin/', admin.site.urls),
    path('search/', login_required(chemicals.views.search_view)),
    path('tree_api/', login_required(chemicals.views.tree_api)),
    path('new_search/', login_required(chemicals.views.new_search)),
    path('chemical/<int:chemical_id>', login_required(chemicals.views.chemical_view)),
    path('', profiles.views.HomePage),
    path('chemicals-images/<str:filename>',
         cache_page(3600)(chemicals.views.chemical_image_view)),
    path('registration/', profiles.views.RegistrationPage.as_view()),
    path('login/', profiles.views.LoginPage.as_view()),
    path('logout/', profiles.views.logout_invisible),
]
