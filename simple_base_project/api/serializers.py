from abc import ABC
from decimal import Decimal
from pprint import pprint
from rest_framework.serializers import (ModelSerializer,
                                        ListSerializer,
                                        ValidationError,
                                        CharField,
                                        IntegerField,
                                        Serializer)
from rest_framework.exceptions import APIException, ParseError
from django.contrib.auth.models import User
from chemicals.models import (Chemical,
                              StoragePlace,
                              BARCODE_STANDARDS)
from chemicals.services.rendering_paginator import create_svg_alt
from chemicals.services.exceptions import DatabaseException
from profiles.models import Hashtag, Ampersandtag, FreeBarcode
from api.services.make_summaries import make_summary
from api.services.validations import (update_chemical_validation,
                                      create_chemical_validation)


class AbstractConflictException(APIException, ABC):
    status_code = 409
    default_code = "conflict"


def make_conflict_exception(message: str):
    class ConflictException(AbstractConflictException):
        default_detail = message
    return ConflictException


class UsersListSerializer(ListSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        search_preferences = self.context["request"].\
            user.profile.search_preferences
        del search_preferences["search_fields"]
        ret.append(search_preferences)
        return ret


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
        list_serializer_class = UsersListSerializer


class ChemicalsSerializer(ModelSerializer):
    mol_block = CharField(allow_blank=True,
                          trim_whitespace=False,
                          required=False,
                          allow_null=True)

    class Meta:
        model = Chemical
        fields = "__all__"
        read_only_fields = ["molecular_formula",
                            "molar_mass",
                            "when_created",
                            "when_updated",
                            "who_created",
                            "who_updated",
                            "barcode",
                            "taken_by",
                            "date_time_taken"]


    def to_representation(self, instance):
        ret = super().to_representation(instance)
        hashtags = Hashtag.objects.filter(
            chemicals=instance
        ).only("name")
        hashtags_list = list(map(lambda x: x.name, hashtags))
        ampersandtags = Ampersandtag.objects.filter(
            creator__user=self.context["request"].user.id,
            chemicals=instance
        ).only("name")
        ampersandtags_list = list(map(lambda x: x.name, ampersandtags))
        
        storage_path = None
        if instance.storage_place:
            storage_path = instance.storage_place.path_str

        structure_picture = None
        if instance.mol_block not in (None, ""):
            structure_picture = create_svg_alt(None, instance)

        who_created = None
        if instance.who_created is not None:
            who_created = instance.who_created.user.username

        who_updated = None
        if instance.who_updated is not None:
            who_updated = instance.who_updated.user.username

        taken_by = None
        if instance.taken_by is not None:
            taken_by = instance.taken_by.user.username

        ret.update(
            {"hashtags": hashtags_list,
             "ampersandtags": ampersandtags_list,
             "storage_place": storage_path,
             "who_created": who_created,
             "who_updated": who_updated,
             "taken_by": taken_by,
             "structure_picture": structure_picture}
        )
        return ret

    def create(self, validated_data):
        create_chemical_validation(validated_data)
        (generated_fields,
         elem_dict,
         path_dict,
         ring_dict) = make_summary(
            validated_data.get("mol_block", "Nothing"),
            validated_data.get("water_number"),
            self.context["request"].user.profile,
            "create"
        )
        validated_data.update(generated_fields)
        try:
            chemical = Chemical.create(validated_data,
                                       elem_dict,
                                       path_dict,
                                       ring_dict)
        except DatabaseException as de:
            raise make_conflict_exception(str(de))
        return chemical

    def update(self, instance, validated_data):
        update_chemical_validation(validated_data, instance)
        (generated_fields,
         elem_dict,
         path_dict,
         ring_dict) = make_summary(
            validated_data.get("mol_block", None),
            validated_data.get("water_number", None),
            self.context["request"].user.profile,
            "update"
        )
        validated_data.update(generated_fields)
        try:
            instance.update(validated_data,
                            elem_dict,
                            path_dict,
                            ring_dict)
        except DatabaseException as de:
            raise make_conflict_exception(str(de))
        return instance


class ChemicalsShortSerializer(ModelSerializer):
    class Meta:
        model = Chemical
        fields = ["id", "name_data"]


class RootStorageSerializer(ModelSerializer):
    class Meta:
        model = StoragePlace
        fields = ["id", "name"]


class StoragesSerializer(ModelSerializer):
    name = CharField(max_length=32,
                     allow_blank=False,
                     required=False)
    class Meta:
        model = StoragePlace
        fields = ["id",
                  "name",
                  "parent",
                  "contains_chemicals",
                  "barcode"]
        read_only_fields = ["id", "contains_chemicals", "barcode"]

    def create(self, validated_data):
        parent_instance = self.get_storage(validated_data["parent"])
        try:
            storage = StoragePlace.create(validated_data["name"],
                                          parent_instance)
            return storage
        except DatabaseException as e:
            raise make_conflict_exception(str(e))

    def update(self, instance, validated_data):
        if "parent" in validated_data and "name" in validated_data:
            raise ParseError(
                "Can't simultaneously rename and move the "
                "storage. Try making these operations "
                "separately."
            )
        if "parent" in validated_data:
            new_parent_instance = self.get_storage(
                validated_data["parent"]
            )
            try:
                instance.move(new_parent_instance)
            except DatabaseException as e:
                raise make_conflict_exception(str(e))
        if "name" in validated_data:
            try:
                instance.rename(validated_data["name"])
            except DatabaseException as e:
                raise make_conflict_exception(str(e))
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        del representation["parent"]
        del representation["contains_chemicals"]
        barcode = representation.pop("barcode")
        if barcode is None:
            representation["type"] = 0
        else:
            representation["type"] = 1
        return representation

    @staticmethod
    def get_storage(storage_id):
        storage_queryset = StoragePlace.objects.filter(id=storage_id)
        if storage_queryset.count() == 0:
            raise make_conflict_exception(
                "Storage with parent_id, given in "
                "the request, does not exist"
            )
        else:
            return storage_queryset[0]


class FavoritesSerializer(ModelSerializer):
    class Meta:
        model = Ampersandtag
        fields = ["chemicals"]

    def update(self, instance, validated_data):
        for chemical in validated_data["chemicals"]:
            instance.chemicals.remove(chemical)
        instance.save()
        return instance

    def create(self, validated_data):
        instance = self.context["ampersandtag"]
        for chemical in validated_data["chemicals"]:
            instance.chemicals.add(chemical)
        instance.save()
        return instance


class UninitializedChemicalsSerializer(ModelSerializer):
    class Meta:
        model = Chemical
        fields = ["barcode", "storage_place"]

    def update(self, instance, validated_data):
        new_barcode_no = validated_data["barcode"]
        storage = validated_data["storage_place"]
        barcode_queryset = FreeBarcode(
            number=new_barcode_no,
            standard=BARCODE_STANDARDS["chemicals"]
        )
        if barcode_queryset.count() == 0:
            raise ValidationError("Barcode does not exist")
        if not (storage and instance.storage_place):
            raise ValidationError(
                "Storage place is required for initializetion"
            )
        barcode = barcode_queryset.get()
        instance.initialize(barcode=barcode, storage=storage)
        return instance


class PathToChemicalSerializer(ModelSerializer):
    class Meta:
        model = Chemical
        fields = ["id", "storage_place"]

    def to_representation(self, instance):
        sequence_to_root = []
        children = dict()
        parent_storage = instance.storage_place
        sibling_chemicals = Chemical.objects.filter(
            storage_place=parent_storage
        )
        siblings_serializer = ChemicalsShortSerializer(
            sibling_chemicals,
            many=True
        )
        children[parent_storage.id] = siblings_serializer.data
        sequence_to_root.append(parent_storage.id)

        while parent_storage.level != 0:
            parent_storage = StoragePlace.objects.get(
                id=parent_storage.parent
            )
            storages_queryset = StoragePlace.objects.filter(
                parent=parent_storage.id
            )
            storages_serializer = RootStorageSerializer(
                storages_queryset,
                many=True
            )
            children[parent_storage.id] = storages_serializer.data
            sequence_to_root.append(parent_storage.id)

        return {"sequence_to_root": sequence_to_root,
                "children": children}


class HashtagSerializerShort(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ["name"]


class AmpersandtagSerializerShort(ModelSerializer):
    class Meta:
        model = Ampersandtag
        fields = ["name"]


class HashtagSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ["name", "chemicals"]

    def update(self, instance, validated_data):
        action = self.context["request"].data.get("action")
        profile = self.context["request"].user.profile
        if action == "add":
            for chemical in validated_data["chemicals"]:
                instance.chemicals.add(chemical)
        if action == "remove":
            for chemical in validated_data["chemicals"]:
                instance.unbind(chemical)
        else:
            raise ValidationError("Wrong value of the 'action' field")
        return instance

    def to_representation(self, instance):
        chemicals = ChemicalsShortSerializer(instance.chemicals,
                                             many=True).data
        return {"chemicals": chemicals}


class AmpersandtagSerializer(HashtagSerializer):
    class Meta:
        model = Ampersandtag
        fields = ["name", "chemicals"]


class TakeChemicalSerializer(ModelSerializer):
    class Meta:
        model = Chemical
        fields = ["barcode", "taken_by"]

    def update(self, instance, validated_data):
        profile = self.context["request"].user.profile
        instance.taken_by = profile
        instance.save()
        return instance

    def to_representation(self, instance):
        return ChemicalsSerializer(instance).data


class ReturnChemicalSerializer(TakeChemicalSerializer):
    def update(self, instance, validated_data):
        profile = self.context["request"].user.profile
        if profile != instance.taken_by:
            raise make_conflict_exception(
                "The chemical can be returned only by "
                "the user, who took it."
            )
        instance.save()
        return instance


class UninitializedStoragesSerializer(ModelSerializer):
    class Meta:
        model = StoragePlace
        fields = ["id", "name", "path_str", "barcode"]

    def update(self, instance, validated_data):
        if "barcode" not in validated_data:
            raise ValidationError(
                "Request does not contain barcode number."
            )
        barcode = validated_data["barcode"]
        barcode_queryset = FreeBarcode.objects.filter(number=barcode)
        if barcode_queryset.count() == 0:
            raise make_conflict_exception(
                "Free barcode with such number does not exist."
            )
        barcode_instance = barcode_queryset[0]
        instance.initialize(barcode_instance)
