import re
from collections import OrderedDict
from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class DatabaseException(BaseException):
    pass


class Chemical(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    name_format = models.JSONField(max_length=256, blank=True)
    structure = models.JSONField(max_length=4096, blank=True)
    # Пока что у структуры будет 2 поля:
    # обязательное inchi и факультативное aq
    mol_block = models.TextField(blank=True)
    molecular_formula = models.CharField(max_length=128, blank=True)
    molar_mass = models.FloatField(blank=True)
    synonym = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    cas = models.IntegerField(null=True, blank=True)
    storage_place = models.ForeignKey("StoragePlace",
                                      on_delete=models.PROTECT)
    # PROTECT -- нельзя будет удалить StaragePlace, пока в нём
    # ещё находятся какие-то реактивы
    quantity = models.FloatField()
    quantity_unit = models.ForeignKey("QuantityUnit",
                                      on_delete=models.PROTECT)
    # PROTECT -- нельзя будет удалить единицу количества, пока
    # она используется хотя бы в одной из записей для обозначения
    # количества
    hazard_pictograms = models.TextField(null=True)

    # Собирать все данные и упаковывать их в словарь должна
    # внешняя функция. Этот метод должен только принять
    # словарь, разложить это по полям базы и сохранить,
    # также обеспечив регистрацию вещества в ElementAbundance
    # и в StructElementRel
    @classmethod
    def create(cls, summary: dict, elem_dict: (dict, OrderedDict)):
        reversed_dir = reversed(dir(cls))
        if not all(map(lambda x: x in reversed_dir, summary.keys())):
            raise ValueError("Some wrong keys in 'summary' dict")
        new_chemical = cls(**summary)
        for element_symbol, index in elem_dict.items():
            element = Element.get_by_symbol(element_symbol)
            ElementAbundance.increment(element)
            StructElementRel.create(element, new_chemical, index)

    def update(self, summary: dict, ):
        pass


class Element(models.Model):
    z = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    symbol = models.CharField(max_length=3, unique=True)
    atomic_weight = models.FloatField()
    contained_by = models.ManyToManyField(Chemical,
                                          through="StructElementRel")

    def __str__(self):
        return f"Element: {self.symbol}"

    @classmethod
    def get_by_symbol(cls, symbol: str):
        return cls.objects.get(symbol=symbol)


class ElementAbundance(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    n_of_chemicals = models.BigIntegerField(default=0)

    @classmethod
    def increment(cls, element_: Element):
        try:
            instance_to_increment = cls.objects.get(element=element_)
        except ObjectDoesNotExist:
            instance_to_increment = cls(element=element_)
        instance_to_increment.n_of_chemicals += 1
        instance_to_increment.save()

    @classmethod
    def decrement(cls, element_: Element):
        instance_to_decrement = cls.objects.get(element=element_)
        instance_to_decrement.n_of_chemicals -= 1
        instance_to_decrement.save()

    @classmethod
    def get_abundance_list(cls):
        return list(cls.objects.all().order_by("-n_of_chemicals"))

    def __str__(self):
        result = f"ElementAbundance: {self.element} in {self.n_of_chemicals};"


class StructElementRel(models.Model):
    element = models.ForeignKey(Element,
                                on_delete=models.CASCADE)
    chemical = models.ForeignKey(Chemical,
                                 on_delete=models.CASCADE)
    # CASCADE -- если удаляется реактив или элемент, удяляются
    # и StructElementRel, которые ему соответствуют
    index = models.SmallIntegerField()

    class Meta:
        unique_together = [["element", "chemical"]]

    @classmethod
    def create(cls, element: Element, chemical: Chemical, index: int):
        return cls(element=element, chemical=chemical, index=index)


class StoragePlace(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    level = models.SmallIntegerField()
    parent = models.IntegerField(null=True)
    terminal = models.BooleanField()

    @classmethod
    def make_root(cls, root_name="Root"):
        possible_roots = cls.objects.filter(Q(parent=None) | Q(level=0))
        if len(possible_roots) > 1:
            raise DatabaseException(f"several root-like objects found: "
                                    f"{possible_roots}")
        elif not possible_roots:
            new_root = cls(name=root_name, level=0,
                           parent=None, terminal=False)
            new_root.save()
        else:
            root = possible_roots[0]
            if not root.terminal:
                raise DatabaseException(f"terminal root found: {root}")
            else:
                raise DatabaseException(f"There was an attempt to create "
                                        f"a new root but it already "
                                        f"exists: {root}")

    @classmethod
    def create(cls, name: str, parent, terminal: bool):
        if not isinstance(parent, cls):
            raise TypeError("'Parent' object must be an instance of "
                            "StoragePlace class")
        level = parent.level
        level += 1
        new_storage = cls(name=name, parent=parent,
                          level=level, terminal=terminal)
        new_storage.save()


class QuantityUnit(models.Model):
    name = models.CharField(max_length=32, unique=True)
    unit_symbol = models.CharField(max_length=32, unique=True)
    measure_type = models.CharField(max_length=32)
    relation_to_basic = models.FloatField(null=True)
    comment = models.TextField()
    # Как минимум кг, г, л, мл, мг

