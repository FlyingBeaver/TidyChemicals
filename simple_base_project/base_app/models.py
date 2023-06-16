import re
import datetime
import copy
from warnings import warn
from collections import OrderedDict, namedtuple
from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from profiles.models import Profile
from base_app.correction_and_validation import (summary_dict_validation,
                                                check_and_correct,
                                                are_there_required_keys)


class DatabaseException(BaseException):
    pass


class Chemical(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    name_format = models.JSONField(max_length=256, null=True)
    structure = models.JSONField(max_length=4096, null=True)
    # Пока что у структуры будет 2 поля:
    # обязательное inchi и необязательное aq
    mol_block = models.TextField(null=True)
    molecular_formula = models.CharField(max_length=128, null=True)
    molar_mass = models.FloatField(null=True)
    synonym = models.TextField(null=True)
    comment = models.TextField(null=True)
    cas = models.IntegerField(null=True)
    storage_place = models.ForeignKey("StoragePlace",
                                      on_delete=models.PROTECT,
                                      null=True)
    # PROTECT -- нельзя будет удалить StaragePlace, пока в нём
    # ещё находятся какие-то реактивы
    quantity = models.FloatField()
    # quantity = models.FloatField(default=0.0)
    quantity_unit = models.ForeignKey("QuantityUnit",
                                      on_delete=models.PROTECT,
                                      null=True)
    # PROTECT -- нельзя будет удалить единицу количества, пока
    # она используется хотя бы в одной из записей для обозначения
    # количества
    hazard_pictograms = models.CharField(null=True, max_length=256)
    when_created = models.DateTimeField(auto_now_add=True)
    when_updated = models.DateTimeField(auto_now=True)
    who_created = models.ForeignKey(Profile,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name="created_chemical_records")
    who_updated = models.ForeignKey(Profile,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name="updated_chemical_records")

    @classmethod
    def create(cls, summary: dict,
               elem_dict: (dict, OrderedDict),
               path_dict: (dict, OrderedDict),
               ring_dict: (dict, OrderedDict)):
        are_there_required_keys(summary)
        summary_dict_validation(summary)
        summary = check_and_correct(summary)
        new_chemical = cls(**summary)
        new_chemical.save()

        for element_symbol, index in elem_dict.items():
            element = Element.get_by_symbol(element_symbol)
            ElementAbundance.increment(element)
            StructElementRel.create(element, new_chemical, index)

        for label, n_of_occurences in path_dict.items():
            try:
                path = Path.get_by_label(label)
            except ValueError:
                path = Path.create(label)
            path.increment()
            StructPathRel.create(path, new_chemical, n_of_occurences)

        for label, n_of_occurences in ring_dict.items():
            try:
                ring = Ring.get_by_label(label)
            except ValueError:
                ring = Ring.create(label)
            ring.increment()
            StructRingRel.create(ring, new_chemical, n_of_occurences)

        return new_chemical

    def update(self, summary: dict,
               elem_dict: (dict, OrderedDict),
               path_dict: (dict, OrderedDict)):
        summary_dict_validation(summary)
        self.update_related_elem(elem_dict)
        self.update_related_path(path_dict)
        self.update_related_ring(ring_dict)

        for key, value in summary.items():
            setattr(self, key, value)
        self.save()

    def update_related_elem(self, elem_dict):
        relations = StructElementRel.objects.filter(chemical=self)
        new_elem_dict = copy.copy(elem_dict)
        AboutElement = namedtuple("AboutElement", 
                                 ['symbol', 'element_obj', 'old_index', 
                                  'new_index', 'relation'])
        about_old_elements = []
        # Здесь он собирает в about_old_elements инфу о тех
        # элементах, которые согласно неотредактированной записи
        # содержатся в веществе.
        for rel in relations:
            about = AboutElement(symbol=rel.element.symbol,
                                 element_obj=rel.element,
                                 old_index=rel.index,
                                 new_index=elem_dict.get(rel.element.symbol),
                                 # если в elem_dict нет этого элемента,
                                 # new_index примет значение None
                                 relation=rel)
            about_old_elements.append(about)
            new_elem_dict.pop(about.symbol, None)
        # В конце в new_elem_dict
        # остаются только те элементы, которых раньше не было, но
        # в новом elem_dict они появились.
        
        for i in about_old_elements:
            # Удаление StructElementRel тех элементов,
            # которых больше нет:
            if not i.new_index:
                i.relation.delete()
                ElementAbundance.decrement(i.element_obj)
            # Ничего не делать, если индексы равны:
            elif i.new_index == i.old_index:
                continue
            # Перезаписать, если поменялся:
            elif i.new_index != i.old_index:
                i.relation.index = i.new_index
                i.relation.save()
        
        for elem_sym, index in new_elem_dict.items():
            element = Element.get_by_symbol(elem_sym)
            StructElementRel.create(element, self, index)
            ElementAbundance.increment(element)

    def update_related_path(self, path_dict):
        old_relations = StructPathRel.objects.filter(chemical=self)
        old_relations_dict = {rel.path.label:rel
                              for rel in old_relations}
        old_path_dict = {rel.path.label:rel.n_of_occurences
                         for rel in old_relations}
        unnecessary_path_labels = set(old_path_dict) - set(path_dict)
        common_path_labels = set(old_path_dict) & set(path_dict)
        new_path_labels = set(path_dict) - set(old_path_dict)
        for label in unnecessary_path_labels:
            rel = old_relations_dict[label]
            rel.delete()

        for label in common_path_labels:
            if old_path_dict[label] != path_dict[label]:
                rel = old_relations_dict[label]
                rel.n_of_occurences = path_dict[label]
                rel.save()

        for label in new_path_labels:
            rel = StructElementRel.create(label, self, new_path_labels[label])

    def update_related_ring(self, ring_dict):
        old_relations = StructRingRel.objects.filter(chemical=self)
        old_relations_dict = {rel.ring.label:rel
                              for rel in old_relations}
        old_ring_dict = {rel.path.ring:rel.n_of_occurences
                         for rel in old_relations}
        unnecessary_ring_labels = set(old_ring_dict) - set(ring_dict)
        common_ring_labels = set(old_ring_dict) - set(ring_dict)
        new_path_labels = set(ring_dict) - set(old_ring_dict)
        for label in unnecessary_ring_labels:
            rel = old_relations_dict[label]
            rel.delete()

        for label in common_ring_labels:
            if old_ring_dict[label] != path_dict[label]:
                rel = old_relations_dict[label]
                rel.n_of_occurences = path_dict[label]
                rel.save()

        for label in new_ring_labels:
            rel = StructRingRel.create(label, self, new_ring_labels[label])

    def delete(self, *args, **kwargs):
        relations_elem = StructElementRel.objects.filter(chemical=self)
        for rel in relations_elem:
            ElementAbundance.decrement(rel.element)
        relations_path = StructPathRel.objects.filter(chemical=self)
        for rel in relations_path:
            rel.path.decrement()
        relations_ring = StructRingRel.objects.filter(chemical=self)
        for rel in relations_ring:
            rel.path.decrement()
        super().delete(*args, **kwargs)


class Element(models.Model):
    z = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    symbol = models.CharField(max_length=3, unique=True)
    atomic_weight = models.FloatField()
    contained_by = models.ManyToManyField(Chemical,
                                          through="StructElementRel")

    def __str__(self):
        return self.symbol

    @classmethod
    def get_by_symbol(cls, symbol: str):
        try:
            element = cls.objects.get(symbol=symbol)
        except ObjectDoesNotExist:
            raise ValueError(f"Method get_by_symbol(): element "
                             f"with symbol '{symbol}' does not exist")
        return element

    class Meta:
        ordering = ["z"]


class Path(models.Model):
    label = models.CharField(max_length=1024, primary_key=True)
    n_of_chemicals = models.IntegerField()
    contained_by = models.ManyToManyField(Chemical,
                                          through="StructPathRel")

    def __str__(self):
        return self.label

    @classmethod
    def get_by_label(cls, label: str):
        try:
            path = cls.objects.get(label=label)
        except ObjectDoesNotExist:
            raise ValueError(f"Method get_by_label() of Path: path "
                             f"with symbol '{label}' does not exist")
        return path

    def increment(self):
        self.n_of_chemicals += 1
        self.save()

    def decrement(self):
        if self.n_of_chemicals == 1:
            self.delete()
        else:
            self.n_of_chemicals -= 1
            self.save()
    
    @classmethod
    def create(cls, label: str):
        instance = cls(label=label, n_of_chemicals=0)
        instance.save()
        return instance

    @classmethod
    def order_path_dict(cls, path_dict):
        PathItem = namedtuple("PathItem",
                             ["label",
                              "n_of_occurences",
                              "n_of_chemicals"])
        path_items = []
        for label, n_of_occurences in path_dict.items():
            queryset = cls.objects.filter(label=label)
            if len(queryset) == 0:
                n_of_chemicals = 0
            else:
                n_of_chemicals = queryset[0].n_of_chemicals
            path_items.append(PathItem(label=label,
                                       n_of_occurences=n_of_occurences,
                                       n_of_chemicals=n_of_chemicals))
        path_items.sort(key=lambda x: x.n_of_chemicals)
        result = OrderedDict()
        for item in path_items:
            result[item.label] = item.n_of_occurences
        return result


class Ring(models.Model):
    label = models.CharField(max_length=1024, primary_key=True)
    n_of_chemicals = models.IntegerField()
    contained_by = models.ManyToManyField(Chemical,
                                          through="StructRingRel")

    def __str__(self):
        return self.label

    @classmethod
    def get_by_label(cls, label: str):
        try:
            ring = cls.objects.get(label=label)
        except ObjectDoesNotExist:
            raise ValueError(f"Method get_by_label() of Ring: ring "
                             f"with symbol '{label}' does not exist")
        return ring

    def increment(self):
        self.n_of_chemicals += 1
        self.save()

    def decrement(self):
        if self.n_of_chemicals == 1:
            self.delete()
        else:
            self.n_of_chemicals -= 1
            self.save()

    @classmethod
    def create(cls, label: str):
        instance = cls(label=label, n_of_chemicals=0)
        instance.save()
        return instance

    @classmethod
    def order_ring_dict(cls, ring_dict):
        ring_labels = list(ring_dict.keys())
        queryset = cls.objects.filter(
            label__in=ring_labels
        ).order_by("n_of_chemicals")
        result = OrderedDict()
        for item in queryset:
            result[item.label] = ring_dict[item.label]
        if len(result) == len(ring_dict):
            return result
        else:
            difference = set(ring_dict) - set(result)
            dict_start = OrderedDict()
            for label in difference:
                dict_start[label] = 0
            result = dict_start | result
            return result


class StructPathRel(models.Model):
    path = models.ForeignKey(Path,
                             on_delete=models.CASCADE)
    chemical = models.ForeignKey(Chemical,
                                 on_delete=models.CASCADE)
    n_of_occurences = models.IntegerField()

    class Meta:
        unique_together = [["path", "chemical"]]
        verbose_name = ("ManyToMany table with "
                        "n of path occurences field")

    @classmethod
    def create(cls, path: Path,
               chemical: Chemical,
               n_of_occurences: int):
        if n_of_occurences <= 0:
            raise DatabaseException("StructPathRel: "
                                    "n_of_occurences must be "
                                    "positive")
        else:
            relation = cls(path=path,
                           chemical=chemical,
                           n_of_occurences=n_of_occurences)
            relation.save()
            return relation

class StructRingRel(models.Model):
    ring = models.ForeignKey(Ring,
                             on_delete=models.CASCADE)
    chemical = models.ForeignKey(Chemical,
                                 on_delete=models.CASCADE)
    n_of_occurences = models.IntegerField()

    class Meta:
        unique_together = [["ring", "chemical"]]
        verbose_name = ("ManyToMany table with "
                        "n of ring occurences field")

    @classmethod
    def create(cls, ring: Ring,
               chemical: Chemical,
               n_of_occurences: int):
        if n_of_occurences <= 0:
            raise DatabaseException("StructRingRel: "
                                    "n_of_occurences must be "
                                    "positive")
        else:
            relation = cls(ring=ring,
                           chemical=chemical,
                           n_of_occurences=n_of_occurences)
            relation.save()
            return relation

class ElementAbundance(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    n_of_chemicals = models.BigIntegerField()

    @classmethod
    def increment(cls, element_: Element):
        try:
            instance_to_increment = cls.objects.get(element=element_)
        except ObjectDoesNotExist:
            instance_to_increment = cls(element=element_, n_of_chemicals=0)
        chemicals_number = instance_to_increment.n_of_chemicals
        instance_to_increment.n_of_chemicals = chemicals_number + 1
        instance_to_increment.save()

    @classmethod
    def decrement(cls, element_: Element):
        try:
            instance_to_decrement = cls.objects.get(element=element_)
        except ObjectDoesNotExist:
            warn(f"Trying to decrement unexistant ElementAbundance "
                 f"object for element: {element_}")
        else:
            chemicals_number = instance_to_decrement.n_of_chemicals
            if chemicals_number <= 1:
                instance_to_decrement.delete()
            else:
                instance_to_decrement.n_of_chemicals = chemicals_number - 1
                instance_to_decrement.save()

    @classmethod
    def get_abundance_list(cls):
        ordered_list_of_selves = \
            list(cls.objects.all().order_by("n_of_chemicals"))
        list_of_symbols = list(map(lambda x: x.element.symbol,
                                   ordered_list_of_selves)
                               )
        return list_of_symbols

    def __str__(self):
        result = (f"{self.element}"
                  f" in {self.n_of_chemicals};")
        return result


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
        verbose_name = "ManyToMany table with n of atoms field"

    @classmethod
    def create(cls, element: Element, chemical: Chemical, index: int):
        if index <= 0:
            raise DatabaseException("StructElementRel: "
                                    "index must be positive")
        relation = cls(element=element, chemical=chemical, index=index)
        relation.save()
        return relation


class StoragePlace(models.Model):
    id = models.BigAutoField(primary_key=True, )
    name = models.CharField(max_length=32)
    level = models.SmallIntegerField()
    parent = models.IntegerField(null=True)
    terminal = models.BooleanField()
    path_str = models.CharField(max_length=1024)

    @classmethod
    def make_root(cls, root_name="Root"):
        possible_roots = cls.objects.filter(Q(parent=None) | Q(level=0))
        if len(possible_roots) > 1:
            raise DatabaseException(f"several root-like objects found: "
                                    f"{possible_roots}")
        elif not possible_roots:
            new_root = cls(name=root_name, level=0,
                           parent=None, terminal=False, path_str=root_name)
            new_root.save()
            return new_root
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
        parent_path = parent.path_str
        self_path = str(parent_path) + '/' + name
        parent_no = parent.id
        new_storage = cls(name=name, parent=parent_no,
                          level=level, terminal=terminal,
                          path_str=self_path)
        new_storage.save()
        return new_storage

    def __str__(self):
        return self.path_str


class QuantityUnit(models.Model):
    name = models.CharField(max_length=32, unique=True)
    unit_symbol = models.CharField(max_length=32, unique=True)
    measure_type = models.CharField(max_length=32)
    relation_to_basic = models.DecimalField(max_digits=64,
                                            decimal_places=32,
                                            null=True)
    comment = models.TextField(null=True)
    # Как минимум кг, г, л, мл, мг

    def __str__(self):
        return str(self.name) + f"; symbol: {self.unit_symbol}"
