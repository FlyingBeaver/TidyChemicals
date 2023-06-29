import networkx as nx
from collections import Counter
from pprint import pprint
from rdkit.Chem import MolFromSmiles
from itertools import tee, permutations, combinations, count
from treelib import Tree
from copy import deepcopy


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


def set_pairwise(list_):
    a, b = tee(list_)
    next(b, None)
    result = set()
    for pair in zip(a, b):
        result.add(frozenset(pair))
    result.add(frozenset((list_[0], list_[-1])))
    return result


def make_fragments(molecule,
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
            atoms_bonds_list = make_atoms_bonds_list(path_list, molecule, ring=False)
            straight_pathstring = ''.join(atoms_bonds_list)
            atoms_bonds_list.reverse()
            reversed_pathstring = ''.join(atoms_bonds_list)
            list_of_pathstrings.append(min(straight_pathstring,
                                           reversed_pathstring))
    linear_fragments = dict(Counter(list_of_pathstrings))

    list_of_ringstrings = []
    all_ring_lists = find_all_rings(the_graph)
    for ring_list in all_ring_lists:
        atoms_bonds_list = make_atoms_bonds_list(ring_list, molecule, ring=True)
        canonic_string = make_canonic_string(atoms_bonds_list)
        list_of_ringstrings.append(canonic_string)
    ring_fragments = dict(Counter(list_of_ringstrings))
    return linear_fragments, ring_fragments


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


def find_all_rings(the_graph):
    all_cycles = set()
    all_cycles_list = []
    tree = Tree()
    counter = count(0)
    first_node_id = next(counter)
    tree.create_node("1", first_node_id, data=the_graph)
    unfinished_leaves = tree.leaves()
    while unfinished_leaves:
        for leaf in unfinished_leaves:
            process_leaf(leaf, tree, counter, all_cycles, all_cycles_list)
        unfinished_leaves = list(filter(lambda x: x.tag == "1", tree.leaves()))
    return all_cycles_list


def process_leaf(leaf, tree, counter, all_cycles, all_cycles_list):
    graph = leaf.data
    basic_cycles = nx.cycle_basis(graph)
    for cycle in basic_cycles:
        old_length = len(all_cycles)
        all_cycles.add(frozenset(cycle))
        if len(all_cycles) > old_length:
            all_cycles_list.append(cycle)
    neighbours = False
    for x, y in combinations(basic_cycles, 2):
        common_edge = set_pairwise(x) & set_pairwise(y)
        if common_edge:
            pair = next(iter(common_edge))
            node1, node2 = pair
            neighbours = True
            new_graph = deepcopy(graph)
            new_graph.remove_edge(node1, node2)
            new_leaf = tree.create_node("1", next(counter), parent=leaf, data=new_graph)
    if not neighbours:
        leaf.tag = "0"


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
    else:
        atoms_bonds_list.append(
            molecule.GetAtomWithIdx(path_list[-1]).GetSymbol()
        )
    if ring:
        bond_type = molecule.GetBondBetweenAtoms(
            path_list[0], path_list[-1]
        ).GetBondType()
        atoms_bonds_list.append(BOND_SYMBOLS[str(bond_type)])
    return atoms_bonds_list


def is_substructure(substructure, superstructure):
    sub_paths = make_linear_fragments(substructure)
    super_paths = make_linear_fragments(superstructure)
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
    print("Cholesterol linear and ring fragments:")
    pprint(make_fragments(chol))


if __name__ == '__main__':
    main()
