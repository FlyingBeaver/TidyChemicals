import re
from django.db import models
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdMolDescriptors import CalcMolFormula


class Structure(models.Model):
    name = models.CharField(max_length=128)
    inchi = models.CharField(max_length=1024)
    brutto = models.CharField(max_length=256)
    molar_mass = models.FloatField()
    
    @classmethod
    def create(cls, molecule: Mol):
        """
        Создаёт новую структуру в таблице
        """
        mol_formula = CalcMolFormula()
        


class Elements(models.Model):
    z = models.IntegerField(primary_key=True)
    symbol = models.CharField(max_length=3)
    atomic_weight = models.FloatField()
    containing_structures = models.ManyToManyField(Structure, 
                                                   on_delete=models.PROTECT)
