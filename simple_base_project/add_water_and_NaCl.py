# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 15:09:18 2021

@author: Александр
"""

from rdkit.Chem.inchi import MolFromInchi
from rdkit.Chem.Descriptors import ExactMolWt
from rdkit.Chem.rdMolDescriptors import CalcMolFormula
from base_app.models import Structure

water_inchi = "InChI=1S/H2O/h1H2"
water = MolFromInchi(water_inchi)
water_brutto = CalcMolFormula(water)
water_molar_mass = ExactMolWt(water)
Structure.objects.create(name="Water", 
                         inchi=water_inchi, 
                         brutto=water_brutto, 
                         molar_mass=water_molar_mass)


salt_inchi = "InChI=1S/ClH.Na/h1H;/q;+1/p-1"
salt = MolFromInchi(salt_inchi)
salt_brutto = CalcMolFormula(salt)
salt_molar_mass = ExactMolWt(salt)
Structure.objects.create(name="Sodium Chloride", 
                         inchi=salt_inchi, 
                         brutto=salt_brutto, 
                         molar_mass=salt_molar_mass)
