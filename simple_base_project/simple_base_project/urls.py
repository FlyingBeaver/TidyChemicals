from django.contrib import admin
from django.urls import path
import base_app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_app.views.search_view)
]
