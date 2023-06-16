import networkx as nx
from collections import Counter
from pprint import pprint
from rdkit.Chem import MolFromSmiles, MolFromInchi
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
        canonic_string1 = make_canonic_string(atoms_bonds_list)
        ring_list.reverse()
        atoms_bonds_list = make_atoms_bonds_list(ring_list, molecule, ring=True)
        canonic_string2 = make_canonic_string(atoms_bonds_list)
        list_of_ringstrings.append(min(canonic_string1, canonic_string2))
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


class Node:
    def __init__(self, tag, self_id, parent=None, data=None):
        self.tag = tag
        self.self_id = self_id
        self.parent = parent
        self.children = dict()
        self.data = data


class Tree:
    def __init__(self):
        self.usual_nodes = dict()
        self.leaves_ = dict()
        self.root = None
        self.root_id = None

    def create_node(self, tag, node_id, parent=None, data=None):
        if parent is None and self.root:
            raise ValueError("Parent needed!")
        if node_id in self.leaves_ or node_id in self.usual_nodes:
            raise ValueError("Already have node with such id!")
        if (parent is not None and
            (parent not in self.leaves_ and
             parent not in self.usual_nodes)):
            raise ValueError(f"No such parent: {parent}")
        node = Node(tag, node_id, parent, data)
        if not self.root:
            self.root = node
            self.root_id = node_id
        self.leaves_[node_id] = node
        if parent in self.leaves_:
            parent_node = self.leaves_[parent]
            del self.leaves_[parent]
            self.usual_nodes[parent] = parent_node
        if parent is not None:
            parent_node = self.usual_nodes[parent]
            parent_node.children[node_id] = node

    def leaves(self):
        return list(self.leaves_.values())

    def delete_not_leaf_nodes(self):
        if self.root_id not in self.leaves_:
            self.root = None
            self.root_id = None
        for key in list(self.usual_nodes.keys()):
            del self.usual_nodes[key]


class FrozenDict(dict):
    def __init__(self, usual_dict: dict):
        if not isinstance(usual_dict, dict):
            raise TypeError("usual_dict must be dict")
        self.hash = hash(self.make_repr(usual_dict))
        super().__init__(usual_dict)

    def make_repr(self, instance):
        items_list = list(instance.items())
        return f"FrozenDict({repr(items_list)})"

    def __repr__(self):
        return self.make_repr(self)

    def __hash__(self):
        return self.hash


def find_all_rings(the_graph):
    all_derived_graphs = set()
    all_cycles = set()
    all_cycles_list = []
    tree = Tree()
    counter = count(0)
    first_node_id = next(counter)
    tree.create_node("1", first_node_id, data=the_graph)
    unfinished_leaves = tree.leaves()
    while unfinished_leaves:
        for leaf in unfinished_leaves:
            process_leaf(leaf,
                         tree,
                         counter,
                         all_cycles,
                         all_cycles_list,
                         all_derived_graphs)
        unfinished_leaves = list(filter(lambda x: x.tag == "1", tree.leaves()))
        tree.delete_not_leaf_nodes()
    return all_cycles_list


def get_graph_dict(graph):
    temp_dict = dict()
    for node1, node2 in graph.edges():
        if node1 in temp_dict:
            temp_dict[node1].add(node2)
        else:
            temp_dict[node1] = {node2}

        if node2 in temp_dict:
            temp_dict[node2].add(node1)
        else:
            temp_dict[node2] = {node1}
    return FrozenDict(temp_dict)


def process_leaf(leaf,
                 tree,
                 counter,
                 all_cycles,
                 all_cycles_list,
                 all_derived_graphs):
    graph = leaf.data
    graph_dict = get_graph_dict(graph)
    if graph_dict in all_derived_graphs:
        leaf.tag = "0"
    else:
        basic_cycles = nx.cycle_basis(graph)
        for cycle in basic_cycles:
            old_length = len(all_cycles)
            all_cycles.add(frozenset(cycle))
            if len(all_cycles) > old_length:
                all_cycles_list.append(cycle)
        neighbours = False
        for ring1, ring2 in combinations(basic_cycles, 2):
            common_edge = set_pairwise(ring1) & set_pairwise(ring2)
            if common_edge:
                pair = next(iter(common_edge))
                node1, node2 = pair
                neighbours = True
                new_graph = deepcopy(graph)
                new_graph.remove_edge(node1, node2)
                new_leaf = tree.create_node("1", next(counter),
                                            parent=leaf.self_id,
                                            data=new_graph)
        if not neighbours:
            leaf.tag = "0"
        all_derived_graphs.add(graph_dict)


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
    inchi1 = "InChI=1S/C57H39N5/c1-34-30-38(60-52-29-28-37(57-58-35(2)31-36(3)59-57)32-47(52)54-45-22-6-4-16-39(45)40-17-5-7-23-46(40)56(54)60)33-53(61-48-24-12-8-18-41(48)42-19-9-13-25-49(42)61)55(34)62-50-26-14-10-20-43(50)44-21-11-15-27-51(44)62/h4-33H,1-3H3"
    inchi2 = "InChI=1S/C52H42/c1-49(2,32-25-27-36-34-17-7-10-21-40(34)50(3,4)44(36)29-32)33-26-28-37-35-18-8-11-22-41(35)52(45(37)30-33)42-23-12-9-19-38(42)47-48(52)39-20-13-15-31-16-14-24-43(46(31)39)51(47,5)6/h7-30H,1-6H3/t52-/m1/s1"

    chol_smiles = ("C[C@H](CCCC(C)C)[C@H]1CC[C@@H]2[C@@]1(CC"
                   "[C@H]3[C@H]2CC=C4[C@@]3(CC[C@@H](C4)O)C)C")
    chol = MolFromSmiles(chol_smiles)
    print("Cholesterol linear and ring fragments:")
    pprint(make_fragments(chol))

    stucture1 = MolFromInchi(inchi1)
    pprint(make_fragments(stucture1))

    stucture2 = MolFromInchi(inchi2)
    pprint(make_fragments(stucture2))


if __name__ == '__main__':
    main()
