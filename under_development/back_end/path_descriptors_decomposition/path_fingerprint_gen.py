import networkx as nx
from collections import Counter
from pprint import pprint
from rdkit.Chem import MolFromSmiles
from itertools import tee, permutations, combinations


BOND_SYMBOLS = {"SINGLE": "-",
                "DOUBLE": "=",
                "TRIPLE": "#",
                "AROMATIC": ":",
                "QUADRUPLE": "$"}


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def make_path_f5print(molecule,
                      length_restriction: (int, None.__class__) = 7):
    the_graph = nx.Graph()
    list_of_atoms = []
    list_of_pathstrings = []

    for atom in molecule.GetAtoms():
        the_graph.add_node(atom.GetIdx())
        list_of_atoms.append(atom.GetIdx())

    for bond in molecule.GetBonds():
        the_graph.add_edge(bond.GetBeginAtomIdx(),
                           bond.GetEndAtomIdx())

    for atom_index1, atom_index2 in combinations(list_of_atoms, 2):
        for path_list in nx.all_shortest_paths(the_graph,
                                               atom_index1,
                                               atom_index2):
            if (length_restriction and len(path_list) >
                    length_restriction):
                continue
            atoms_bonds_list = []
            for atom_id1, atom_id2 in pairwise(path_list):
                atoms_bonds_list.append(
                    molecule.GetAtomWithIdx(atom_id1).GetSymbol()
                )
                bond_type = molecule.GetBondBetweenAtoms(
                    atom_id1, atom_id2
                ).GetBondType()
                bond_symbol = BOND_SYMBOLS[str(bond_type)]
                atoms_bonds_list.append(bond_symbol)
            else:
                atoms_bonds_list.append(
                    molecule.GetAtomWithIdx(path_list[-1]).GetSymbol()
                )
            straight_pathstring = ''.join(atoms_bonds_list)
            atoms_bonds_list.reverse()
            reversed_pathstring = ''.join(atoms_bonds_list)
            list_of_pathstrings.append(min(straight_pathstring,
                                           reversed_pathstring))

    return dict(Counter(list_of_pathstrings))


def is_substructure(substructure, superstructure):
    sub_paths = make_path_f5print(substructure)
    super_paths = make_path_f5print(superstructure)
    sub_paths_set = set(sub_paths)

    if sub_paths_set <= set(super_paths):
        return all([sub_paths[key] <= super_paths[key] for key \
                    in sub_paths_set])
    else:
        return False


def compare(sub_smiles, super_smiles):
    sub = MolFromSmiles(sub_smiles)
    super_ = MolFromSmiles(super_smiles)
    print(is_substructure(sub, super_))


def main():
    chol_smiles = ("C[C@H](CCCC(C)C)[C@H]1CC[C@@H]2[C@@]1(CC"
                   "[C@H]3[C@H]2CC=C4[C@@]3(CC[C@@H](C4)O)C)C")
    chol = MolFromSmiles(chol_smiles)
    isopropyl_cyclopentane_smiles = "CC(C)C1CCCC1"
    tretbutyl_cyclopentane_smiles = "CC(C)(C)C1CCCC1"
    isopropyl_cyclopentane = MolFromSmiles(
        isopropyl_cyclopentane_smiles
    )
    tretbutyl_cyclopentane = MolFromSmiles(
        tretbutyl_cyclopentane_smiles
    )
    print(is_substructure(isopropyl_cyclopentane, chol))
    print(is_substructure(tretbutyl_cyclopentane, chol))
    print()
    print("Toluene")
    print("must be True")
    compare('Cc1ccccc1', 'Cc1ccc(C)cc1')
    compare('Cc1ccccc1', 'Cc1cccc(C)c1')
    compare('Cc1ccccc1', 'Cc1ccccc1C')
    compare('Cc1ccccc1', 'Cc1cc(O)cc(O)c1')
    compare('Cc1ccccc1', 'C#Cc1ccccc1')
    compare('Cc1ccccc1', 'O=C(O)c1ccccc1')
    compare('Cc1ccccc1', 'c1cc(ccc1)c1ccccc1')
    compare('Cc1ccccc1', 'C#CC1CCC2C3C=Cc4ccccc4C3CC[C@]12C')
    print()
    print('Glycole')
    print("must be True")
    compare("CC(O)C(C)O", 'OC1CCCC1O')
    compare("CC(O)C(C)O", 'O=C(O)C(O)C(C)(C)O')
    compare("CC(O)C(C)O", 'OC1CCCCC1O')
    compare("CC(O)C(C)O", 'O=P(O)(O)OCC(O)C(O)C(O)C(O)C(=O)O')
    compare("CC(O)C(C)O", 'OC1CC=C(Oc2ccccc2)CC1O')
    print()
    print("Both, Toluene")
    print("must be True")
    compare('Cc1ccccc1', 'Cc1ccc(C)cc1')
    compare('Cc1ccccc1', 'OC1c2ccccc2CCC1O')
    compare('Cc1ccccc1', 'OC(C(C)O)c1ccccc1')
    compare('Cc1ccccc1', 'Cc1ccc2OC3CCCCC3Oc2c1')
    compare('Cc1ccccc1', 'Oc1ccc(C#N)cc1O')
    print()
    print("Both, Glycole")
    print("must be True")
    compare('CC(O)C(C)O', 'OC1c2ccccc2CCC1O')
    compare('CC(O)C(C)O', 'OC(C(C)O)c1ccccc1')
    compare('CC(O)C(C)O', 'Cc1ccc2OC3CCCCC3Oc2c1')
    print()
    print()
    print("must be False")
    compare('Cc1ccccc1', 'O=CC(N)CCC(N)=O')
    compare('Cc1ccccc1', 'CC(N)C=O')
    compare('Cc1ccccc1', 'C1CCC(C1)C1CCCC1')
    compare('Cc1ccccc1', 'C1CCCC1')
    compare('Cc1ccccc1', 'C1CCCCC1')
    compare('Cc1ccccc1', 'O=C1CCCCC1O')
    compare('Cc1ccccc1', 'O=CC(N)O')
    compare('Cc1ccccc1', 'CC(O)CO')
    compare('CC(O)C(C)O', 'O=CC(N)CCC(N)=O')
    compare('CC(O)C(C)O', 'CC(N)C=O')
    compare('CC(O)C(C)O', 'C1CCC(C1)C1CCCC1')
    compare('CC(O)C(C)O', 'C1CCCC1')
    compare('CC(O)C(C)O', 'C1CCCCC1')
    compare('CC(O)C(C)O', 'O=C1CCCCC1O')
    compare('CC(O)C(C)O', 'O=CC(N)O')
    compare('CC(O)C(C)O', 'CC(O)CO')

if __name__ == '__main__':
    main()
