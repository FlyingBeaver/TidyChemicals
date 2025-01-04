from decimal import Decimal
from pprint import pprint
from rest_framework.serializers import (ModelSerializer,
                                        ListSerializer)
from django.contrib.auth.models import User
from chemicals.models import Chemical
from chemicals.services.rendering_paginator import create_svg_alt
from profiles.models import Hashtag, Ampersandtag
from api.services.make_summaries import make_summary


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
        (generated_fields,
         elem_dict,
         path_dict,
         ring_dict) = make_summary(
            validated_data.get("mol_block", None),
            validated_data.get("structure", None),
            self.context["request"].user.profile,
            "create"
        )
        validated_data.update(generated_fields)
        return Chemical.create(validated_data,
                               elem_dict,
                               path_dict,
                               ring_dict)

    #def update(self, instance, validated_data):
