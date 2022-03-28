from copy import copy, deepcopy
from collections import Counter
from itertools import combinations
from rdkit.Chem import MolFromSmiles
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdchem import Atom
from making_trees import AtomTree


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
        """
        It saves 2d array of atom_id's made by Tree's method
        'paths_to_leaves'. Then transforms it into rectangular
        matrix, adding None's to make lists of equal lengthes.
        Then transposes it and transforms every column to set,
        removes None's from sets (self.level_sets)
        """
        self.rectangular_paths_list = []
        for i in range(len(self.paths_to_leaves)):
            delta = len(self.paths_to_leaves[i]) - self.max_length
            list_to_add = copy(self.paths_to_leaves[i])
            list_to_add.extend([None] * delta)
            self.rectangular_paths_list.append(list_to_add)
        self.transposed_paths = list(zip(*self.rectangular_paths_list))
        self.level_sets = list(map(lambda x: set(x).difference({None}),
                                   list(self.transposed_paths)))

    def find_common_nodes(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Argument must be TreeHandler")
        length = min(self.max_length, other.max_length)
        intersection_position = None
        for i in range(1, length):
            intersection_set = (
                                (self.level_sets[i] | self.level_sets[i + 1]) &
                                (other.level_sets[i] | other.level_sets[i + 1])
                                )
            if intersection_set:
                # то нужно провести сравнение отдельными множествами
                intersection_position = i
                return self.specify_found(intersection_position, other)

    def specify_found(self,
                      intersection_position: int,
                      other):
        second_position = intersection_position + 1
        possible_result = (self.level_sets[second_position] &
                           other.level_sets[second_position])
        if possible_result:
            return possible_result, intersection_position
        else:
            list_of_pairs1 = list(
                zip(self.transposed_paths[intersection_position],
                    self.transposed_paths[second_position])
            )
            list_of_pairs2_raw = list(
                zip(other.transposed_paths[intersection_position],
                    other.transposed_paths[second_position])
            )
            list_of_pairs2 = list(map(lambda x: (x[1], x[0]),
                                      list_of_pairs2_raw))
            common_pairs = set(list_of_pairs1) & set(list_of_pairs2)
            if common_pairs:
                return set(common_pairs.pop()), intersection_position
            else:
                raise ValueError("??????????")

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
        row_no = self.transposed_paths[position].index(atom_id1)
        row_no2 = self.transposed_paths[position + 1].index(atom_id2)
        if row_no != row_no2:
            raise ValueError("There are different row numbers")
        atom_id_row = self.rectangular_paths_list[row_no]
        truncated_atom_id_row = atom_id_row[:max(atom_id1, atom_id2) + 1]
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

    def make_raw_pathstring(self, pathlist: list):
        result = ''
        for index, node_id in enumerate(pathlist):
            result += self.tree.get_node(node_id).data.elem_symbol
            if index < len(pathlist) - 1:
                bond_symbol = self.tree.get_node(pathlist[index + 1]
                                                 ).data.bond_to_parent
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
    tree1.create_node(atom1)
    tree2.create_node(atom2)
    tree1.grow()
    tree2.grow()
    handler1 = TreeHandler(tree1)
    handler2 = TreeHandler(tree2)
    common_nodes, position = handler1.find_common_nodes(handler2)
    p = None
    if isinstance(common_nodes, list):
        for i in common_nodes:
            p = handler1.make_pathlist_to_leaf_int(i)
    elif isinstance(common_nodes, tuple):
        for i in common_nodes:
            p = handler1.make_pathlist_to_leaf_tuple(i)
    print(p)


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
    shortest_paths(chol_smiles, 2, 11)


if __name__ == '__main__':
    # not_main()
    main()
