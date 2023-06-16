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


class ModelsTestException(BaseException):
    pass


class ChemicalTestCase(TestCase):
    """Parent class for all tests in here.
       It contains setUp() method and all methods needed for setup"""
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

        self.struct_element_rels_before = set(
            StructElementRel.objects.all()
        )
        self.all_chemicals_before = set(Chemical.objects.all())
        self.chemicals_in_drawer_before = set(
            Chemical.objects.filter(storage_place=self.drawer)
        )
        self.chemicals_with_q_in_grams_before = set(
            Chemical.objects.filter(quantity_unit=self.gram)
        )
        self.chemicals_by_vigri_before = set(
            Chemical.objects.filter(who_created=self.vigri)
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

    def make_abundance_dict(self):
        abundance_dict = dict()
        for element_symbol in self.elements_dict:
            element_obj = Element.objects.get(symbol=element_symbol)
            element_abundance_qset = ElementAbundance.objects.filter(
                element=element_obj
            )
            if len(element_abundance_qset) == 0:
                abundance_number = 0
            elif len(element_abundance_qset) == 1:
                abundance_obj = element_abundance_qset[0]
                abundance_number = abundance_obj.n_of_chemicals
            else:
                raise ModelsTestException("More than 1 instances of "
                    "ElementAbundance for one element"
                )
            abundance_dict[element_obj] = abundance_number
        self.abundance_dict = abundance_dict


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
                      (self.liter , 0.4),
                      (self.milligram, 800.0)]
        for number, subst in enumerate(substances[:-1]):
            file_path = ('base_app/tests/substances_for_test/' +
                subst["name"] + ".mol"
            )
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


class ChemicalCreateTestCase(ChemicalTestCase):
    def setUp(self):
        super().setUp()
        # properties_dict, abundance_dict and elements_dict are
        # about test_substance, elements_dict created inside of
        # create_properties_dict()
        self.create_properties_dict()
        self.make_abundance_dict()

        self.test_substance = Chemical.create(
            self.properties_dict,
            self.elements_dict
        )


    def test_chemicals_create1(self):
        """
        Comparison of StructElementRel.objects.all() before and 
        after creation of the chemical. Number of new SER must be equal
        to number of elements in the chemical

        """
        struct_element_rels_after = StructElementRel.objects.all()
        SER_after = set(struct_element_rels_after)
        SER_delta = SER_after - self.struct_element_rels_before
        # length of elements_dict and number of new StructElementRel
        # must be equal
        self.assertEqual(len(self.elements_dict), len(SER_delta))
        # this cycle must reproduce elements dict from SER_delta
        elements_and_indices = dict()
        for item in SER_delta:
            elements_and_indices[item.element.symbol] = item.index
        self.assertEqual(elements_and_indices, self.elements_dict)
        # all new StructElementRel must have new chemical as 
        # subsrance field
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

    def test_chemicals_create3(self):
        chemicals_in_drawer_after = set(
            Chemical.objects.filter(storage_place=self.drawer)
        )
        chemicals_in_drawer_delta = (chemicals_in_drawer_after -
            self.chemicals_in_drawer_before
        )
        self.assertEqual(len(chemicals_in_drawer_delta), 1)
        new_chemical = chemicals_in_drawer_delta.pop()
        self.assertEqual(self.test_substance, new_chemical)
    
    def test_chemicals_create4(self):
        chemicals_with_q_in_grams_after = set(
            Chemical.objects.filter(quantity_unit=self.gram)
        )
        chemicals_with_q_in_grams_delta = (chemicals_with_q_in_grams_after -
            self.chemicals_with_q_in_grams_before
        )
        self.assertEqual(len(chemicals_with_q_in_grams_delta), 1)
        new_chemical = chemicals_with_q_in_grams_delta.pop()
        self.assertEqual(self.test_substance, new_chemical)

    def test_chemicals_create5(self):
        chemicals_by_vigri_after = set(
            Chemical.objects.filter(who_created=self.vigri)
        )
        chemicals_by_vigri_delta = (chemicals_by_vigri_after -
            self.chemicals_by_vigri_before
        )
        self.assertEqual(len(chemicals_by_vigri_delta), 1)
        new_chemical = chemicals_by_vigri_delta.pop()
        self.assertEqual(self.test_substance, new_chemical)

    def test_chemicals_create6(self):
        old_abundance_dict = dict(self.abundance_dict)
        self.make_abundance_dict()
        for key, old_value in old_abundance_dict.items():
            self.assertEqual(self.abundance_dict[key], old_value + 1)


