from itertools import tee, combinations
from collections import Counter
from pprint import pprint

import networkx as nx
from rdkit.Chem import MolFromSmiles

from chemicals.services.find_all_cycles import find_all_cycles


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


def make_fragments(molecule,
                   length_restriction: (int, None.__class__) = 7):
    the_graph = nx.Graph()
    list_of_atoms = []

    for atom in molecule.GetAtoms():
        the_graph.add_node(atom.GetIdx())
        list_of_atoms.append(atom.GetIdx())

    for bond in molecule.GetBonds():
        the_graph.add_edge(bond.GetBeginAtomIdx(),
                           bond.GetEndAtomIdx())
    return (make_paths(molecule,
                       the_graph,
                       list_of_atoms,
                       length_restriction),
            make_rings(molecule, the_graph))


def make_paths(molecule, the_graph, list_of_atoms, length_restriction):
    list_of_pathstrings = []
    for atom_index1, atom_index2 in combinations(list_of_atoms, 2):
        try:
            paths_generator = nx.all_shortest_paths(the_graph,
                                                    atom_index1,
                                                    atom_index2)
            paths = list(paths_generator)
        except nx.NetworkXNoPath:
            paths = []
        for path_list in paths:
            if (length_restriction and len(path_list) >
                    length_restriction):
                continue
            atoms_bonds_list = make_atoms_bonds_list(path_list,
                                                     molecule,
                                                     ring=False)
            straight_pathstring = ''.join(atoms_bonds_list)
            atoms_bonds_list.reverse()
            reversed_pathstring = ''.join(atoms_bonds_list)
            list_of_pathstrings.append(min(straight_pathstring,
                                           reversed_pathstring))
    return dict(Counter(list_of_pathstrings))


def make_rings(molecule, the_graph):
    list_of_ringstrings = []
    all_ring_lists = find_all_cycles(the_graph)
    for ring_list in all_ring_lists:
        atoms_bonds_list = make_atoms_bonds_list(ring_list,
                                                 molecule,
                                                 ring=True)
        canonic_string1 = make_canonic_string(atoms_bonds_list)
        ring_list.reverse()
        atoms_bonds_list = make_atoms_bonds_list(ring_list,
                                                 molecule,
                                                 ring=True)
        canonic_string2 = make_canonic_string(atoms_bonds_list)
        list_of_ringstrings.append(min(canonic_string1, canonic_string2))
    return dict(Counter(list_of_ringstrings))


def make_canonic_string(atoms_bonds_list):
    if len(atoms_bonds_list) % 2 == 1:
        raise ValueError("Odd number of elements in atoms_bonds_list")
    halflength = len(atoms_bonds_list) // 2
    candidates_lists = [atoms_bonds_list]
    for i in range(1, halflength):
        candidates_lists.append(
            atoms_bonds_list[-2 * i:] + atoms_bonds_list[:-2 * i]
        )
    candidates_strings = []
    for list_ in candidates_lists:
        candidates_strings.append("".join(list_))
    return min(candidates_strings)


def make_atoms_bonds_list(path_list, molecule, ring):
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
    atoms_bonds_list.append(
        molecule.GetAtomWithIdx(path_list[-1]).GetSymbol()
    )
    if ring:
        bond_type = molecule.GetBondBetweenAtoms(
            path_list[0], path_list[-1]
        ).GetBondType()
        atoms_bonds_list.append(BOND_SYMBOLS[str(bond_type)])
    return atoms_bonds_list


def main():
    chol_smiles = ("C[C@H](CCCC(C)C)[C@H]1CC[C@@H]2[C@@]1(CC"
                   "[C@H]3[C@H]2CC=C4[C@@]3(CC[C@@H](C4)O)C)C")
    chol = MolFromSmiles(chol_smiles)
    print("Cholesterol linear and ring fragments:")
    pprint(make_fragments(chol))


if __name__ == '__main__':
    main()
