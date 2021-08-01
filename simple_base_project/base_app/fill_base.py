# =============================================================================
# import os
# import pathlib
# =============================================================================
from rdkit.Chem.inchi import MolToInchi
from rdkit.Chem.Descriptors import ExactMolWt
from rdkit.Chem.rdMolDescriptors import CalcMolFormula
from rdkit.Chem.rdmolfiles import MolFromPDBBlock
from base_app import models


# =============================================================================
# FOLDER_PATH = pathlib.PureWindowsPath(("D:/playground/chem_sandbox/"
#                                        "simple_base/simple_base_project/"
#                                        "base_app/pdb_files"))
# =============================================================================

with open("base_app/all_merged.txt", "rt", encoding="utf-8") as long_file:
    content = long_file.read()


separator = "\n###separator###\n"
list_of_pdbs = content.strip(separator).split(separator)


n = 1
for i in list_of_pdbs:
    molecule = MolFromPDBBlock(i)
    its_name = f"unnamed molecule No {n}"
    its_inchi = MolToInchi(molecule)
    its_brutto = CalcMolFormula(molecule)
    its_molar_weight = ExactMolWt(molecule)
    models.Structure.objects.create(name=its_name,
                                    inchi=its_inchi,
                                    brutto=its_brutto,
                                    molar_mass=its_molar_weight)
    n += 1
    if n % 20 == 0:
        print('number', n)
