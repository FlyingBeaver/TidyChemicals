from copy import copy, deepcopy
from collections import Counter
from itertools import combinations
from pprint import pprint
from rdkit.Chem import MolFromSmiles
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdchem import Atom
from making_trees import AtomTree, BOND_SYMBOLS


def make_path_dicts(molecule: Mol):
    number_of_atoms = molecule.GetNumAtoms()
    for i, j in combinations(range(number_of_atoms), 2):
        tree1 = AtomTree(i, molecule)
        tree2 = AtomTree(j, molecule)
        tree_handler1 = TreeHandler(tree1)
        tree_handler1.make_level_sets()
        tree_handler2 = TreeHandler(tree2)


class TreeHandler:
    def __init__(self, tree: AtomTree):
        self.tree = tree
        self.paths_to_leaves = tree.paths_to_leaves()
        self.max_length = max(map(len, self.paths_to_leaves))
        self.rectangular_paths_list = []
        self.transposed_paths = []
        self.level_sets = []
        self.make_level_sets()

    def make_level_sets(self):
        """Fills rect.paths_list, transposed_paths, level_sets fields

        It saves 2d array of atom_id's made by Tree's method
        'paths_to_leaves'. Then transforms it into rectangular
        matrix, adding None's to make lists of equal lengthes.
        Then transposes it and transforms every column to set,
        removes None's from sets (self.level_sets)

        Does not return anything
        """
        self.rectangular_paths_list = []
        for i in range(len(self.paths_to_leaves)):
            delta = self.max_length - len(self.paths_to_leaves[i])
            list_to_add = copy(self.paths_to_leaves[i])
            list_to_add.extend([None] * delta)
            self.rectangular_paths_list.append(list_to_add)
        self.transposed_paths = list(zip(*self.rectangular_paths_list))
        self.level_sets = list(map(lambda x: set(x).difference({None}),
                                   list(self.transposed_paths)))

    def find_common_nodes(self, other):
        """
        There are two possible intersection patterns:
        [a, b, c, X, Y] [d, e, f, Y, X] and
        [a, b, c, X] [d, e, f, X]
        Code here finds approximate index of intersection
        level and...
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Argument must be TreeHandler")
        length = min(self.max_length, other.max_length)
        intersection_position = None
        for i in range(length - 1):
            true_if_even_intersection = \
                (self.level_sets[i] & other.level_sets[i + 1]
                ) and (
                other.level_sets[i] & self.level_sets[i + 1])
            true_if_odd_intersection = \
                (self.level_sets[i + 1] & other.level_sets[i + 1])
            if true_if_odd_intersection:
                return self.process_odd_intersection(other, i + 1)
            elif true_if_even_intersection:
                return self.process_even_intersection(other, i)
        else:
            raise RuntimeError("intersection not found2")

    def process_even_intersection(self, other, intersection_position):
        """Будет возвращать список тьюплов"""
        intersection_near = (self.level_sets[intersection_position] &
                        other.level_sets[intersection_position + 1])
        intersection_far = (self.level_sets[intersection_position + 1] &
                        other.level_sets[intersection_position])
        result = []
        # для каждого члена множества интерсекшн нужно найти его вхождения 
        # в self.transposed_paths[intersection_position]
        #    для каждого вхождения нужно найти 
        #    self.transposed_paths[intersection_position + 1][index]
        #        и если он входит в intersection_far
        for i in intersection_near:
            for j in self.appearance_indices(self.transposed_paths[intersection_position], i):
                if self.transposed_paths[intersection_position + 1][j] in intersection_far:
                    result.append((self.transposed_paths[intersection_position][j],
                                   self.transposed_paths[intersection_position + 1][j])
                    )
        return result, intersection_position

    def process_odd_intersection(self, other, intersection_position):
        """Будет возвращать список целых чисел"""
        return list(self.level_sets[intersection_position] &
                    other.level_sets[intersection_position]), intersection_position

    def make_pathlist_to_leaf_int(self, node_id: int, position: int):
        list_number = self.transposed_paths[position].index(node_id)
        id_list_long = self.rectangular_paths_list[list_number]
        id_list = id_list_long[: position + 1]
        return id_list

    def make_pathlist_to_leaf_tuple(self, node_id: tuple, position: int):
        """
        This method takes 'node_id', tuple of two atom ids,
        that must be in a matrix, (stored in self.rectangular_paths_list)
        together in a column with index of 'position' (2nd method arg).
        It must return a fragment of a row from the matrix with
        atom ids  that starts with 0 position up to both node_ids.
        """
        atom_id1, atom_id2 = node_id
        if (atom_id1 in self.transposed_paths[position] and
                atom_id2 in self.transposed_paths[position + 1]):
            pass
        elif (atom_id2 in self.transposed_paths[position] and
                atom_id1 in self.transposed_paths[position + 1]):
            atom_id1, atom_id2 = atom_id2, atom_id1
        else:
            raise ValueError("At least one atom_id isn't in a column")
        column1 = self.transposed_paths[position]
        column2 = self.transposed_paths[position + 1]
        column_of_pairs = list(zip(column1, column2))
        row_no = column_of_pairs.index((atom_id1, atom_id2))
        
        atom_id_row = self.rectangular_paths_list[row_no]
        truncated_atom_id_row = atom_id_row[:position + 2]
        return truncated_atom_id_row
    
    @staticmethod
    def unite_pathlists(path1: list, path2: list):
        if path1[-1] == path2[-1]:
            return path1 + list(reversed(path2[: -1]))
        elif path1[-2:] == list(reversed(path2[-2:])):
            return path1 + list(reversed(path2[: -2]))
        else:
            raise ValueError(f"Pathlists {path1} and"
                             f" {path2} can't be united")
    
    @staticmethod
    def appearance_indices(the_list, element):
        result = []
        index = 0
        while True:
            try:
                index = the_list.index(element, index)
            except ValueError:
                return result
            result.append(index)
            index += 1

    def make_raw_pathstring(self, pathlist: list):
        result = ''
        for index, node_id in enumerate(pathlist):
            node_itself = self.tree.get_node(node_id)
            if node_itself:
                result += node_itself.data.elem_symbol
            else:
                result += self.tree.molecule.GetAtomWithIdx(node_id).GetSymbol()
            if index < len(pathlist) - 1:
                bond_object = self.tree.molecule.GetBondBetweenAtoms(
                    node_id, pathlist[index + 1]
                    )
                bond_type = bond_object.GetBondType()
                bond_symbol = BOND_SYMBOLS[str(bond_type)]
                if bond_symbol != "-":
                    result += bond_symbol
        return result

    def make_pathstring(self, pathlist):
        # Works correctly only with pathlists made by 
        # unite_pathlists from halves made 
        # by make_pathlist_to_leaf_int or make_pathlist_to_leaf_tuple
        symmetrical = False
        reversed_pathlist = list(reversed(pathlist))
        if pathlist == reversed_pathlist:
            symmetrical = True

        if symmetrical:
            return self.make_raw_pathstring(pathlist)
        else:
            return min(self.make_raw_pathstring(pathlist),
                       self.make_raw_pathstring(reversed_pathlist))


def shortest_paths(struct: str = '',
                   idx1: (int, None) = None,
                   idx2: (int, None) = None):
    molecule = MolFromSmiles(struct)
    atom1 = molecule.GetAtomWithIdx(idx1)
    atom2 = molecule.GetAtomWithIdx(idx2)
    tree1 = AtomTree(molecule)
    tree2 = deepcopy(tree1)
    tree1.create_atom_node(atom1)
    tree2.create_atom_node(atom2)
    tree1.grow()
    tree2.grow()
    # tree1.show(idhidden=False)
    # tree2.show(idhidden=False)
    handler1 = TreeHandler(tree1)
    handler2 = TreeHandler(tree2)
    common_nodes, position = handler1.find_common_nodes(handler2)
    list_of_results = []
    if isinstance(common_nodes[0], int):
        for i in common_nodes:
            half_path1 = handler1.make_pathlist_to_leaf_int(i, position)
            half_path2 = handler2.make_pathlist_to_leaf_int(i, position)
            united_pathlist = TreeHandler.unite_pathlists(half_path1, half_path2)
            list_of_results.append(united_pathlist)
    elif isinstance(common_nodes[0], tuple):
        for i in common_nodes:
            half_path1 = handler1.make_pathlist_to_leaf_tuple(i, position)
            half_path2 = handler2.make_pathlist_to_leaf_tuple(i, position)
            united_pathlist = TreeHandler.unite_pathlists(half_path1, half_path2)
            list_of_results.append(united_pathlist)
    return list_of_results


def main():
    tbf_sm = "O=P(OCCCC)(OCCCC)OCCCC"
    tbf = MolFromSmiles(tbf_sm)
    for i in range(tbf.GetNumAtoms()):
        c_terminal = tbf.GetAtomWithIdx(i)
        if c_terminal.GetSymbol() == 'c':
            if list(map(lambda x: x.GetSymbol(), 
                        c_terminal.GetNeighbors())
                    ) == ['c']:
                break
    for i in range(tbf.GetNumAtoms()):
        o_terminal = tbf.GetAtomWithIdx(i)
        print(f"o_terminal.GetBonds()[0].GetBondType():"
              f"\n{o_terminal.GetBonds()[0].GetBondType()}")
        print(f"o_terminal.GetSymbol():\n{o_terminal.GetSymbol()}")
        if (o_terminal.GetSymbol() == 'O' and
            str(o_terminal.GetBonds()[0].GetBondType()) == "DOUBLE"
            ):
            break
    else:
        raise RuntimeError("can't find right atom")

    tree_tbf1 = AtomTree(tbf)
    tree_tbf1.create_node(c_terminal)
    tree_tbf1.grow()
    tree_handler1 = TreeHandler(tree_tbf1)

    tree_tbf2 = AtomTree(tbf)
    tree_tbf2.create_node(o_terminal)
    tree_tbf2.grow()
    tree_handler2 = TreeHandler(tree_tbf2)

    result, pos = tree_handler1.find_common_nodes(tree_handler2)
    print("rezult")
    print(result)
    common_node = result.pop()
    print("common_node")
    print(common_node)
    print(tree_handler1.make_pathlist_to_leaf_tuple(common_node, pos))


def not_main():
    chol_smiles = ("C[C@H](CCCC(C)C)[C@H]1CC[C@@H]2[C@@]1(CC"
                   "[C@H]3[C@H]2CC=C4[C@@]3(CC[C@@H](C4)O)C)C")
    print(shortest_paths(chol_smiles, 23, 12))


if __name__ == '__main__':
    not_main()
    # main()
    