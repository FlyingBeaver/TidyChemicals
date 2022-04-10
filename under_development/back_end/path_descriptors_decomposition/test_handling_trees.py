import unittest
from copy import deepcopy
from handling_trees import TreeHandler
from making_trees import AtomTree, BOND_SYMBOLS
from rdkit.Chem import MolFromSmiles
from rdkit.Chem.rdmolops import GetShortestPath
from atom_tree_mock import AtomTreeMock
from random import choice, randint, seed


class TestTreeHandler(unittest.TestCase):
    @staticmethod
    def random_gen(from_0_to=100, dont_include: (int, list, None) = None):
        if isinstance(dont_include, int):
            dont_include_ = [dont_include]
        elif isinstance(dont_include, list):
            dont_include_ = dont_include
        else:
            raise TypeError(f"Wrong 'dont_include' type: "
                            f"{type(dont_include)}. Must be list or int")
        while True:
            rand = randint(0, from_0_to)
            if rand not in dont_include_:
                yield rand

    @staticmethod
    def make_handlers(mol_object, atom1, atom2):
        tree1 = AtomTree(mol_object)
        tree2 = deepcopy(tree1)
        tree1.create_atom_node(atom1)
        tree2.create_atom_node(atom2)
        tree1.grow()
        tree2.grow()
        tree_handler1 = TreeHandler(tree1)
        tree_handler2 = TreeHandler(tree2)
        return tree_handler1, tree_handler2

    @staticmethod
    def sort_tuple(tup: tuple):
        list_from_tuple = list(tup)
        list_from_tuple.sort()
        return tuple(list_from_tuple)

    def test_find_common_nodes1(self):
        """Substance: diethyl ether
        Path from methyl to methyl
        Common node to be found must be O
        """
        ether_smiles = "CCOCC"
        ether_mol = MolFromSmiles(ether_smiles)
        #Finding two methyl groups:
        methyl_c1 = None
        methyl_c2 = None
        for atom in ether_mol.GetAtoms():
            if (atom.GetSymbol() == "C" and
                len(list(atom.GetNeighbors())) == 1 and
                not methyl_c1):
                methyl_c1 = atom
            elif (atom.GetSymbol() == "C" and
                  len(list(atom.GetNeighbors())) == 1 and
                  not methyl_c2):
                methyl_c2 = atom
        
        (methyl_c1_tree_handler,
         methyl_c2_tree_handler) = self.make_handlers(ether_mol,
                                                      methyl_c1,
                                                      methyl_c2)

        result = methyl_c1_tree_handler.find_common_nodes(methyl_c2_tree_handler)
        list_of_common_atom_indices, distance_to_common_atoms = result
        common_atom_symbols = list(
            map(lambda x: ether_mol.GetAtomWithIdx(x).GetSymbol(), 
                list_of_common_atom_indices)
        )
        self.assertEqual(["O"], common_atom_symbols)
        for atom_id in list_of_common_atom_indices:
            distance = len(GetShortestPath(ether_mol, atom_id, methyl_c1.GetIdx())) - 1
            self.assertEqual(distance_to_common_atoms, distance)
        for atom_id in list_of_common_atom_indices:
            distance = len(GetShortestPath(ether_mol, atom_id, methyl_c2.GetIdx())) - 1
            self.assertEqual(distance_to_common_atoms, distance)

    def test_find_common_nodes2(self):
        """Even substance
        Substance: dyethyl ether
        Path from methyl to methyl
        Common node to be found must be O
        """
        conc_smiles = "CONC"
        conc_mol = MolFromSmiles(conc_smiles)
        #Finding two methyl groups:
        methyl_c1 = None
        methyl_c2 = None
        for atom in conc_mol.GetAtoms():
            if (atom.GetSymbol() == "C" and
                len(list(atom.GetNeighbors())) == 1 and
                not methyl_c1):
                methyl_c1 = atom
            elif (atom.GetSymbol() == "C" and
                  len(list(atom.GetNeighbors())) == 1 and
                  not methyl_c2):
                methyl_c2 = atom

        (methyl_c1_tree_handler,
         methyl_c2_tree_handler) = self.make_handlers(conc_mol,
                                                      methyl_c1,
                                                      methyl_c2)

        result = methyl_c1_tree_handler.find_common_nodes(methyl_c2_tree_handler)
        list_of_common_atoms_tuples, distance_to_common_atoms = result
        # Нужно убедиться, что list_of_common_atoms_tuples содержит ("N", "O")
        the_tuple = list_of_common_atoms_tuples[0]
        symbols_tuple = tuple(
            map(lambda x: conc_mol.GetAtomWithIdx(x).GetSymbol(),
                the_tuple)
        )
        self.assertEqual(self.sort_tuple(symbols_tuple),
                         self.sort_tuple(("N", "O"))
                         )
        self.assertEqual(len(list_of_common_atoms_tuples), 1)



    def test_find_common_nodes3(self):
        """Even substance
        Substance: dyethyl ether
        Path from methyl to methyl
        Common node to be found must be O
        """
        hetq_smiles = "CC1(OP=C(C)NS1)C1CC1"
        hetq_mol = MolFromSmiles(hetq_smiles)
        #Finding two methyl groups:
        methyl_c1 = None
        methyl_c2 = None
        for atom in hetq_mol.GetAtoms():
            if (atom.GetSymbol() == "C" and
                len(list(atom.GetNeighbors())) == 1 and
                not methyl_c1):
                methyl_c1 = atom
            elif (atom.GetSymbol() == "C" and
                  len(list(atom.GetNeighbors())) == 1 and
                  not methyl_c2):
                methyl_c2 = atom

        (methyl_c1_tree_handler,
         methyl_c2_tree_handler) = self.make_handlers(hetq_mol,
                                                      methyl_c1,
                                                      methyl_c2)

        result = methyl_c1_tree_handler.find_common_nodes(methyl_c2_tree_handler)
        list_of_common_atoms_tuples, distance_to_common_atoms = result
        list_to_compare = []
        for tup in list_of_common_atoms_tuples:
            list_to_compare.append(
                set(map(lambda x: hetq_mol.GetAtomWithIdx(x).GetSymbol(),
                        tup
                        )
                )
            )
        list_to_compare.sort()
        expected_list = [{"P", "O"}, {"S", "N"}]
        expected_list.sort()
        self.assertEqual(list_to_compare, expected_list)


    def test_make_pathlist_to_leaf_int(self):
        tree_mock = AtomTreeMock((1, "N"), 4, 0)
        tree_mock.make_mock_tree()
        tree_handler = TreeHandler(tree_mock)

        path_to_the_root = []
        path_to_the_root.append(tree_mock.tail_ids[-1])
        root_id = tree_mock.root

        while path_to_the_root[-1] != root_id:
            current_node = tree_mock.parent(path_to_the_root[-1])
            current_node_id = current_node.identifier
            path_to_the_root.append(current_node_id)
        path_to_the_root.reverse()

        self.assertEqual(path_to_the_root, 
                         tree_handler.make_pathlist_to_leaf_int(1, 3))


    def test_make_pathlist_to_leaf_tuple(self):
        tree_mock = AtomTreeMock((1, "O", 2, "C", "="), 4, 0)
        tree_mock.make_mock_tree()
        tree_handler = TreeHandler(tree_mock)
        
        path_to_the_root = []
        path_to_the_root.append(tree_mock.tail_ids[-1])
        root_id = tree_mock.root

        while path_to_the_root[-1] != root_id:
            current_node = tree_mock.parent(path_to_the_root[-1])
            current_node_id = current_node.identifier
            path_to_the_root.append(current_node_id)
        path_to_the_root.reverse()

        self.assertEqual(path_to_the_root, 
                         tree_handler.make_pathlist_to_leaf_int(2, 3))
    
    def test_unite_pathlists1(self):
        random_generator = self.random_gen(dont_include=[1, 2])
        lists_length = choice(list(range(5, 15)))
        mock_pathlist1 = list(map(lambda x: next(random_generator), 
                                  range(lists_length)))
        mock_pathlist2 = list(map(lambda x: next(random_generator), 
                                  range(lists_length)))
    
        mock_united_pathlist = (mock_pathlist1 +
                                [1, 2] +
                                list(reversed(mock_pathlist2))
                                )
        mock_pathlist1 += [1, 2]
        mock_pathlist2 += [2, 1]

        self.assertEqual(mock_united_pathlist,
                         TreeHandler.unite_pathlists(mock_pathlist1,
                                                     mock_pathlist2)
                         )

    def test_unite_pathlists2(self):
        mock_pathlist1 = [52, 71, 36, 65, 38, 83, 19, 39, 1, 2]
        mock_pathlist2 = [63, 8, 24, 40, 56, 68, 66, 23, 2, 1]
        mock_united_pathlist = [52, 71, 36, 65, 38, 83, 19, 39, 1,
                                2, 23, 66, 68, 56, 40, 24, 8, 63]
        self.assertEqual(mock_united_pathlist, 
                         TreeHandler.unite_pathlists(mock_pathlist1,
                                                     mock_pathlist2)
                         )

    def test_make_pathstring1(self):

        def pathstring_from_path(some_path):
            pathstring = ''
            for index, atom_id in enumerate(some_path):
                pathstring += chol.GetAtomWithIdx(atom_id).GetSymbol()
                if index < len(some_path) - 1:
                    bond = chol.GetBondBetweenAtoms(atom_id, some_path[index + 1])
                    if str(bond.GetBondType()) != "SINGLE":
                        pathstring += BOND_SYMBOLS[str(bond.GetBondType())]
            return pathstring

        def pathstring_transformation(some_path):
            """make pathstring from path, makes
            pathlist and reversed pathlist, compares and
            returns one with least value"""
            some_path_rev = list(reversed(some_path))
            return min(pathstring_from_path(some_path),
                       pathstring_from_path(some_path_rev))

        chololesterol_smiles = ("C[C@H](CCCC(C)C)[C@H]1CC[C@@H]2"
                                "[C@@]1(CC[C@H]3[C@H]2CC=C4[C@@]"
                                "3(CC[C@@H](C4)O)C)C")
        chol = MolFromSmiles(chololesterol_smiles)
        n_of_atoms = chol.GetNumAtoms()
        atom_id1 = randint(0, n_of_atoms - 1)
        atom_id2 = next(self.random_gen(from_0_to=(n_of_atoms - 1), dont_include=atom_id1))
        path = GetShortestPath(chol, atom_id1, atom_id2)
        path_rev = list(reversed(path))
        pathstring1_test = pathstring_transformation(path)
        pathstring2_test = pathstring_transformation(path_rev)
        
        tree = AtomTree(chol)
        tree.create_atom_node(chol.GetAtomWithIdx(0))
        tree.grow()
        tree_handler = TreeHandler(tree)
        pathstring1 = tree_handler.make_pathstring(path)
        pathstring2 = tree_handler.make_pathstring(path_rev)

        self.assertTrue((pathstring1 == pathstring1_test and
                         pathstring2 == pathstring2_test
                         ) or (
                         pathstring1 == pathstring2_test and
                         pathstring2 == pathstring1_test))

    def test_make_pathstring2(self):
        smiles_tbf = "O=P(OCCCC)(OCCCC)OCCCC"
        tbf = MolFromSmiles(smiles_tbf)
        methyl_carbons_ids = []
        for atom_id in range(tbf.GetNumAtoms()):
            atom = tbf.GetAtomWithIdx(atom_id)
            neighbors = []
            for neigh in atom.GetNeighbors():
                neighbors += neigh.GetSymbol()
            if neighbors == ['C'] and atom.GetSymbol() == 'C':
                methyl_carbons_ids.append(atom_id)

        methyl_id1 = methyl_carbons_ids[0]
        methyl_id2 = methyl_carbons_ids[1]

        # по-другому он работает
        tbf_tree = AtomTree(tbf)
        tbf_tree.create_atom_node(tbf.GetAtomWithIdx(0))
        tbf_tree.grow()
        tbf_handler = TreeHandler(tbf_tree)

        path = GetShortestPath(tbf, methyl_id1, methyl_id2)

        self.assertEqual(tbf_handler.make_pathstring(path), "CCCCOPOCCCC")



if __name__ == '__main__':
    unittest.main()
