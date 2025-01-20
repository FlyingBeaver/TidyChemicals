from random import seed, choice, randint
from decimal import Decimal
from pprint import pprint
from collections import namedtuple
from pathlib import Path
from unittest import skip
from decimal import Decimal as D
from django.test import TestCase, Client
from django.urls import reverse
from yaml import load, Loader
from profiles.views import logout_invisible
from chemicals.models import (
    Chemical,
    Chemical_Element,
    Chemical_Path,
    Chemical_Ring,
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
from api.tests.setup import (
    BasicApiTest,
    SUBSTANCES_PATH,
    make_name_data_dict,
    rchoice
)


seed(1)

citrate_path = SUBSTANCES_PATH / "Disodium hydrogen citrate.mol"
with open(citrate_path, "rt", encoding="utf-8") as file:
    CITRATE_MOL = file.read()

testcases_path = (Path(__file__).resolve().parent /
                  "post_put_testcases.yaml")
with open(testcases_path, "rt", encoding="utf-8") as file:
    TESTCASES = load(file.read(), Loader=Loader)

sodium_citrate_path = SUBSTANCES_PATH / "Sodium citrate.mol"
with open(citrate_path, "rt", encoding="utf-8") as file:
    SODIUM_CITRATE_MOL = file.read()
    SODIUM_CITRATE_LAZYMOL = LazyMol(SODIUM_CITRATE_MOL,
                                     form="mol_block")


class ChemicalsApiTest(BasicApiTest):
    def test_create_and_delete_chemical(self):
        # data preparation
        with open(SUBSTANCES_PATH / "Ergosterol.mol", "rt", encoding="utf-8") as file:
            mol_block = file.read()
        data_for_creation_request = {
            "name": "Ergosterol",
            "name_data": make_name_data_dict("Ergosterol"),
            "quantity": "200",
            "quantity_unit": "g",
            "mol_block": mol_block
        }

        # login
        self.billie_eilish_logs_in()
        
        # how many instances of Chemical, Chemical_Element,
        # Chemical_Path, Chemical_Ring
        n_of_chemicals = Chemical.objects.all().count()
        n_of_chemical_element = Chemical_Element.objects.all().count()
        n_of_chemical_path = Chemical_Path.objects.all().count()
        n_of_chemical_ring = Chemical_Ring.objects.all().count()

        # sending request
        response = self.client.post(
            "/api/v1/chemicals",
            data_for_creation_request,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        
        # Getting new numbers of instances of Chemical,
        # Chemical_Element, Chemical_Path, Chemical_Ring
        new_n_of_chemicals = Chemical.objects.all().count()
        new_n_of_chemical_element = Chemical_Element.objects.all().count()
        new_n_of_chemical_path = Chemical_Path.objects.all().count()
        new_n_of_chemical_ring = Chemical_Ring.objects.all().count()

        self.assertEqual(new_n_of_chemicals, n_of_chemicals + 1)
        self.assertTrue(new_n_of_chemical_path > n_of_chemical_path)
        self.assertTrue(new_n_of_chemical_element > n_of_chemical_element)
        self.assertTrue(new_n_of_chemical_ring > n_of_chemical_ring)

        # deleting created chemical
        chemical = Chemical.objects.get(name="Ergosterol")
        pk = chemical.id
        response2 = self.client.delete(f"/api/v1/chemicals/{pk}")
        self.assertEqual(response2.status_code, 204)

        last_n_of_chemicals = Chemical.objects.all().count()
        last_n_of_chemical_element = Chemical_Element.objects.all().count()
        last_n_of_chemical_path = Chemical_Path.objects.all().count()
        last_n_of_chemical_ring = Chemical_Ring.objects.all().count()

        self.assertEqual(n_of_chemicals, last_n_of_chemicals)
        self.assertEqual(n_of_chemical_element, last_n_of_chemical_element)
        self.assertEqual(n_of_chemical_path, last_n_of_chemical_path)
        self.assertEqual(n_of_chemical_ring, last_n_of_chemical_ring)

    def test_create_chemical_unauthorized(self):
        with open(SUBSTANCES_PATH / "Ergosterol.mol", "rt", encoding="utf-8") as file:
            mol_block = file.read()
        data_for_creation_request = {
            "name": "Ergosterol",
            "name_data": make_name_data_dict("Ergosterol"),
            "quantity": "200",
            "quantity_unit": "g",
            "mol_block": mol_block
        }
        response = self.client.post(
            "/api/v1/chemicals",
            data_for_creation_request,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_read_chemicals(self):
        self.billie_eilish_logs_in()
        name = self.phosphorus_oxide.name
        storage = self.phosphorus_oxide.storage_place.path_str
        quantity = self.phosphorus_oxide.quantity
        quantity_unit = self.phosphorus_oxide.quantity_unit.unit_symbol
        mol_block = self.phosphorus_oxide.mol_block
        pk = self.phosphorus_oxide.id
        response = self.client.get(f"/api/v1/chemicals/{pk}")
        data = response.data
        self.assertEqual(data["name"], name)
        self.assertEqual(data["storage_place"], storage)
        self.assertEqual(Decimal(data["quantity"]), quantity)
        self.assertEqual(data["quantity_unit"], quantity_unit)
        self.assertEqual(data["mol_block"], mol_block)

    def test_read_chemical_unauthorized(self):
        chemical = rchoice(Chemical.objects.all())
        pk = chemical.id
        response = self.client.get(f"/api/v1/chemicals/{pk}")
        self.assertEqual(response.status_code, 403)

    def test_delete_chemical_unauthorized(self):
        chemical = rchoice(Chemical.objects.all())
        pk = chemical.id
        response = self.client.delete(f"/api/v1/chemicals/{pk}")
        self.assertEqual(response.status_code, 403)

    def test_list_chemicals_unauthorized(self):
        response = self.client.get("/api/v1/chemicals")
        self.assertEqual(response.status_code, 403)

    def test_list_chemicals(self):
        self.billie_eilish_logs_in()
        response = self.client.get("/api/v1/chemicals")
        self.assertEqual(response.status_code, 405)

    def test_create_chemical_without_structure(self):
        self.billie_eilish_logs_in()
        data_for_creation_request = {
            "name": "Ergosterol",
            "name_data": make_name_data_dict("Ergosterol"),
            "quantity": "200",
            "quantity_unit": "g",
        }
        n_of_chemicals = Chemical.objects.all().count()
        n_of_chemical_element = Chemical_Element.objects.all().count()
        n_of_chemical_path = Chemical_Path.objects.all().count()
        n_of_chemical_ring = Chemical_Ring.objects.all().count()

        response = self.client.post(
            "/api/v1/chemicals",
            data_for_creation_request,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        new_n_of_chemicals = Chemical.objects.all().count()
        new_n_of_chemical_element = Chemical_Element.objects.all().count()
        new_n_of_chemical_path = Chemical_Path.objects.all().count()
        new_n_of_chemical_ring = Chemical_Ring.objects.all().count()

        self.assertEqual(new_n_of_chemicals, n_of_chemicals + 1)
        self.assertEqual(new_n_of_chemical_path, n_of_chemical_path)
        self.assertEqual(new_n_of_chemical_element, n_of_chemical_element)
        self.assertEqual(new_n_of_chemical_ring, n_of_chemical_ring)


class ChemicalsPostPutTest(BasicApiTest):
    bad_water_numbers = [
        [0, 2],
        [2, 0],
        -1,
        -2,
        [-1, 2],
        [2, -1],
        [1, 1],
        [2, 2],
        [2, 1],
        [4, 2],
        [1, 1, 1]
    ]

    @staticmethod
    def make_citrate_data():
        return {
            "name": "Disodium hydrogen citrate sesquihydrate",
            "name_data": make_name_data_dict(
                "Disodium hydrogen citrate sesquihydrate"
            ),
            "quantity": 300,
            "quantity_unit": "g",
            "mol_block": CITRATE_MOL,
            "water_number": [3, 2]
        }

    def create_sodium_citrate(self,
                              mol_block_none=None,
                              water_number_zero=None):
        if (mol_block_none and water_number_zero) is None:
            raise ValueError("Both arguments must be True or False")
        summary = {
            "name": "Sodium citrate",
            "name_data": make_name_data_dict("Sodium citrate"),
            "quantity": Decimal("250"),
            "quantity_unit": self.gram,
            "who_created": self.billie_eilish
        }
        if water_number_zero:
            summary["water_number"] = 0
        else:
            summary["water_number"] = 2
        if mol_block_none:
            summary["mol_block"] = None
            chemical = Chemical.create(
                summary,
                SODIUM_CITRATE_LAZYMOL.elements_dict(),
                SODIUM_CITRATE_LAZYMOL.path_dict(),
                SODIUM_CITRATE_LAZYMOL.ring_dict()
            )
        else:
            summary["mol_block"] = SODIUM_CITRATE_MOL
            chemical = Chemical.create(
                summary,
                dict(),
                dict(),
                dict()
            )
        return chemical.id

    @staticmethod
    def delete_chemical(name="", id=None):
        if bool(name) == bool(id):
            raise ValueError("Only one argument per "
                             "calling is accepted")
        if name:
            queryset = Chemical.objects.filter(name=name)
        if id:
            queryset = Chemical.objects.filter(id=id)
        if queryset.count() == 1:
            queryset[0].delete()


    def test_post(self):
        self.billie_eilish_logs_in()
        post_testcases = TESTCASES["post_requests"]
        for testcase_data in post_testcases:
            water_number = testcase_data["water_number"]
            mol_block = testcase_data["mol_block"]
            status_code = testcase_data["status_code"]

            citrate_data = self.make_citrate_data()
            if water_number == "No":
                del citrate_data["water_number"]
            else:
                citrate_data["water_number"] = water_number
            if mol_block == "No":
                del citrate_data["mol_block"]
            elif mol_block is None:
                citrate_data["mol_block"] = None

            with self.subTest(citrate_data=citrate_data,
                              status_code=status_code):
                response = self.client.post(
                    '/api/v1/chemicals',
                    citrate_data,
                    content_type="application/json"
                )
                self.assertEqual(response.status_code, status_code)
            self.delete_chemical(
                "Disodium hydrogen citrate sesquihydrate"
            )
    
    def test_put(self):
        parameters = {
            1: {"mol_block_none": True, "water_number_zero": True},
            2: {"mol_block_none": False, "water_number_zero": True},
            3: {"mol_block_none": False, "water_number_zero": False}
        }
        self.billie_eilish_logs_in()
        for i in range(1, 4):
            put_testcases = TESTCASES[f"put_requests_case_{i}"]
            for testcase_data in put_testcases:
                sodium_citrate_id = self.create_sodium_citrate(
                    **parameters[i]
                )
                water_number = testcase_data["water_number"]
                mol_block = testcase_data["mol_block"]
                status_code = testcase_data["status_code"]

                citrate_data = self.make_citrate_data()
                if water_number == "No":
                    del citrate_data["water_number"]
                else:
                    citrate_data["water_number"] = water_number
                if mol_block == "No":
                    del citrate_data["mol_block"]
                elif mol_block is None:
                    citrate_data["mol_block"] = None

                with self.subTest(citrate_data=citrate_data,
                                  status_code=status_code):
                    response = self.client.put(
                        f'/api/v1/chemicals/{sodium_citrate_id}',
                        citrate_data,
                        content_type="application/json"
                    )
                    self.assertEqual(response.status_code, status_code)
                self.delete_chemical(id=sodium_citrate_id)

    def test_post_bad_water_numbers(self):
        self.billie_eilish_logs_in()
        for wn in self.bad_water_numbers:
            citrate_data = self.make_citrate_data()
            citrate_data["water_number"] = wn
            name = citrate_data["name"]

            with self.subTest(citrate_data=citrate_data):
                response = self.client.post(
                    f'/api/v1/chemicals',
                    citrate_data,
                    content_type="application/json"
                )
                self.assertEqual(response.status_code, 400)
            self.delete_chemical(name=name)

    def test_put_bad_water_numbers(self):
        self.billie_eilish_logs_in()
        for wn in self.bad_water_numbers:
            sodium_citrate_id = self.create_sodium_citrate(
                mol_block_none=False,
                water_number_zero=False
            )
            citrate_data = self.make_citrate_data()
            citrate_data["water_number"] = wn

            with self.subTest(citrate_data=citrate_data):
                response = self.client.put(
                    f"/api/v1/chemicals/{sodium_citrate_id}",
                    citrate_data,
                    content_type="application/json"
                )
                self.assertEqual(response.status_code, 400)
            self.delete_chemical(id=sodium_citrate_id)

    def test_post_good_storage_place(self):
        self.billie_eilish_logs_in()
        citrate_data = self.make_citrate_data()
        storage = rchoice(
            StoragePlace.objects.exclude(barcode=None)
        )
        citrate_data["storage_place"] = storage.id
        response = self.client.post(
            "/api/v1/chemicals",
            citrate_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_post_bad_storage_place(self):
        self.billie_eilish_logs_in()
        citrate_data = self.make_citrate_data()
        storage = rchoice(
            StoragePlace.objects.filter(barcode=None)
        )
        citrate_data["storage_place"] = storage.id
        response = self.client.post(
            "/api/v1/chemicals",
            citrate_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)
