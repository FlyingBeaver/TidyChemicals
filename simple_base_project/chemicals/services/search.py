from collections import OrderedDict
import datetime

from django.db.models import FilteredRelation, Q
from rdkit.Chem.inchi import MolFromInchi
from rdkit.Chem.rdmolfiles import MolFromMolBlock

from chemicals.models import (
    Chemical, Element, QuantityUnit,
    StoragePlace, Path, Ring
)
from chemicals.services.mol_classes import LazyMol, MyMolError


class SearchException(BaseException):
    pass


def primary_search(search_order: OrderedDict, q_set=None):
    if not search_order:
        return q_set
    if q_set is None:
        elem_sym, index = search_order.popitem(last=False)
        element_obj = Element.get_by_symbol(elem_sym)
        if not q_set:
            new_q_set = Chemical.objects \
                .filter(chemical_element__element=element_obj,
                        chemical_element__n_of_occurrences__gte=index)
        else:
            new_q_set = q_set.filter(chemical_element__element=element_obj,
                                     chemical_element__n_of_occurrences__gte=index)
        return primary_search(search_order, new_q_set)
    else:
        elem_sym, index = search_order.popitem(last=False)
        element_obj = Element.get_by_symbol(elem_sym)
        new_q_set = \
            q_set.filter(chemical_element__element=element_obj,
                         chemical_element__n_of_occurrences__gte=index)
        return new_q_set


def secondary_search(path_dict: OrderedDict, primary_results=None):
    if not path_dict:
        raise SearchException("path_dict is empty")
    if primary_results:
        objects = primary_results
    else:
        objects = Chemical.objects
    link_table_name = "chemical_path"
    fk_name = "path"
    quantity_name = "n_of_occurrences"
    i = 1
    for label, n_of_occurrences in path_dict.items():
        relation_name = "pathFR" + str(i)
        condition_q = Q(**{link_table_name + "__" + fk_name: label})
        filtered_relation = FilteredRelation(link_table_name,
                                             condition=condition_q)
        objects = objects.annotate(
            **{relation_name: filtered_relation}
        ).filter(
            **{(relation_name + "__" +
                quantity_name + "__gte"): n_of_occurrences}
        )
        i += 1
    return objects


def tertiary_search(ring_dict: OrderedDict, previous_results=None):
    print(ring_dict)
    if not ring_dict:
        return previous_results
    if previous_results:
        objects = previous_results
    else:
        objects = Chemical.objects
    link_table_name = "chemical_ring"
    fk_name = "ring"
    quantity_name = "n_of_occurrences"
    i = 1
    for label, n_of_occurrences in ring_dict.items():
        relation_name = "ringFR" + str(i)
        condition_q = Q(**{link_table_name + "__" + fk_name: label})
        filtered_relation = FilteredRelation(link_table_name,
                                             condition=condition_q)
        objects = objects.annotate(
            **{relation_name: filtered_relation}
        ).filter(
            **{(relation_name + "__" +
                quantity_name + "__gte"): n_of_occurrences}
        )
        i += 1
    return objects


def find_superstructures(mol_block):
    substructure = LazyMol(mol_block, "mol")
    sorted_by_abundances = Element.get_ordered_elements_list()
    substructure_elements = substructure.elements_list
    if set(substructure_elements) - set(sorted_by_abundances):
        raise SearchException("Unique elements present in mol-query")
    ordered_elements_dict = substructure.elements_dict(
        template=sorted_by_abundances
    )
    if "H" in ordered_elements_dict:
        ordered_elements_dict.pop("H")
    raw_results1 = primary_search(ordered_elements_dict, None)
    path_dict = substructure.path_dict()
    ordered_path_dict = Path.order_path_dict(path_dict)
    raw_results2 = secondary_search(ordered_path_dict,
                                    primary_results=raw_results1)
    ring_dict = substructure.ring_dict()
    ordered_ring_dict = Ring.order_ring_dict(ring_dict)
    raw_results3 = tertiary_search(ordered_ring_dict,
                                   previous_results=raw_results2)
    print(60*"#")
    print(f"found: without paths {len(raw_results1)},\n" +
          f"with paths {len(raw_results2)}\n"
          f"with rings {len(raw_results3)}")
    print(60*"#")
    # check if there is need to 'clean' results
    if substructure.is_simple():
        return raw_results3

    cleaned_results = []
    n = 0
    for item in raw_results3:
        mol_block = item.mol_block
        try:
            potential_superstructure = LazyMol(mol_block, "mol_block", False)
        except MyMolError:
            with open("errors_log.txt", "at", encoding="utf-8") as log:
                date_time_string = datetime.datetime.now().strftime("%c")
                log.write(f"\n{date_time_string}: MyMolError at object "
                          f"with id={item.id}, name='{item.name}'\n")
            continue
        if potential_superstructure % substructure:
            match = {"chemical": item, "lazymol": potential_superstructure}
            cleaned_results.append(match)
        n += 1
        if not n % 100:
            print("checked:", n)

    return cleaned_results
