from collections import OrderedDict, namedtuple
import uuid
import datetime
from base_app.models import Chemical, Element, ElementAbundance, \
    QuantityUnit, StoragePlace
from base_app.mol_classes import LazyMol, MyMolError
from simple_base_project.settings import NOTATION_FOR_RENDERING


def start_pdb_debugging():
    import pdb; pdb.set_trace()


class SearchException(BaseException):
    pass


def primary_search(search_order: OrderedDict, q_set=None):
    if len(search_order) > 1:
        elem_sym, index = search_order.popitem(last=False)
        element_obj = Element.get_by_symbol(elem_sym)
        if not q_set:
            new_q_set = Chemical.objects \
                .filter(structelementrel__element=element_obj,
                        structelementrel__index__gte=index)
        else:
            new_q_set = q_set.filter(structelementrel__element=element_obj,
                                     structelementrel__index__gte=index)
        return primary_search(search_order, new_q_set)
    elif len(search_order) == 1:
        elem_sym, index = search_order.popitem(last=False)
        element_obj = Element.get_by_symbol(elem_sym)
        new_q_set = \
            q_set.filter(structelementrel__element=element_obj,
                         structelementrel__index__gte=index)
        return new_q_set
    else:
        raise SearchException("search_order всё.")


def find_superstructures(mol_block):
    if mol_block:
        substructure = LazyMol(mol_block, "mol")
    sorted_by_abundances = ElementAbundance.get_abundance_list()
    substructure_elements = substructure.elements_list
    if set(substructure_elements) - set(sorted_by_abundances):
        raise SearchException("Unique elements present in mol-query")
    order_of_search = substructure.elements_dict(template=sorted_by_abundances)
    n = 0
    cleaned_results = []
    raw_results = primary_search(order_of_search, None)
    print(60*"#")
    print(f"found {len(raw_results)}")
    print(60*"#")
    Matched = namedtuple("Matched", ["id", "uuid",
                                     "name", "storage_place",
                                     "molblock"])
    for i in raw_results:
        inchi = i.structure['inchi']
        try:
            potential_superstructure = LazyMol(inchi, "inchi", False)
        except MyMolError:
            with open("errors_log.txt", "at", encoding="utf-8") as log:
                date_time_string = datetime.datetime.now().strftime("%c")
                log.write(f"\n{date_time_string}: MyMolError at object "
                          f"with id={i.id}, name='{i.name}'\n")
        if potential_superstructure % substructure:
            if NOTATION_FOR_RENDERING == "inchi":
                structure_container = potential_superstructure
            elif NOTATION_FOR_RENDERING == "mol":
                structure_container = i.mol_block
            match = {"id": i.id, "name": i.name,
                     "storage_place": i.storage_place.path_str, 
                     "structure_container": structure_container}

            # match = Matched(id=i.id, name=i.name, uuid=str(uuid.uuid4()),
            #                 storage_place=i.storage_place.path_str,
            #                 molblock=i.mol_block) 
            # For some reason attribute error when trying to read from
            # namedtuple, what is weird

            cleaned_results.append(match)
        n += 1
        if not n % 100:
            print("checked:", n)
    return cleaned_results
