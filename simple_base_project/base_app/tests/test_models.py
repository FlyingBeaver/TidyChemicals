from collections import Counter, OrderedDict
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from rdkit.Chem.rdmolfiles import MolFromMolBlock
from base_app.models import *
from base_app.tests.initial_setup import (create_periodic_system,
                                          create_quantity_units)
from profiles.models import Profile
from profiles.views import logout_invisible, RegistrationPage
from base_app.tests.substances import substances


class ChemicalTestCase(TestCase):
    def setUp(self):
        self.krtek, self.vigri = self.create_users()
        create_periodic_system()
        create_quantity_units()
        self.shkaf, self.door, self.drawer = self.create_storages()

        self.liter = QuantityUnit.objects.get(unit_symbol='l')
        self.milliliter = QuantityUnit.objects.get(unit_symbol='ml')
        self.gram = QuantityUnit.objects.get(unit_symbol='g')
        self.kilogram = QuantityUnit.objects.get(unit_symbol='kg')
        self.milligram = QuantityUnit.objects.get(unit_symbol='mg')

        self.create_chemicals()
        self.create_properties_dict()

        self.struct_element_rels_before = set(StructElementRel.objects.all())
        self.all_chemicals_before = set(Chemical.objects.all())

        self.test_substance = Chemical.create(
            self.properties_dict,
            self.elements_dict
        )
    
    def create_properties_dict(self):
        self.properties_dict = substances[-1]
        with open('base_app/tests/substances_for_test/' +
                  self.properties_dict["name"] +
                  '.mol', "rt", encoding="utf-8") as file:
            self.properties_dict["mol_block"] = file.read()
        self.properties_dict["storage_place"] = self.drawer
        self.properties_dict["quantity_unit"] = self.gram
        self.properties_dict["quantity"] = 135.0
        self.properties_dict["who_created"] = self.vigri
        self.elements_dict = self.make_element_dict(
            self.properties_dict["mol_block"]
        )

    def make_element_dict(self, mol_block):
        molecule = MolFromMolBlock(mol_block)
        elem_symbols = []
        for atom in molecule.GetAtoms():
            elem_symbols.append(atom.GetSymbol())
        return dict(Counter(elem_symbols))

    def create_chemicals(self):
        users_list = [self.krtek, self.krtek, self.krtek, self.krtek,
                      self.vigri, self.vigri, self.vigri, self.vigri,
                      self.krtek, self.krtek, self.krtek, self.krtek,
                      self.vigri]
        storages_list = [self.shkaf, self.shkaf, self.shkaf, self.shkaf,
                         self.door, self.door, self.door, self.door,
                         self.drawer, self.drawer, self.drawer, self.drawer,
                         self.shkaf]
        quantities = [(self.milliliter, 200.0),
                      (self.kilogram, 1.0),
                      (self.milligram, 400.0),
                      (self.gram , 350.0),
                      (self.liter , 2.0),
                      (self.gram , 85.0),
                      (self.milliliter, 40.0),
                      (self.gram, 4.5),
                      (self.kilogram, 0.7),
                      (self.gram, 60.0),
                      (self.liter, 0.5),
                      (self.milligram, 800.0),
                      (self.liter , 0.4)]
        for number, subst in enumerate(substances[:-1]):
            file_path = 'base_app/tests/substances_for_test/' + subst["name"] + ".mol"
            with open(file_path, "rt", encoding="utf-8") as file:
                subst["mol_block"] = file.read()
            subst["storage_place"] = storages_list[number]
            subst["quantity_unit"], subst["quantity"] = quantities.pop(0)
            subst["who_created"] = users_list[number]
            elem_dict = self.make_element_dict(subst["mol_block"])
            Chemical.create(subst, elem_dict)
            
    def create_storages(self):
        root = StoragePlace.make_root(root_name="root")
        lab1 = StoragePlace.create("Lab 1", root, False)
        shkaf = StoragePlace.create("Shkaf", lab1, True)
        fridge = StoragePlace.create("Холодильник", lab1, False)
        door = StoragePlace.create("Дверь", fridge, True)
        drawer = StoragePlace.create("Drawer", fridge, True)
        return shkaf, door, drawer

    def create_users(self):
        client = Client()
        response1 = client.post(
            '/registration/',
            {'username': 'Krtek',
             'password1': 'manganuM12345',
             'password2': 'manganuM12345'}
        )
        response2 = client.get(reverse(logout_invisible))
        response3 = client.post(
            '/registration/',
            {'username': 'Vigri',
             'password1': 'berilliuM12345',
             'password2': 'berilliuM12345'}
        )
        krtek = Profile.objects.get(user__username="Krtek")
        vigri = Profile.objects.get(user__username="Vigri")
        if krtek and vigri:
            return krtek, vigri
    
    def test_chemicals_create1(self):
        struct_element_rels_after = StructElementRel.objects.all()
        SER_after = set(struct_element_rels_after)
        SER_delta = SER_after - self.struct_element_rels_before
        self.assertEqual(len(self.elements_dict), len(SER_delta))
        elements_and_indices = dict()
        for item in SER_delta:
            elements_and_indices[item.element.symbol] = item.index
        self.assertEqual(elements_and_indices, self.elements_dict)
        self.assertTrue(all([x.chemical == self.test_substance \
            for x in SER_delta]))
    
    def test_chemicals_create2(self):
        all_chemicals_after = set(Chemical.objects.all())
        all_chemicals_delta = all_chemicals_after - self.all_chemicals_before
        self.assertEqual(len(all_chemicals_delta), 1)
        new_chemical = all_chemicals_delta.pop()
        self.assertEqual(self.test_substance, new_chemical)
        self.assertTrue(all(
            [getattr(self.test_substance, x) == self.properties_dict[x] \
             for x in self.properties_dict]
            )
        )
