from random import choice, randint
from collections import namedtuple
from pathlib import Path
from decimal import Decimal as D
from django.test import TestCase, Client
from django.urls import reverse
from profiles.views import logout_invisible
from chemicals.models import (
    Chemical,
    StoragePlace,
    QuantityUnit,
    Element,
    BARCODE_STANDARDS
)
from chemicals.services.mol_classes import LazyMol
from profiles.models import (
    Profile,
    Hashtag,
    Ampersandtag,
    FreeBarcode
)
from simple_base_project.services.elements_units import (
    create_units,
    create_elements
)


SUBSTANCES_PATH = Path(__file__).resolve().parent / "substances"

AMPERSANDTAGS_USERS = {
    "lorem": "LarysaHrybalova",
    "ipsum": "BillieEilish",
}

HASHTAGS = ("dolor", "sit")

HAZARD_TYPES = ['compressed_gas',
                'corrosive',
                'environmental_hazard',
                'explosive',
                'flammable',
                'harmful',
                'health_hazard',
                'oxidizing',
                'toxic']


class InfiniteLoop(BaseException):
    pass


def make_name_data_dict(name):
    return {"html": f"<p>{name}</p>",
            "delta": {"ops":[{"insert":f"{name}\n"}]}}


def dict_to_namedtuple(dictionary):
    NamedTuple = namedtuple("NamedTuple", dictionary.keys())
    return NamedTuple(**dictionary)


def rchoice(seq):
    if seq.__class__.__name__ == "QuerySet":
        length = seq.count()
        return seq[randint(0, length - 1)]
    elif seq.__class__.__name__ == "filter":
        return choice(list(seq))
    else:
        return choice(seq)


def rchoice_exclude(seq, exclude):
    if seq.__class__.__name__ == "filter":
        seq = list(seq)
    result = rchoice(seq)
    i = 0
    while result == exclude:
        result = rchoice(seq)
        i += 1
        if i > 200:
            raise InfiniteLoop()
    return result


class BasicApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        create_units()
        self.extract_units()
        create_elements()
        self.create_storages()
        self.initialize_storages()
        self.create_users()
        self.create_substances()
        self.initialize_chemicals()
        self.create_ampersandtags()
        self.create_hashtags()

    def extract_units(self):
        self.liter = QuantityUnit.objects.get(unit_symbol='l')
        self.milliliter = QuantityUnit.objects.get(unit_symbol='ml')
        self.gram = QuantityUnit.objects.get(unit_symbol='g')
        self.kilogram = QuantityUnit.objects.get(unit_symbol='kg')
        self.milligram = QuantityUnit.objects.get(unit_symbol='mg')

    def create_storages(self):
        self.root = StoragePlace.make_root(root_name="root")
        self.lab1 = StoragePlace.create("Lab1", self.root)
        self.lab2 = StoragePlace.create("Lab2", self.root)

        self.cabinet1 = StoragePlace.create("Cabinet 1", self.lab1)
        self.cabinet2 = StoragePlace.create("Cabinet 2", self.lab1)

        self.cabinet = StoragePlace.create("Cabinet", self.lab2)
        self.fridge = StoragePlace.create("Fridge", self.lab2)
        self.safe = StoragePlace.create("Safe", self.lab1)

    def create_users(self):
        UserData = namedtuple("UserData",
                              ["username",
                               "password",
                               "created_ampersandtag"],
                               defaults=(None,))
        self.darth_vader_data = UserData(username="DarthVader",
                                         password='doEiusmod1')
        response1 = self.client.post(
            '/registration/',
            {'username': self.darth_vader_data.username,
             'password1': self.darth_vader_data.password,
             'password2': self.darth_vader_data.password}
        )
        response2 = self.client.get(reverse(logout_invisible))

        self.billie_eilish_data = UserData(username='BillieEilish',
                                           password='temporIncididunt2',
                                           created_ampersandtag="lorem")
        response3 = self.client.post(
            '/registration/',
            {'username': self.billie_eilish_data.username,
             'password1': self.billie_eilish_data.password,
             'password2': self.billie_eilish_data.password}
        )

        self.larysa_hrybalova_data = UserData(username="LarysaHrybalova",
                                              password='utLaboreEt3',
                                              created_ampersandtag="ipsum")
        response4 = self.client.post(
            '/registration/',
            {'username': self.larysa_hrybalova_data.username,
             'password1': self.larysa_hrybalova_data.password,
             'password2': self.larysa_hrybalova_data.password}
        )
        self.billie_eilish = Profile.objects.get(user__username="BillieEilish")
        self.darth_vader = Profile.objects.get(user__username="DarthVader")
        self.larysa_hrybalova = Profile.objects.get(user__username="LarysaHrybalova")
    
    @staticmethod
    def create_chemical(file: str,
                        quantity: D,
                        unit: QuantityUnit,
                        storage: StoragePlace,
                        creator: Profile,
                        hazards: list,
                        water_number=None):
        name = file.replace(".mol", "")
        summary = dict()
        with open(SUBSTANCES_PATH / file, "rt", encoding="utf-8") as f:
            mol_block = f.read()
        if storage is not None:
            summary.update({"storage_place": storage})
        if hazards is not None:
            summary.update({"hazard_pictograms": ", ".join(hazards)})
        mol = LazyMol(mol_block, form="mol_block")
        elem_dict = mol.elements_dict()
        path_dict = mol.path_dict()
        ring_dict = mol.ring_dict()
        if water_number is not None:
            summary["water_number"] = water_number
        summary.update(
            {
                "mol_block": mol_block,
                "quantity": quantity,
                "quantity_unit": unit,
                "who_created": creator,
                "name": name,
                "name_data": make_name_data_dict(name),
            }
        )
        return Chemical.create(summary, elem_dict, path_dict, ring_dict)

        

    def create_substances(self):
        # pyridine and caffeic supposed to be uninitialized chemicals
        self.buthyl_lithium = self.create_chemical(
            'Buthyl lithium.mol',
            D("50"),
            self.milliliter,
            self.fridge,
            self.darth_vader,
            [
                'flammable',
                'health_hazard',
                'corrosive',
                'harmful',
                'environmental_hazard',
            ]
        )
        self.caffeic_acid = self.create_chemical(
            'Caffeic acid.mol',
            D("10"),
            self.gram,
            None,
            self.larysa_hrybalova,
            ['health_hazard']
        )
        self.calcium_chloride = self.create_chemical(
            'Calcium chloride.mol',
            D("1"),
            self.kilogram,
            self.cabinet1,
            self.darth_vader,
            ['harmful']
        )
        self.phosphorus_oxide = self.create_chemical(
            'Phosphorus (V) oxide.mol',
            D("500"),
            self.gram,
            self.cabinet1,
            self.billie_eilish,
            ["corrosive"]
        )
        self.pyridine = self.create_chemical(
            'Pyridine.mol',
            D("2"),
            self.liter,
            None,
            self.larysa_hrybalova,
            ['harmful', "flammable"]
        )
        self.tbdmsCl = self.create_chemical(
            'tert-Butyldimethylsilyl chloride.mol',
            D("200"),
            self.gram,
            self.fridge,
            self.billie_eilish,
            ['flammable','corrosive','environmental_hazard']
        )

    def initialize_chemicals(self):
        chemicals = [self.buthyl_lithium,
                     self.calcium_chloride,
                     self.phosphorus_oxide,
                     self.tbdmsCl]
        for chemical in chemicals:
            self.initialize_substance(chemical)
        self.initialized_chemicals = chemicals

    def initialize_storages(self):
        storages = [self.cabinet1,
                    self.cabinet2,
                    self.fridge]
        for storage in storages:
            self.initialize_storage(storage)
        self.initialized_storages = storages

    @staticmethod
    def initialize_storage(storage):
        barcode = FreeBarcode.objects.create(
            standard=BARCODE_STANDARDS["storages"]
        )
        storage.initialize(barcode)

    @staticmethod
    def initialize_substance(chemical):
        barcode = FreeBarcode.objects.create(
            standard=BARCODE_STANDARDS["chemicals"]
        )
        chemical.initialize(barcode=barcode)

    def create_hashtags(self):
        HashtagData = namedtuple("HashtagData",
                                 ["tag", "chemicals"])
        self.hashtag1 = HashtagData(
            tag="dolor",
            chemicals=[
                self.buthyl_lithium,
                self.calcium_chloride,
                self.phosphorus_oxide
            ]
        )
        for chemical in self.hashtag1.chemicals:
            Hashtag.bind(chemical,
                         self.hashtag1.tag,
                         self.darth_vader)
        
        self.hashtag2 = HashtagData(
            tag="sit",
            chemicals=[
                self.calcium_chloride,
                self.phosphorus_oxide,
                self.tbdmsCl
            ]
        )
        for chemical in self.hashtag2.chemicals:
            Hashtag.bind(chemical,
                         self.hashtag2.tag,
                         self.darth_vader)

    def create_ampersandtags(self):
        AmpersandtagData = namedtuple("AmpersandtagData",
                                      ["tag",
                                       "creator",
                                       "chemicals"])
        self.ampersandtag1 = AmpersandtagData(
            tag=self.billie_eilish_data.created_ampersandtag,
            creator=self.billie_eilish,
            chemicals=[self.buthyl_lithium,
                       self.calcium_chloride]
        )
        for chemical in self.ampersandtag1.chemicals:
            Ampersandtag.bind(chemical,
                              self.ampersandtag1.tag,
                              self.ampersandtag1.creator)
        
        self.ampersandtag2 = AmpersandtagData(
            tag=self.larysa_hrybalova_data.created_ampersandtag,
            creator=self.larysa_hrybalova,
            chemicals=[self.phosphorus_oxide,
                       self.tbdmsCl]
        )
        for chemical in self.ampersandtag2.chemicals:
            Ampersandtag.bind(chemical,
                              self.ampersandtag2.tag,
                              self.ampersandtag2.creator)

    def billie_eilish_logs_in(self):
        response = self.client.post(
            '/login/',
            {"username": self.billie_eilish_data.username,
             "password": self.billie_eilish_data.password}
        )