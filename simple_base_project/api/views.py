from django.shortcuts import render
from django.http import (HttpResponseNotAllowed,
                         HttpResponseForbidden)
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User

from chemicals.models import Chemical
from api.serializers import (UsersSerializer,
                             ChemicalsSerializer)


class Users(ListAPIView):
    queryset = User.objects.only("username",
                                 "first_name",
                                 "last_name").all()
    serializer_class = UsersSerializer


class Chemicals(ModelViewSet):
    queryset = Chemical.objects.select_related("storage_place",
                                               "who_created__user",
                                               "who_updated__user",
                                               "taken_by__user").\
        only("id",
             "name",
             "name_data",
             "structure",
             "mol_block",
             "molecular_formula",
             "molar_mass",
             "synonym",
             "synonym_data",
             "comment",
             "comment_data",
             "cas",
             "quantity",
             "hazard_pictograms",
             "when_created",
             "when_updated",
             "barcode",
             "date_time_taken",
             "storage_place",
             "quantity_unit",
             "who_created",
             "who_updated",
             "taken_by",
             "storage_place__path_str",
             "who_created__user__username",
             "who_updated__user__username",
             "taken_by__user__username").all()
    serializer_class = ChemicalsSerializer

    def list(self, request):
        return HttpResponseForbidden("GET request is forbidden")
