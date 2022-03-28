import unittest
from copy import deepcopy
from handling_trees import TreeHandler
from making_trees import AtomTree
from rdkit.Chem import MolFromSmiles, Atom
from atom_tree_mock import AtomTreeMock


class TestTreeHandler(unittest.TestCase):
    def setUp(self):
        self.smiles_al = "COCNCC=O"
        self.smiles_tbf = "O=P(OCCCC)(OCCCC)OCCCC"
        self.smiles_arg = "NC(CCCNC(N)=N)C(O)=O"
        self.mol_al = MolFromSmiles(self.smiles_al)
        self.mol_tbf = MolFromSmiles(self.smiles_tbf)
        self.mol_arg = MolFromSmiles(self.smiles_arg)
        self.atom_tree_al = AtomTree(self.mol_al)
        self.atom_tree_tbf = AtomTree(self.mol_tbf)
        self.atom_tree_arg = AtomTree(self.mol_arg)
    
    @staticmethod
    def atomtree_and_atom_to_tuples_set(atom_tree: AtomTree,
                                        atom: Atom,
                                        what_in_result="element"):
        atom_tree.create_atom_node(atom)
        atom_tree.grow()
        # transform list of lists paths_to_leaves
        # in set of tuples for more convenient comparison
        paths_to_leaves = atom_tree.paths_to_leaves()
        paths_to_leaves_by_symbols = []
        for path_list in paths_to_leaves:
            symbols_path_list = []
            for atom_id in path_list:
                if what_in_result == "element":
                    symbols_path_list.append(
                        atom_tree.molecule.GetAtomWithIdx(atom_id).GetSymbol()
                    )
                elif what_in_result == "bond":
                    symbols_path_list.append(
                        atom_tree.get_node(atom_id).data.bond_to_parent
                    )
            paths_to_leaves_by_symbols.append(tuple(symbols_path_list))
        result_set = set(paths_to_leaves_by_symbols)
        return result_set


    def test_grow1(self):
        # Find nitrogen atom:
        start_atom = None
        for atom in self.mol_al.GetAtoms():
            if atom.GetSymbol() == "N":
                start_atom = atom
                break
        # Make tree:
        result_set = self.atomtree_and_atom_to_tuples_set(self.atom_tree_al,
                                                          start_atom,
                                                          what_in_result="element")
        self.assertEqual(result_set, {('N', 'C', 'O', 'C'),
                                      ('N', 'C', 'C', 'O')})

    def test_grow2(self):
        # Find nitrogen atom:
        start_atom = None
        for atom in self.mol_al.GetAtoms():
            if atom.GetSymbol() == "N":
                start_atom = atom
                break
        # Make tree:
        result_set = self.atomtree_and_atom_to_tuples_set(self.atom_tree_al,
                                                          start_atom,
                                                          what_in_result="bond")
        self.assertEqual(result_set, {(None, '-', '-', '-'),
                                      (None, '-', '-', '=')})

    def test_grow3(self):
        # Tree from phosphate double-bound O
        start_atom = None
        for atom in self.mol_tbf.GetAtoms():
            neighbors_symbols = list(map(lambda x: x.GetSymbol(), 
                                         atom.GetNeighbors()))
            if neighbors_symbols == ['P']:
                start_atom = atom
                break
        result_set = self.atomtree_and_atom_to_tuples_set(self.atom_tree_tbf,
                                                          start_atom,
                                                          what_in_result="element")
        self.assertEqual(result_set, {('O', 'P', 'O', 'C', 'C', 'C', 'C'),
                                      ('O', 'P', 'O', 'C', 'C', 'C', 'C'),
                                      ('O', 'P', 'O', 'C', 'C', 'C', 'C')})

    def test_grow4(self):
        # Tree from phosphate double-bound O
        start_atom = None
        for atom in self.mol_tbf.GetAtoms():
            neighbors_symbols = list(map(lambda x: x.GetSymbol(), 
                                         atom.GetNeighbors()))
            if neighbors_symbols == ['P']:
                start_atom = atom
                break
        result_set = self.atomtree_and_atom_to_tuples_set(self.atom_tree_tbf,
                                                          start_atom,
                                                          what_in_result="bond")
        self.assertEqual(result_set, {(None, '=', '-', '-', '-', '-', '-'),
                                      (None, '=', '-', '-', '-', '-', '-'),
                                      (None, '=', '-', '-', '-', '-', '-')})

    def test_grow5(self):
        # Tree from ester O that's neighbors are P and C
        start_atom = None
        for atom in self.mol_tbf.GetAtoms():
            neighbors_symbols = list(map(lambda x: x.GetSymbol(), 
                                         atom.GetNeighbors()))
            neighbors_symbols.sort()
            if atom.GetSymbol() == "O" and neighbors_symbols == ['C', 'P']:
                start_atom = atom
                break
        result_set = self.atomtree_and_atom_to_tuples_set(self.atom_tree_tbf,
                                                          start_atom,
                                                          what_in_result="element")
        self.assertEqual(result_set, {('O', 'C', 'C', 'C', 'C'),
                                      ('O', 'P', 'O'),
                                      ('O', 'P', 'O', 'C', 'C', 'C', 'C'),
                                      ('O', 'P', 'O', 'C', 'C', 'C', 'C')})

    def test_grow6(self):
        # Tree from ester O that's neighbors are P and C
        start_atom = None
        for atom in self.mol_tbf.GetAtoms():
            neighbors_symbols = list(map(lambda x: x.GetSymbol(), 
                                         atom.GetNeighbors()))
            neighbors_symbols.sort()
            if atom.GetSymbol() == "O" and neighbors_symbols == ['C', 'P']:
                start_atom = atom
                break
        result_set = self.atomtree_and_atom_to_tuples_set(self.atom_tree_tbf,
                                                          start_atom,
                                                          what_in_result="bond")
        self.assertEqual(result_set, {(None, '-', '-', '-', '-'),
                                      (None, '-', '='),
                                      (None, '-', '-', '-', '-', '-', '-'),
                                      (None, '-', '-', '-', '-', '-', '-')})


if __name__ == '__main__':
    unittest.main()
