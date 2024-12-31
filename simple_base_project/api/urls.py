from django.urls import path, include
from django.contrib.auth.decorators import login_required

from api.views import Users, Chemicals


urlpatterns = [
    path('users', Users.as_view()),
    path('chemicals', Chemicals.as_view({"get": "list",
                                         "post": "create"})),
    path('chemicals/<int:pk>', Chemicals.as_view({"get": "retrieve",
                                                  "put": "update",
                                                  "delete": "destroy"}))
]
