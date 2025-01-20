from django.shortcuts import render
from django.http import (HttpResponseNotAllowed,
                         HttpResponseForbidden)
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView,
                                     RetrieveUpdateAPIView,
                                     get_object_or_404)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.exceptions import (MethodNotAllowed,
                                       ValidationError,
                                       NotFound)
from rest_framework.response import Response
from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   UpdateModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin)
from django.contrib.auth.models import User

from chemicals.models import (Chemical,
                              StoragePlace)
from chemicals.services.exceptions import DatabaseException
from profiles.models import Ampersandtag, Hashtag
from api.serializers import (make_conflict_exception,
                             UsersSerializer,
                             ChemicalsSerializer,
                             RootStorageSerializer,
                             StoragesSerializer,
                             ChemicalsShortSerializer,
                             FavoritesSerializer,
                             UninitializedChemicalsSerializer,
                             PathToChemicalSerializer,
                             HashtagSerializer,
                             HashtagSerializerShort,
                             AmpersandtagSerializer,
                             AmpersandtagSerializerShort,
                             TakeChemicalSerializer,
                             ReturnChemicalSerializer,
                             UninitializedStoragesSerializer)


class Users(ListAPIView):
    queryset = User.objects.only("username",
                                 "first_name",
                                 "last_name").all()
    serializer_class = UsersSerializer


class Chemicals(CreateModelMixin,
                RetrieveModelMixin,
                UpdateModelMixin,
                DestroyModelMixin,
                GenericViewSet):
    queryset = Chemical.objects.select_related("storage_place",
                                               "who_created__user",
                                               "who_updated__user",
                                               "taken_by__user").\
        only("id",
             "name",
             "name_data",
             "water_number",
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


class RootStorage(RetrieveAPIView):
    queryset = StoragePlace.objects.all()
    serializer_class = RootStorageSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, level=0)


class Storages(CreateModelMixin,
               RetrieveModelMixin,
               UpdateModelMixin,
               DestroyModelMixin,
               GenericViewSet):
    queryset = StoragePlace.objects.all()
    serializer_class = StoragesSerializer

    def retrieve(self, request, pk=None):
        storage = get_object_or_404(self.queryset, id=pk)
        if storage.contains_chemicals:
            content = Chemical.objects.filter(storage_place=storage)
            serializer = ChemicalsShortSerializer(content, many=True)
        else:
            children = self.queryset.filter(parent=pk)
            serializer = StoragesSerializer(children, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except DatabaseException as e:
            raise make_conflict_exception(str(e))


class Favorites(ModelViewSet):
    serializer_class = FavoritesSerializer
    queryset = Ampersandtag.objects.all()
    
    def list(self, request):
        profile = request.user.profile
        ampersandtags_qset = Ampersandtag.objects.filter(
            creator=profile,
            name="favorites"
        )
        if ampersandtags_qset.count() == 0:
            return Response([])
        else:
            ampersandtag = ampersandtags_qset[0]
            chemicals = ampersandtag.chemicals.all()
            serializer = ChemicalsShortSerializer(chemicals,
                                                  many=True)
            return Response(serializer.data)

    def create(self, request):
        ampersandtag = self.get_object()
        serializer = self.serializer_class(
            data=request.data,
            context={"ampersandtag": ampersandtag}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.get_or_create(
            creator=self.request.user.profile,
            name="favorites"
        )[0]


class UninitializedChemicals(ListModelMixin,
                             RetrieveModelMixin,
                             UpdateModelMixin,
                             GenericViewSet):
    serializer_class = UninitializedChemicalsSerializer
    queryset = Chemical.objects.filter(barcode=None).\
        select_related("storage_place",
                       "who_created__user",
                        "who_updated__user",
                        "taken_by__user").\
        only("id",
             "name",
             "name_data",
             "water_number",
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
             "taken_by__user__username")

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ChemicalsShortSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        chemical = get_object_or_404(queryset, id=pk)
        serializer = ChemicalsSerializer(chemical,
                                         context={"request": request})
        return Response(serializer.data)


class PathToChemical(RetrieveAPIView):
    serializer_class = PathToChemicalSerializer
    queryset = Chemical.objects.all()


class Hashtags(CreateModelMixin,
               ListModelMixin,
               RetrieveModelMixin,
               UpdateModelMixin,
               GenericViewSet):
    serializer_class = HashtagSerializer
    queryset = Hashtag.objects.all()

    @classmethod
    def create_list(cls):
        serializer = HashtagSerializerShort(cls.queryset, many=True)
        return serializer.data

    def list(self, request):
        return Response(self.create_list())


class Ampersandtags(CreateModelMixin,
                    ListModelMixin,
                    RetrieveModelMixin,
                    UpdateModelMixin,
                    GenericViewSet):
    serializer_class = AmpersandtagSerializer
    queryset = Ampersandtag.objects.all()

    @classmethod
    def create_list(cls, profile):
        queryset = cls.queryset.filter(creator=profile)
        serializer = AmpersandtagSerializerShort(queryset, many=True)
        return serializer.data

    def list(self, request):
        profile = request.user.profile
        return Response(self.create_list(profile))

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        profile = request.user.profile
        ampersandtag = get_object_or_404(queryset,
                                         name=pk,
                                         creator=profile)
        serializer = AmpersandtagSerializer(ampersandtag,
                                            context={"request": request})
        return Response(serializer.data)


class Tags(ListAPIView):
    def get(self, request):
        profile = request.user.profile
        return Response(
            {"ampersandtags": Ampersandtags.create_list(profile),
             "hashtags": Hashtags.create_list()}
        )


class TakeChemical(UpdateAPIView):
    queryset = Chemical.objects.exclude(barcode=None)
    serializer_class = TakeChemicalSerializer

    def get_object(self):
        queryset = self.get_queryset()
        barcode_raw = request.data.get("barcode")
        try:
            barcode = int(barcode_raw)
        except ValueError:
            raise ValidationError(
                "Invalid value of 'barcode'. "
                "Can't convert it to integer."
            )
        filtered = queryset.filter(barcode=barcode)
        if filtered.count() == 0:
            raise NotFound()
        instance = filtered[0]
        return instance


class ReturnChemical(TakeChemical):
    serializer_class = ReturnChemicalSerializer


class UninitializedStorages(ListModelMixin,
                            UpdateModelMixin,
                            GenericViewSet):
    serializer_class = UninitializedStoragesSerializer
    queryset = StoragePlace.objects.filter(barcode=None)
