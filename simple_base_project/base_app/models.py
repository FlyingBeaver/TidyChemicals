import re
from collections import OrderedDict
from django.db import models
from mol_classes import LazyMol


class Chemical(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=256)
    name_format = models.JSONField(max_length=256)
    structure = models.JSONField(max_length=4096)
    molecular_formula = models.CharField(max_length=128)
    molar_mass = models.FloatField()
    synonym = models.TextField(null=True)
    comment = models.TextField(null=True)
    cas = models.IntegerField(null=True)
    storage_place = models.ForeignKey("StoragePlace",
                                      on_delete=models.PROTECT)
    quantity = models.FloatField()
    quantity_unit = models.ForeignKey()



    @classmethod
    def create(cls, molecule: Mol):
        """
        Создаёт новую структуру в таблице
        """


class Element(models.Model):
    z = models.SmallIntegerField(primary_key=True)
    title = models.CharField(max_length=30)
    symbol = models.CharField(max_length=3)
    atomic_weight = models.FloatField()
    contained_by = models.ManyToManyField(Chemical,
                                          through="StructElementRel")
    n_of_containing = models.IntegerField(default=0)


class StructElementRel(models.Model):
    element = models.ForeignKey(Element,
                                on_delete=models.CASCADE)
    chemical = models.ForeignKey(Chemical,
                                 on_delete=models.CASCADE)
    index = models.SmallIntegerField()

    class Meta:
        unique_together = [["element", "chemical"]]


class StoragePlace(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField()
    level = models.SmallIntegerField()
    parent = models.IntegerField()
    terminal = models.BooleanField()


class QuantityUnit(models.Model):
    name = models.CharField(max_length=32)
    unit_symbol = models.CharField(max_length=32)
    quantity_type = models.ForeignKey("QuantityMeasure",
                                      on_delete=models.PROTECT)
    basic_unit = models.BooleanField()
    relation_to_basic = models.DecimalField(null=True)
    comment = models.TextField()


class QuantityMeasure(models.Model):
    name = models.CharField(max_length=32)
    comment = models.TextField()
