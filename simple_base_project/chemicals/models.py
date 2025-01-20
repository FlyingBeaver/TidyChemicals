import copy
from datetime import datetime
from warnings import warn
from pprint import pprint
from collections import OrderedDict, namedtuple

from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from profiles.models import Profile
from chemicals.services.correction_and_validation import (
    summary_dict_validation,
    check_and_correct,
    are_there_required_keys,
    check_type,
    none_case_validation
)
from chemicals.services.exceptions import DatabaseException


BARCODE_STANDARDS = {
    "storages": "Code 128",
    "chemicals": "QR Code"
}


def default_water_number():
    return 0


class Chemical(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    name_data = models.JSONField()
    water_number = models.JSONField(default=default_water_number)
    mol_block = models.TextField(null=True)
    molecular_formula = models.CharField(max_length=128, null=True)
    molar_mass = models.DecimalField(max_digits=16,
                                     decimal_places=4,
                                     null=True)
    synonym = models.TextField(null=True)
    synonym_data = models.JSONField(null=True)
    comment = models.TextField(null=True)
    comment_data = models.JSONField(null=True)
    cas = models.PositiveBigIntegerField(null=True)
    storage_place = models.ForeignKey("StoragePlace",
                                      on_delete=models.PROTECT,
                                      null=True)
    # PROTECT -- нельзя будет удалить StaragePlace, пока в нём
    # ещё находятся какие-то реактивы
    quantity = models.DecimalField(max_digits=16,
                                   decimal_places=4)
    quantity_unit = models.ForeignKey("QuantityUnit",
                                      on_delete=models.PROTECT)
    # PROTECT -- нельзя будет удалить единицу количества, пока
    # она используется хотя бы в одной из записей для обозначения
    # количества
    hazard_pictograms = models.CharField(null=True, max_length=256)
    when_created = models.DateField(auto_now_add=True)
    when_updated = models.DateField(null=True, default=None)
    who_created = models.ForeignKey(Profile,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name="created_chemical_records")
    who_updated = models.ForeignKey(Profile,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name="updated_chemical_records")
    barcode = models.PositiveIntegerField(null=True,
                                          unique=True,
                                          default=None)
    taken_by = models.ForeignKey(Profile,
                                 on_delete=models.SET_NULL,
                                 null=True)
    date_time_taken = models.DateTimeField(null=True)

    class Meta:
       ordering = ['id']

    @property
    def initialized(self):
        return self.barcode is not None

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

        storage_place = summary.get("storage_place")
        if storage_place:
            if not storage_place.initialized:
                raise DatabaseException("Attempt to place a "
                    "chemical in uninitialized storage. Uninitialized "
                    "storages are supposed to contain other "
                    "storages, not chemicals")
            elif not storage_place.has_children:
                storage_place.contains_chemicals = True
                storage_place.save()

        for element_symbol, n_of_occurrences in elem_dict.items():
            element = Element.get_by_symbol(element_symbol)
            element.increment_n_of_chemicals()
            Chemical_Element.create(element,
                                    new_chemical,
                                    n_of_occurrences)

        for label, n_of_occurrences in path_dict.items():
            try:
                path = Path.get_by_label(label)
            except ValueError:
                path = Path.create(label)
            path.increment()
            Chemical_Path.create(path,
                                 new_chemical,
                                 n_of_occurrences)

        for label, n_of_occurrences in ring_dict.items():
            try:
                ring = Ring.get_by_label(label)
            except ValueError:
                ring = Ring.create(label)
            ring.increment()
            Chemical_Ring.create(ring,
                                 new_chemical,
                                 n_of_occurrences)
        return new_chemical

    def update(self, summary: dict,
               elem_dict: (dict, OrderedDict, None.__class__),
               path_dict: (dict, OrderedDict, None.__class__),
               ring_dict: (dict, OrderedDict, None.__class__)):
        summary_dict_validation(summary)
        none_case_validation(summary,
                             elem_dict,
                             path_dict,
                             ring_dict)
        self.update_related_elem(elem_dict)
        self.update_related_path(path_dict)
        self.update_related_ring(ring_dict)
        
        old_storage = None
        if "storage_place" in summary:
            storage_place = summary["storage_place"]
            if not storage_place.initialized:
                raise DatabaseException(
                    "Attempt to put chemical in uninitialized "
                    "storage. Uninitialized storages can't "
                    "contain chemicals, only other storages."
                )
            elif not storage_place.contains_chemicals:
                storage_place.contains_chemicals = True
                storage_place.save()
            old_storage = self.storage_place
        
        self.when_updated = datetime.now().date()

        for key, value in summary.items():
            setattr(self, key, value)
        self.save()

        if old_storage is not None:
            self.process_old_storage(old_storage)

    def process_old_storage(self, old_storage):
        chemicals_in_old_storage = self.__class__.objects.filter(
            storage_place=old_storage
        )
        if (len(chemicals_in_old_storage) == 0 and
                old_storage.contains_chemicals):
            old_storage.contains_chemicals = False
            old_storage.save()

    def update_related_elem(self, elem_dict):
        if elem_dict == dict():
            return None
        elif elem_dict is None:
            self.destroy_related_elem()
            return None
        relations = Chemical_Element.objects.filter(chemical=self)
        new_elem_dict = copy.copy(elem_dict)
        AboutElement = namedtuple("AboutElement", 
                                 ['symbol',
                                  'element_obj',
                                  'old_n_of_occurrences',
                                  'new_n_of_occurrences',
                                  'relation'])
        about_old_elements = []
        # Здесь он собирает в about_old_elements инфу о тех
        # элементах, которые согласно неотредактированной записи
        # содержатся в веществе.
        for rel in relations:
            about = AboutElement(
                symbol=rel.element.symbol,
                element_obj=rel.element,
                old_n_of_occurrences=rel.n_of_occurrences,
                new_n_of_occurrences=elem_dict.get(rel.element.symbol),
                # если в elem_dict нет этого элемента,
                # new_n_of_occurrences примет значение None
                relation=rel
            )
            about_old_elements.append(about)
            new_elem_dict.pop(about.symbol, None)
        # В конце в new_elem_dict
        # остаются только те элементы, которых раньше не было, но
        # в новом elem_dict они появились.
        
        for element_info in about_old_elements:
            # Удаление Chemical_Element тех элементов,
            # которых больше нет:
            if not element_info.new_n_of_occurrences:
                element_info.relation.delete()
                element_info.element_obj.decrement_n_of_chemicals()
            # Ничего не делать, если индексы равны:
            elif (element_info.new_n_of_occurrences ==
                  element_info.old_n_of_occurrences):
                continue
            # Перезаписать, если поменялся:
            elif (element_info.new_n_of_occurrences !=
                  element_info.old_n_of_occurrences):
                element_info.relation.n_of_occurrences =\
                    element_info.new_n_of_occurrences
                element_info.relation.save()
        
        for elem_sym, n_of_occurrences in new_elem_dict.items():
            element = Element.get_by_symbol(elem_sym)
            Chemical_Element.create(element, self, n_of_occurrences)
            element.increment_n_of_chemicals()

    def update_related_path(self, path_dict):
        if path_dict == dict():
            return None
        elif path_dict is None:
            self.destroy_related_path()
            return None
        old_relations = Chemical_Path.objects.filter(chemical=self)
        old_relations_dict = {rel.path.label:rel
                              for rel in old_relations}
        old_path_dict = {rel.path.label:rel.n_of_occurrences
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
                rel.n_of_occurrences = path_dict[label]
                rel.save()

        for label in new_path_labels:
            try:
                path_instance = Path.get_by_label(label)
            except ValueError:
                path_instance = Path.create(label)
            rel = Chemical_Path.create(path_instance,
                                       self,
                                       path_dict[label])
            # rel = Chemical_Element.create(label,
            #                               self,
            #                               new_path_labels[label])

    def update_related_ring(self, ring_dict):
        if ring_dict == dict():
            return None
        elif ring_dict is None:
            self.destroy_related_ring()
            return None
        old_relations = Chemical_Ring.objects.filter(chemical=self)
        old_relations_dict = {rel.ring.label:rel
                              for rel in old_relations}
        old_ring_dict = {rel.path.ring:rel.n_of_occurrences
                         for rel in old_relations}
        unnecessary_ring_labels = (
            set(old_ring_dict) - set(ring_dict)
        )
        common_ring_labels = set(old_ring_dict) - set(ring_dict)
        new_path_labels = set(ring_dict) - set(old_ring_dict)
        for label in unnecessary_ring_labels:
            rel = old_relations_dict[label]
            rel.delete()

        for label in common_ring_labels:
            if old_ring_dict[label] != path_dict[label]:
                rel = old_relations_dict[label]
                rel.n_of_occurrences = path_dict[label]
                rel.save()

        for label in new_ring_labels:
            rel = Chemical_Ring.create(label,
                                       self,
                                       new_ring_labels[label])
    
    def destroy_related_elem(self):
        relations = Chemical_Element.objects.filter(chemical=self)
        for rel in relations:
            rel.delete()

    def destroy_related_path(self):
        relations = Chemical_Path.objects.filter(chemical=self)
        for rel in relations:
            rel.delete()

    def destroy_related_ring(self):
        relations = Chemical_Ring.objects.filter(chemical=self)
        for rel in relations:
            rel.delete()

    def delete(self, *args, **kwargs):
        old_storage = self.storage_place
        relations_elem = Chemical_Element.objects.filter(
            chemical=self
        )
        for rel in relations_elem:
            rel.element.decrement_n_of_chemicals()
        relations_path = Chemical_Path.objects.filter(
            chemical=self
        )
        for rel in relations_path:
            rel.path.decrement()
        relations_ring = Chemical_Ring.objects.filter(
            chemical=self
        )
        for rel in relations_ring:
            rel.ring.decrement()
        super().delete(*args, **kwargs)
        if old_storage is not None:
            self.process_old_storage(old_storage)

    def initialize(self, barcode=None, storage=None):
        if barcode is None:
            raise ValueError("'barcode' argument is required")
        check_type(argument=barcode,
                   type="FreeBarcode",
                   argument_name="barcode")
        if self.barcode is not None:
            warn("Attempt to initialize chemical that already "
                 "has been initialized")
            return None
        if barcode.standard != BARCODE_STANDARDS["chemicals"]:
            raise DatabaseException("Standard of barcode proposed "
                "for chemical initialization doesn't match with "
                "standard set for chemicals")
        self.barcode = barcode.number
        barcode.delete()
        if storage is not None and self.storage_place is not None:
            warn("Attempt to set storage place during "
                 "initialization, but it was already set")
        elif self.storage_place is None and storage is not None:
            check_type(argument=storage,
                       type=StoragePlace,
                       argument_name="storage")
            self.storage_place = storage
        self.save()

    def take(self, person):
        check_type(argument=person,
                   type=Profile,
                   argument_name="person")
        if self.taken_by is None:
            self.taken_by = person
            self.date_time_taken = datetime.now()
            self.save()
        else:
            raise DatabaseException("Can't take chemical that "
                                    "was already taken")

    def return_(self, storage):
        check_type(argument=storage,
                   type=StoragePlace,
                   argument_name="storage")
        if self.taken_by is None:
            warn("Attempt to return a chemical that was not taken")
            return None
        if self.storage_place != storage:
            raise DatabaseException("Attempt to return: wrong "
                                    "storage place")
        self.taken_by = None
        self.date_time_taken = None
        self.save()

    def take_already_taken(self, person):
        check_type(argument=person,
                   type=Profile,
                   argument_name="person")
        self.taken_by = person
        self.date_time_taken = datetime.now()
        self.save()

    def __str__(self):
        return (f"Chemical named {self.name}, "
                f"{self.molecular_formula}")


class Element(models.Model):
    z = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    symbol = models.CharField(max_length=3, unique=True)
    atomic_weight = models.DecimalField(max_digits=7,
                                        decimal_places=4)
    contained_by = models.ManyToManyField(
        Chemical,
        through="Chemical_Element"
    )
    n_of_chemicals = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.symbol

    def increment_n_of_chemicals(self):
        self.n_of_chemicals += 1
        self.save()

    def decrement_n_of_chemicals(self):
        if self.n_of_chemicals > 0:
            self.n_of_chemicals -= 1
            self.save()
        else:
            raise DatabaseException(
                "Trying to decrement n_of_chemicals "
                f"of the element {self}, while "
                "n_of_chemicals is 0"
            )

    @classmethod
    def get_by_symbol(cls, symbol: str):
        try:
            element = cls.objects.get(symbol=symbol)
        except ObjectDoesNotExist:
            raise ValueError(f"Method get_by_symbol(): element "
                             f"with symbol '{symbol}' "
                             "does not exist")
        return element

    @classmethod
    def get_ordered_elements_list(cls):
        ordered_list_of_selves = \
            list(cls.objects.all().order_by("n_of_chemicals"))
        list_of_symbols = list(map(lambda x: x.symbol,
                                   ordered_list_of_selves)
                               )
        return list_of_symbols

    class Meta:
        ordering = ["z"]


class Path(models.Model):
    label = models.CharField(max_length=1024, primary_key=True)
    n_of_chemicals = models.PositiveBigIntegerField()
    contained_by = models.ManyToManyField(Chemical,
                                          through="Chemical_Path")

    def __str__(self):
        return self.label

    @classmethod
    def get_by_label(cls, label: str):
        try:
            path = cls.objects.get(label=label)
        except ObjectDoesNotExist:
            raise ValueError("Method get_by_label() of Path: "
                             f"path with symbol '{label}' does "
                             "not exist")
        return path

    def increment(self):
        self.n_of_chemicals += 1
        self.save()

    def decrement(self):
        if self.n_of_chemicals == 1:
            self.delete()
        elif self.n_of_chemicals > 1:
            self.n_of_chemicals -= 1
            self.save()
        else:
            raise DatabaseException("n_of_chemicals <= 0")
    
    @classmethod
    def create(cls, label: str):
        instance = cls(label=label, n_of_chemicals=1)
        instance.save()
        return instance

    @classmethod
    def order_path_dict(cls, path_dict):
        PathItem = namedtuple("PathItem",
                             ["label",
                              "n_of_occurrences",
                              "n_of_chemicals"])
        path_items = []
        for label, n_of_occurrences in path_dict.items():
            queryset = cls.objects.filter(label=label)
            if len(queryset) == 0:
                n_of_chemicals = 0
            else:
                n_of_chemicals = queryset[0].n_of_chemicals
            path_items.append(
                PathItem(
                    label=label,
                    n_of_occurrences=n_of_occurrences,
                    n_of_chemicals=n_of_chemicals
                )
            )
        path_items.sort(key=lambda x: x.n_of_chemicals)
        result = OrderedDict()
        for item in path_items:
            result[item.label] = item.n_of_occurrences
        return result


class Ring(models.Model):
    label = models.CharField(max_length=1024, primary_key=True)
    n_of_chemicals = models.PositiveBigIntegerField()
    contained_by = models.ManyToManyField(Chemical,
                                          through="Chemical_Ring")

    def __str__(self):
        return self.label

    @classmethod
    def get_by_label(cls, label: str):
        try:
            ring = cls.objects.get(label=label)
        except ObjectDoesNotExist:
            raise ValueError("Method get_by_label() of Ring: "
                             f"ring with symbol '{label}' does "
                             "not exist")
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


class Chemical_Path(models.Model):
    path = models.ForeignKey(Path,
                             on_delete=models.CASCADE)
    chemical = models.ForeignKey(Chemical,
                                 on_delete=models.CASCADE)
    n_of_occurrences = models.PositiveIntegerField()

    class Meta:
        unique_together = [["path", "chemical"]]
        verbose_name = ("ManyToMany table with "
                        "n of path occurences field")

    @classmethod
    def create(cls, path: Path,
               chemical: Chemical,
               n_of_occurrences: int):
        if n_of_occurrences <= 0:
            raise DatabaseException("Chemical_Path: "
                                    "n_of_occurrences must be "
                                    "positive")
        else:
            relation = cls(path=path,
                           chemical=chemical,
                           n_of_occurrences=n_of_occurrences)
            relation.save()
            return relation
    
    def delete(self):
        self.path.decrement()
        super().delete()


class Chemical_Ring(models.Model):
    ring = models.ForeignKey(Ring,
                             on_delete=models.CASCADE)
    chemical = models.ForeignKey(Chemical,
                                 on_delete=models.CASCADE)
    n_of_occurrences = models.PositiveIntegerField()

    class Meta:
        unique_together = [["ring", "chemical"]]
        verbose_name = ("ManyToMany table with "
                        "n of ring occurences field")

    @classmethod
    def create(cls, ring: Ring,
               chemical: Chemical,
               n_of_occurrences: int):
        if n_of_occurrences <= 0:
            raise DatabaseException("Chemical_Ring: "
                                    "n_of_occurrences must be "
                                    "positive")
        else:
            relation = cls(ring=ring,
                           chemical=chemical,
                           n_of_occurrences=n_of_occurrences)
            relation.save()
            return relation

    def delete(self):
        self.ring.decrement()
        super().delete()


class Chemical_Element(models.Model):
    element = models.ForeignKey(Element,
                                on_delete=models.CASCADE)
    chemical = models.ForeignKey(Chemical,
                                 on_delete=models.CASCADE)
    # CASCADE -- если удаляется реактив или элемент, удяляются
    # и Chemical_Element, которые ему соответствуют
    n_of_occurrences = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [["element", "chemical"]]
        verbose_name = "ManyToMany table with n of atoms field"

    @classmethod
    def create(cls,
               element: Element,
               chemical: Chemical,
               n_of_occurrences: int):
        if n_of_occurrences <= 0:
            raise DatabaseException("Chemical_Element: "
                "n_of_occurrences must be positive"
            )
        relation = cls(element=element,
                       chemical=chemical,
                       n_of_occurrences=n_of_occurrences)
        relation.save()
        return relation

    def delete(self):
        self.element.decrement_n_of_chemicals()
        super().delete()


class StoragePlace(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)
    level = models.SmallIntegerField()
    parent = models.IntegerField(null=True)
    contains_chemicals = models.BooleanField(default=False)
    path_str = models.CharField(max_length=1024)
    barcode = models.PositiveIntegerField(null=True,
                                          unique=True,
                                          default=None)

    @property
    def initialized(self):
        return self.barcode is not None

    @classmethod
    def make_root(cls, root_name="Root"):
        possible_roots = cls.objects.filter(
            Q(parent=None) | Q(level=0)
        )
        if len(possible_roots) > 1:
            raise DatabaseException(
                "several root-like objects found: "
                f"{possible_roots}"
            )
        elif not possible_roots:
            new_root = cls(name=root_name,
                           level=0,
                           parent=None,
                           path_str=root_name)
            new_root.save()
            return new_root
        else:
            root = possible_roots[0]
            return root

    @classmethod
    def create(cls,
               name: str,
               parent):
        cls.check_parent(parent)
        level = parent.level + 1
        parent_path = parent.path_str
        self_path = parent_path + '/' + name
        parent_no = parent.id
        if not parent.is_this_child_name_available(name):
            raise DatabaseException("Attempt to create in "
                "the storage second child storage with the "
                "same name. Storage names inside of a parent "
                "storage must be unique. Try to choose another "
                "name."
            )
        new_storage = cls(name=name,
                          parent=parent_no,
                          level=level,
                          path_str=self_path)
        new_storage.save()
        return new_storage

    def delete(self):
        if self.contains_chemicals:
            children = Chemical.objects.filter(storage_place=self)
            if len(children) > 0:
                raise DatabaseException("Attempt to delete a "
                    "storage that contains chemicals")
        else:
            children = self.__class__.objects.filter(parent=self.id)
            if len(children) > 0:
                raise DatabaseException("Attempt to delete a "
                    "storage that contains other storages")
        super().delete()

    def move(self, new_parent):
        self.__class__.check_parent(new_parent)
        if new_parent == self:
            raise DatabaseException("Attempt to place a storage "
                "into itself")
        upper_storage_id = new_parent.parent
        while upper_storage_id is not None:
            if upper_storage_id == self.id:
                raise DatabaseException("Attempt to place a "
                    "storage into one of it's decendants")
            upper_storage = self.__class__.objects.get(
                id=upper_storage_id
            )
            upper_storage_id = upper_storage.parent

        new_level = new_parent.level + 1
        new_path = new_parent.path_str + "/" + self.name
        self.level = new_level
        self.path_str = new_path
        self.parent = new_parent.id
        self.save()
    
    def rename(self, new_name: str):
        if self.level == 0:
            self.name = new_name
            self.save()
            return None
        parent = self.__class__.objects.get(id=self.parent)
        if parent.is_this_child_name_available(new_name):
            self.name = new_name
            self.save()
        else:
            raise DatabaseException("Attempt to move the storage "
                "to another parent storage, but new parent "
                "storage already has a child storage with the "
                "same name. Storage names inside of a parent "
                "storage must be unique. Try to rename the "
                "storage first."
            )
    
    def is_this_child_name_available(self, name: str):
        queryset = self.__class__.objects.filter(parent=self.id,
                                                 name=name)
        return queryset.count() == 0

    @classmethod
    def check_parent(cls, parent):
        check_type(argument=parent,
                   type=cls,
                   argument_name="parent")
        if parent.initialized:
            raise DatabaseException(
                "Parent storage marked as initialized, so it "
                "has to contain chemicals."
            )

    def __str__(self):
        return self.path_str

    @property
    def has_children(self):
        return len(
            self.__class__.objects.filter(parent=self.id)
        ) > 0

    def initialize(self, barcode):
        check_type(argument=barcode,
                   type="FreeBarcode",
                   argument_name="barcode")
        if self.barcode is not None:
            warn("Trying to initialize the storage that already "
                 "has been initialized")
            return None
        if barcode.standard != BARCODE_STANDARDS["storages"]:
            raise DatabaseException("Attempt to assign to the "
                "storage bacode of wrong format")
        self.barcode = barcode.number
        barcode.delete()
        self.save()


class QuantityUnit(models.Model):
    unit_symbol = models.CharField(primary_key=True,
                                   max_length=32,
                                   unique=True)
    name = models.CharField(max_length=32, unique=True)
    measure_type = models.CharField(max_length=32)
    relation_to_basic = models.DecimalField(max_digits=64,
                                            decimal_places=32,
                                            null=False)
    comment = models.TextField(null=True)
    # Как минимум кг, г, л, мл, мг

    def __str__(self):
        return self.unit_symbol
