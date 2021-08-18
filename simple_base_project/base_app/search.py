from collections import OrderedDict, namedtuple
import uuid
from base_app.models import Chemical, Element, ElementAbundance, \
    QuantityUnit, StoragePlace
from mol_classes import LazyMol


class SearchException(BaseException):
    pass


def primary_search(search_order: OrderedDict, q_set=None):
    if len(search_order) > 1:
        elem_sym, index = search_order.popitem(last=False)
        element_obj = Element.get_by_symbol(elem_sym)
        if not q_set:
            new_q_set = Chemical.objects \
                .filter(chemicalelemetnrel__element=element_obj,
                        chemicalelemetnrel__index__gte=index)
            return primary_search(search_order, new_q_set)
    elif len(search_order) == 1:
        elem_sym, index = search_order.popitem(last=False)
        element_obj = Element.get_by_symbol(elem_sym)
        new_q_set = \
            q_set.filter(chemicalelemetnrel__element=element_obj,
                         chemicalelemetnrel__index__gte=index)
        return new_q_set
    else:
        raise SearchException("search_order всё.")


def find_superstructures(mol_block):
    substructure = LazyMol(mol_block)
    sorted_by_abundances = ElementAbundance.get_abundance_list()
    substructure_elements = substructure.elements_list()
    if set(substructure_elements) - set(sorted_by_abundances):
        raise SearchException("Unique elements present in mol-query")
    order_of_search = substructure.elements_dict(template=sorted_by_abundances)
    n = 0
    cleaned_results = []
    raw_results = primary_search(order_of_search, None)
    Matched = namedtuple("Matched", ["id", "uuid",
                                     "name", "storage_place"])
    for i in raw_results:
        inchi = i.structure['inchi']
        potential_superstructure = LazyMol(inchi)
        if potential_superstructure % substructure:
            match = Matched(id=i.id, name=i.name, uuid=str(uuid.uuid4()),
                            storage_place=i.#Пока неясно как вызвать)

