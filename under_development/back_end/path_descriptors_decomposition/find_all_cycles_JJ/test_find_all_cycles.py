# There is one unevidant fact, that for some graphs
# can exist several cycles, that include the same
# set of nodes, but in different order. That is why
# representation of cycle as set() is incorrect way.
# So here was used representation of cycles as lists,
# that were transformed into unified form with
# choose_minimal_repr() function.


from pprint import pprint
import unittest
import networkx as nx

from cleaned_data import data
from find_all_cycles import find_all_cycles


def create_graph(list_of_edges):
    graph = nx.Graph()
    all_nodes = set()
    for edge in list_of_edges:
        all_nodes |= set(edge)
    graph.add_nodes_from(all_nodes)
    graph.add_edges_from(list_of_edges)
    return graph


def sort_by_length(list_):
    list_.sort()
    list_.sort(key=len)
    return list_


def pop_last_items_and_order(list_):
    for i, inner_list in enumerate(list_):
        inner_list.pop()
        list_[i] = choose_minimal_repr(inner_list)
    return list_


def just_order(list_):
    for i, inner_list in enumerate(list_):
        list_[i] = choose_minimal_repr(inner_list)
    return list_


def choose_minimal_repr(list_):
    candidates = []
    for i in range(len(list_)):
        candidates.append(list_[i:] + list_[:i])
    list_.reverse()
    for i in range(len(list_)):
        candidates.append(list_[i:] + list_[:i])
    return min(candidates)


class TestFindAllRings(unittest.TestCase):
    def setUp(self):
        self.graph1 = create_graph(data[1]["edges"])
        self.graph2 = create_graph(data[2]["edges"])
        self.graph3 = create_graph(data[3]["edges"])
        self.graph4 = create_graph(data[4]["edges"])
        self.graph5 = create_graph(data[5]["edges"])
        self.graph6 = create_graph(data[6]["edges"])

        self.rings_list1 = data[1]["rings"]
        self.rings_list2 = data[2]["rings"]
        self.rings_list3 = data[3]["rings"]
        self.rings_list4 = data[4]["rings"]
        self.rings_list5 = data[5]["rings"]
        self.rings_list6 = data[6]["rings"]
    
    def test_find_all_rings(self):
        self.assertEqual(
            sort_by_length(just_order(find_all_cycles(self.graph1))),
            sort_by_length(pop_last_items_and_order(self.rings_list1))
        )
        self.assertEqual(
            sort_by_length(just_order(find_all_cycles(self.graph2))),
            sort_by_length(pop_last_items_and_order(self.rings_list2))
        )
        self.assertEqual(
            sort_by_length(just_order(find_all_cycles(self.graph3))),
            sort_by_length(pop_last_items_and_order(self.rings_list3))
        )
        self.assertEqual(
            sort_by_length(just_order(find_all_cycles(self.graph4))),
            sort_by_length(pop_last_items_and_order(self.rings_list4))
        )
        self.assertEqual(
            sort_by_length(just_order(find_all_cycles(self.graph5))),
            sort_by_length(pop_last_items_and_order(self.rings_list5))
        )
        self.assertEqual(
            sort_by_length(just_order(find_all_cycles(self.graph6))),
            sort_by_length(pop_last_items_and_order(self.rings_list6))
        )


if __name__ == '__main__':
    unittest.main()
