from mol_classes import LazyMol
import unittest
import re
import substances_for_test as sub
from pprint import pprint


ofile = open("file.txt", 'wt', encoding='utf-8')

def brutto_list(brutto1):
    charge = ''
    list1 = []
    if "+" in brutto1 or "-" in brutto1:
        charge += brutto1[-2:]
        list1 += charge
    list1 += re.findall(r"[A-Z][a-z]*\d*", brutto1)
    return set(list1)


def compare_lists(list1, list2):
    list1.sort()
    list2.sort()
    return list1 == list2


def compare_mw(mw1, mw2):
    return (mw1 - mw2) / mw1 < 1/100


class TestLazyMol(unittest.TestCase):
    def setUp(self):
        self.water = LazyMol(sub.water['smiles'])
        self.nacl = LazyMol(sub.nacl['smiles'])
        self.iproh = LazyMol(sub.iproh['smiles'])
        self.stigm = LazyMol(sub.stigm['smiles'])
        self.tio2 = LazyMol(sub.tio2['smiles'])
        self.cuso4aq = LazyMol(sub.cuso4aq['smiles'])
        self.ti_ipro4 = LazyMol(sub.ti_ipro4['smiles'])
        self.so4 = LazyMol(sub.so4['smiles'])

    def test_inchi(self):
        self.assertEqual(self.water.inchi, sub.water['inchi'])
        self.assertEqual(self.nacl.inchi, sub.nacl['inchi'])
        self.assertEqual(self.iproh.inchi, sub.iproh['inchi'])
        self.assertEqual(self.stigm.inchi, sub.stigm['inchi'])
        self.assertEqual(self.tio2.inchi, sub.tio2['inchi'])
        self.assertEqual(self.cuso4aq.inchi, sub.cuso4aq['inchi'])
        self.assertEqual(self.ti_ipro4.inchi, sub.ti_ipro4['inchi'])
        self.assertEqual(self.so4.inchi, sub.so4['inchi'])

    def test_charge(self):
        self.assertEqual(self.water.charge, sub.water['charge'])
        self.assertEqual(self.nacl.charge, sub.nacl['charge'])
        self.assertEqual(self.iproh.charge, sub.iproh['charge'])
        self.assertEqual(self.stigm.charge, sub.stigm['charge'])
        self.assertEqual(self.tio2.charge, sub.tio2['charge'])
        self.assertEqual(self.cuso4aq.charge, sub.cuso4aq['charge'])
        self.assertEqual(self.ti_ipro4.charge, sub.ti_ipro4['charge'])
        self.assertEqual(self.so4.charge, sub.so4['charge'])
        self.assertEqual(self.water.charge, sub.water['charge'])


    def test_elements_list(self):
        self.assertEqual(sorted(self.water.elements_list), sorted(sub.water['elements_list']))
        self.assertEqual(sorted(self.nacl.elements_list), sorted(sub.nacl['elements_list']))
        self.assertEqual(sorted(self.iproh.elements_list), sorted(sub.iproh['elements_list']))
        self.assertEqual(sorted(self.stigm.elements_list), sorted(sub.stigm['elements_list']))
        self.assertEqual(sorted(self.tio2.elements_list), sorted(sub.tio2['elements_list']))
        self.assertEqual(sorted(self.cuso4aq.elements_list), sorted(sub.cuso4aq['elements_list']))
        self.assertEqual(sorted(self.ti_ipro4.elements_list), sorted(sub.ti_ipro4['elements_list']))
        self.assertEqual(sorted(self.so4.elements_list), sorted(sub.so4['elements_list']))

    def test_elements_dict(self):
        self.assertEqual(self.water.elements_dict, sub.water['elements_dict'])
        self.assertEqual(self.nacl.elements_dict, sub.nacl['elements_dict'])
        self.assertEqual(self.iproh.elements_dict, sub.iproh['elements_dict'])
        self.assertEqual(self.stigm.elements_dict, sub.stigm['elements_dict'])
        self.assertEqual(self.tio2.elements_dict, sub.tio2['elements_dict'])
        self.assertEqual(self.cuso4aq.elements_dict, sub.cuso4aq['elements_dict'])
        self.assertEqual(self.ti_ipro4.elements_dict, sub.ti_ipro4['elements_dict'])
        self.assertEqual(self.so4.elements_dict, sub.so4['elements_dict'])

    def test_inchikey(self):
        self.assertEqual(self.water.inchikey, sub.water['inchikey'])
        self.assertEqual(self.nacl.inchikey, sub.nacl['inchikey'])
        self.assertEqual(self.iproh.inchikey, sub.iproh['inchikey'])
        self.assertEqual(self.stigm.inchikey, sub.stigm['inchikey'])
        self.assertEqual(self.tio2.inchikey, sub.tio2['inchikey'])
        self.assertEqual(self.cuso4aq.inchikey, sub.cuso4aq['inchikey'])
        self.assertEqual(self.ti_ipro4.inchikey, sub.ti_ipro4['inchikey'])
        self.assertEqual(self.so4.inchikey, sub.so4['inchikey'])

    def test_molecular_formula(self):
        self.assertEqual(brutto_list(self.water.molecular_formula), brutto_list(sub.water['molecular_formula']))
        self.assertEqual(brutto_list(self.nacl.molecular_formula), brutto_list(sub.nacl['molecular_formula']))
        self.assertEqual(brutto_list(self.iproh.molecular_formula), brutto_list(sub.iproh['molecular_formula']))
        self.assertEqual(brutto_list(self.stigm.molecular_formula), brutto_list(sub.stigm['molecular_formula']))
        self.assertEqual(brutto_list(self.tio2.molecular_formula), brutto_list(sub.tio2['molecular_formula']))
        self.assertEqual(brutto_list(self.cuso4aq.molecular_formula), brutto_list(sub.cuso4aq['molecular_formula']))
        self.assertEqual(brutto_list(self.ti_ipro4.molecular_formula), brutto_list(sub.ti_ipro4['molecular_formula']))
        self.assertEqual(brutto_list(self.so4.molecular_formula), brutto_list(sub.so4['molecular_formula']))

    def test_molar_weight(self):
        self.assertEqual(self.water.molar_weight, sub.water["molar_weight"])
        self.assertEqual(self.nacl.molar_weight, sub.nacl["molar_weight"])
        self.assertEqual(self.iproh.molar_weight, sub.iproh["molar_weight"])
        self.assertEqual(self.stigm.molar_weight, sub.stigm["molar_weight"])
        self.assertEqual(self.tio2.molar_weight, sub.tio2["molar_weight"])
        self.assertEqual(self.cuso4aq.molar_weight, sub.cuso4aq["molar_weight"])
        self.assertEqual(self.ti_ipro4.molar_weight, sub.ti_ipro4["molar_weight"])
        self.assertEqual(self.so4.molar_weight, sub.so4["molar_weight"])


if __name__ == "__main__":
    unittest.main()