class ChemicalDeleteTestCase(ChemicalTestCase):
    def setUp(self):
        super().setUp()
        self.ergosterol = Chemical.objects.get(name="Ergosterol")
        self.elements_dict = self.make_element_dict(
            self.ergosterol.mol_block
        )
        self.make_abundance_dict()
        self.n_of_SER_linked_to_ergosterol = len(
            StructElementRel.objects.filter(chemical=self.ergosterol)
        )
        self.chemicals_in_door_before = set(Chemical.objects.filter(
            storage_place=self.door
        ))
        self.ergosterol.delete()
        

    def test_chemicals_delete1(self):
        struct_element_rels_after = StructElementRel.objects.all()
        SER_after = set(struct_element_rels_after)
        SER_delta = self.struct_element_rels_before - SER_after
        self.assertEqual(self.n_of_SER_linked_to_ergosterol, len(SER_delta))

    def test_chemicals_delete2(self):
        all_chemicals_after = Chemical.objects.all()
        delta_of_len = (len(self.all_chemicals_before) - 
            len(all_chemicals_after)
        )
        self.assertEqual(1, delta_of_len)

    def test_chemicals_delete3(self):
        all_chemicals_by_Vigri_after = Chemical.objects.filter(
            who_created=self.vigri
        )
        delta_of_len = (len(self.chemicals_by_vigri_before) - 
            len(all_chemicals_by_Vigri_after)
        )
        self.assertEqual(delta_of_len, 1)

    def test_chemicals_delete4(self):
        chemicals_with_q_in_grams_after = Chemical.objects.filter(
            quantity_unit=self.gram
        )
        delta_of_len = (len(self.chemicals_with_q_in_grams_before) -
            len(chemicals_with_q_in_grams_after)
        )
        self.assertEqual(delta_of_len, 1)

    def test_chemicals_delete5(self):
        chemicals_in_door_after = Chemical.objects.filter(
            storage_place=self.door
        )
        delta_of_len = (len(self.chemicals_in_door_before) - 
            len(chemicals_in_door_after)
        )
        self.assertEqual(delta_of_len, 1)

    def test_chemicals_delete6(self):
        old_abundance_dict = dict(self.abundance_dict)
        self.make_abundance_dict()
        for key, old_value in old_abundance_dict.items():
            self.assertEqual(self.abundance_dict[key], old_value - 1)


class ChemicalUpdateTestCase(ChemicalTestCase):
    def setUp(self):
        super().setUp()
        self.chemicals_with_q_in_kg_before = set(Chemical.objects.filter(
            quantity_unit=self.kilogram
        ))
        self.chemicals_with_q_in_mg_before = set(Chemical.objects.filter(
            quantity_unit=self.milligram
        ))
        self.chemicals_by_krtek_before = set(Chemical.objects.filter(
            who_created=self.krtek
        ))
        self.chemicals_in_door_before = set(Chemical.objects.filter(
            storage_place=self.door
        ))
        # old substance
        self.old_substance = Chemical.objects.get(name="Iron (II) Sulfate")
        fe_elem = Element.get_by_symbol("Fe")
        s_elem = Element.get_by_symbol("S")
        o_elem = Element.get_by_symbol("O")
        c_elem = Element.get_by_symbol("C")
        si_elem = Element.get_by_symbol("Si")
        cl_elem = Element.get_by_symbol("Cl")
        elem_list = [fe_elem, s_elem, o_elem,
                     c_elem, si_elem, cl_elem]
        # сделать методы make_n_of_SER_dict и make_abundance_dict
        # которые будут принимать список элементов
        # и возвращать для этих элементов соответствующие словари
        self.n_of_SER_before = self.make_n_of_SER_dict(elem_list)
        self.abundance_before = self.make_abundance_dict(elem_list)
        self.create_properties_dict()
        self.old_substance.update(
            self.properties_dict,
            self.elements_dict
        )
    
    def make_n_of_SER_dict(self, elem_list):
        pass
    
    def make_abundance_dict(self, elem_list):
        pass

    def create_properties_dict(self):
        self.properties_dict = substances[-1]
        with open('base_app/tests/substances_for_test/' +
                  self.properties_dict["name"] +
                  '.mol', "rt", encoding="utf-8") as file:
            self.properties_dict["mol_block"] = file.read()
        self.properties_dict["storage_place"] = self.door
        self.properties_dict["quantity_unit"] = self.milligram
        self.properties_dict["quantity"] = 800.0
        self.properties_dict["who_created"] = self.vigri
        self.elements_dict = self.make_element_dict(
            self.properties_dict["mol_block"]
        )

    def test_chemicals_update1(self):
        n_of_chemicals_after = len(Chemical.objects.all())
        n_of_chemicals_before = len(self.all_chemicals_before)
        self.assertEqual(n_of_chemicals_before, n_of_chemicals_after)

    def test_chemicals_update2(self):
        pass
