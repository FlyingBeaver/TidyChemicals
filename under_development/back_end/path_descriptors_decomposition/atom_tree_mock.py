import unittest
from collections import namedtuple
# from rdkit.Chem import MolFromSmiles
from handling_trees import TreeHandler
from making_trees import AtomTree
from random import choice, randint, shuffle, seed
from time import time
from treelib import Tree



# counter = 0
# seed(1)
AtomData = namedtuple("AtomData", "elem_symbol, bond_to_parent")



def GEN(randoms_start_with, id1, id2=None):
    numbers = list(range(randoms_start_with,
                         100 + randoms_start_with))
    if id1 in numbers:
        numbers.remove(id1)
    if id2 in numbers:
        numbers.remove(id2)
    while numbers:
        rand = choice(numbers)
        numbers.remove(rand)
        yield rand


class AtomTreeMock(AtomTree):
    def __init__(self, tail: (tuple), levels_no: int, randoms_start_with:int=0):
        # tail is a tuple, that contains:
        # IF IT CONTAINS 5 ITEMS
        # 1) id of the 1st atom
        # 2) element of the 1st atom
        # 3) id of the 2nd atom
        # 4) element of the 2nd atom
        # 5) symbol of the bond between 1st and 2nd atoms
        # IF IT CONTAINS 3 ITEMS
        # 1) id of the 1st atom
        # 2) element of the 1st atom
        # 3) symbol of the bond between 1st and previous atoms
        # Levels_no -- how many levels will
        if len(tail) == 5:
            self.tail_ids = tail[0], tail[2]
            self.tail_elements = tail[1], tail[3]
            self.tail_bond = tail[4]
            self.gen = GEN(randoms_start_with, tail[0], tail[2])
        elif len(tail) == 2:
            self.tail_ids = (tail[0], )
            self.tail_elements = (tail[1], )
            self.tail_bond = None
            self.gen = GEN(randoms_start_with, tail[0])
        else:
            raise ValueError("Wrong length of the 'tail' tuple")
        self.levels_no = levels_no
        super().__init__(molecule = None)

    def make_mock_tree(self):
        start = True
        # Итерация по уровням дерева:
        for i in range(self.levels_no):
            # Если это корень:
            if start:
                node_data = self.make_node_data()
                args_ = node_data["args"]
                kwargs_ = node_data["kwargs"]
                self.create_node(*args_, **kwargs_)
                start = False
            # Если это не корень: итерация для 
            # листьев. У листа создаются дети
            else:
                for leaf in self.leaves():
                    self.process_leaf(leaf)
        self.add_small_tree()


    def process_leaf(self, leaf):
        # От одного до 3-х детей создаётся у листа:
        for iteration in range(choice([1, 2, 3])):
            leaf_id = leaf.identifier
            node_data = self.make_node_data(leaf_id)
            args_ = node_data["args"]
            kwargs_ = node_data["kwargs"]
            self.create_node(*args_, **kwargs_)


    def make_node_data(self, parent_id = None):
        element_symbol = choice(["C", "C", "C", "N", "O", "O", "N", "P", "S"])
        node_id = next(self.gen)
        if parent_id is not None:
            bond_symbol = choice(["-", "-", "-", "=", "=", "#"])
        else:
            bond_symbol = None
        data = AtomData(element_symbol, bond_symbol)
        if parent_id is not None:
            return {"args": [element_symbol, node_id],
             "kwargs": 
                {"parent": parent_id,
                 "data": data}
            }
        else:
            return {"args": [element_symbol, node_id],
             "kwargs": 
                {"data": data}
            }
    
    def add_small_tree(self):
        all_nodes = self.all_nodes()
        shuffle(all_nodes)
        if len(self.tail_ids) == 2:
            grandfather_id = None
            for future_parent in all_nodes:
                grandfather_id = future_parent.identifier
                level_no = self.level(grandfather_id)
                if level_no == self.levels_no - 3:
                    break
            small_tree = Tree()
            small_tree.create_node(self.tail_elements[0],
                                   self.tail_ids[0],
                                   data=AtomData(self.tail_elements[0],
                                                 choice(["-", "-",
                                                         "-", "=",
                                                         "=", "#"]))
                                    )
            small_tree.create_node(self.tail_elements[1],
                                   self.tail_ids[1],
                                   parent=self.tail_ids[0],
                                   data=AtomData(self.tail_elements[1], 
                                                 self.tail_bond)
                                   )
            self.paste(grandfather_id, small_tree)
        elif len(self.tail_ids) == 1:
            father_id = None
            for future_parent in all_nodes:
                father_id = future_parent.identifier
                level_no = self.level(father_id)
                if level_no == self.levels_no - 2:
                    break
            # # for debug
            # global counter
            # print("!!!!!!!!!counter:")
            # print(counter)
            # counter += 1
            # # for debug ends
            # import pdb; pdb.set_trace()
            self.create_node(self.tail_elements[0],
                             self.tail_ids[0],
                             parent=father_id,
                             data=AtomData(self.tail_elements[0],
                                           choice(["-", "-", "-", "=", "=", "#"])
                                           )
                             )
        else:
            raise ValueError("Wrong lenfth of 'tail_id' tuple")
