from math import gcd
from rest_framework.serializers import ValidationError


def validate_water_number(water_number):
    if water_number.__class__ not in (int, list):
        raise ValidationError(
            "water_number must be int or list"
        )
    if isinstance(water_number, list):
        if len(water_number) != 2:
            raise ValidationError(
                "In case if water_number is list, "
                "its length must be 2."
            )
        elif not (isinstance(water_number[0], int) and
                isinstance(water_number[1], int)):
            raise ValidationError(
                "One of values of water_number list "
                "is not integer."
            )
        elif water_number[0] <= 0 or water_number[1] <= 0:
            raise ValidationError(
                "One of values of water_number list "
                "is not positive."
            )
        elif gcd(water_number[0], water_number[1]) != 1:
            raise ValidationError(
                "Water number list is representation of fraction, "
                "so greatest common divisor of first and second "
                "value must be equal to 1."
            )
        elif water_number[1] == 1:
            raise ValidationError("Water number list must "
                "represent numerator and denominator of "
                "an irreducible fraction, so water_number[1] "
                "(denominator) can't be 1."
            )
    else:
        if water_number < 0:
            raise ValidationError(
                "If water_number is integer, it must be >= 0."
            )


def update_chemical_validation(validated_data, instance):
    if ("mol_block" in validated_data and
            "water_number" in validated_data):
        if (validated_data["mol_block"] is None and
                validated_data["water_number"] != 0):
            raise ValidationError("Request can't contain "
                "'mol_block' value equal to None and "
                "'water_number' value not equal to 0"
            )
    if ("mol_block" in validated_data and
            not "water_number" in validated_data):
        if (validated_data["mol_block"] is None and
                instance.water_number != 0):
            raise ValidationError("If for a chemical"
                "'water_number' set not equal to 0, "
                "update request can't contain 'mol_block', "
                "equal to None."
            )
    if ("water_number" in validated_data and
            not "mol_block" in validated_data):
        if (validated_data["water_number"] != 0 and
                instance.mol_block is None):
            raise ValidationError("If for a chemical"
                "'mol_block' set equal to None, update "
                "request can't contain 'water_number' not "
                "equal to None"
            )


def create_chemical_validation(validated_data):
    water_number = validated_data.get("water_number", "Nothing")
    mol_block = validated_data.get("mol_block", "Nothing")
    if water_number is None:
        raise ValidationError()
    if (water_number != 0 and
            water_number != "Nothing" and
            (mol_block == "Nothing" or not mol_block)):
        raise ValidationError()