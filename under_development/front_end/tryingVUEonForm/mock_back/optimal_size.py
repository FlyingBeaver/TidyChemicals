import math
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import MolToFile


def get_optimal_size(mol):
    x_list = []
    y_list = []
    bonds_lengthes = []
    AllChem.Compute2DCoords(mol)
    conformer = mol.GetConformer()
    for atom in mol.GetAtoms():
        index = atom.GetIdx()
        position = conformer.GetAtomPosition(index)
        x_list.append(position.x)
        y_list.append(position.y)
    for bond in mol.GetBonds():
        begin_index = bond.GetBeginAtomIdx()
        end_index = bond.GetEndAtomIdx()
        begin_atom_pos = conformer.GetAtomPosition(begin_index)
        end_atom_pos = conformer.GetAtomPosition(end_index)
        bond_length = math.sqrt(
            (begin_atom_pos.x - end_atom_pos.x) ** 2 + 
            (begin_atom_pos.y - end_atom_pos.y) ** 2
        )
        bonds_lengthes.append(bond_length)
    max_x = max(x_list)
    min_x = min(x_list)
    max_y = max(y_list)
    min_y = min(y_list)
    max_dimension = max((max_x - min_x), (max_y - min_y))
    average_bond_length = sum(bonds_lengthes) / len(bonds_lengthes)
    size = max_dimension * 60 / average_bond_length
    return round(size)
