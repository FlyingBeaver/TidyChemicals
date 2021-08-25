from base_app.mol_classes import LazyMol
import re


REQUIRED_KEYS = {'name', 
                 'storage_place', 
                 'quantity', 
                 'quantity_unit', 
                 'who_created'}

FIELD_VALUES_TYPES = {'name': str,
                      'name_format': str, 
                      'structure': dict, 
                      'mol_block': str, 
                      'molecular_formula': str, 
                      'molar_mass': float, 
                      'synonym': str, 
                      'comment': str, 
                      'cas': int, 
                      'storage_place': 'StoragePlace', 
                      'quantity': float, 
                      'quantity_unit': 'QuantityUnit', 
                      'hazard_pictograms': str, 
                      'who_created': 'Profile', 
                      'who_updated': 'Profile'}


def join_set(set_: set):
    return "'" + "', '".join(list(set_)) + "'"


def summary_dict_validation(summary):
    """
    It checks:
    -- if summary dict has keys he mustn't
        ("id", "when_created", "who_updated" that
        are auto generated)
    -- if summary dict has extra keys
    -- if summary dict's values are of correct type
    If summary is invalid, exception raised
    Method doesn't return anything
    """
    auto_gen_keys = {"id", "when_created", "who_updated"}
    if auto_gen_keys & set(summary):
        raise ValueError(f"summary dict can't contain '"
                         f"{join_set(auto_gen_keys & set(summary))} "
                         f"(generated automatically only)")
    extra_keys = set(summary) - set(FIELD_VALUES_TYPES)
    if extra_keys:
        raise ValueError(f"Some extra keys in 'summary' dict: "
                         f"'{join_set(extra_keys)}'")
    for key, value in summary.items():
        if isinstance(FIELD_VALUES_TYPES[key], str):
            if summary[key].__class__.__name__ == FIELD_VALUES_TYPES[key]:
                continue
        else:
            if isinstance(summary[key], FIELD_VALUES_TYPES[key]):
                continue
            else:
                raise TypeError(f"Some values in 'summary' dict have "
                                f"wrong types: key is {key}, type "
                                f"is {summary[key].__class__}")


def if_lacks_add_items(summary):
    """If 'summary' dict does contains 'structure' but
    'molar_mass', 'molecular_formula' and 'mol_block'
    for some reason doesn't, this method will add
    them to 'summary'. Otherwise 'summary' won't be
    changed.
    Returns 'summary'
    """
    # TODO Выглядит ужасно. Неплохо было бы переписать
    lacking_keys = filter(lambda x: not summary.get(x), 
                          ["molar_mass", 
                           "molecular_formula", 
                           "mol_block"])
    lacking_keys_list = list(lacking_keys)
    if lacking_keys_list:
        lazy_mol = None

        def make_lazymol(sum_dic):
            """Function for reuse the same lazymol obj"""
            nonlocal lazy_mol
            if not lazy_mol:
                lazy_mol = LazyMol(sum_dic["structure"]["inchi"])
            return lazy_mol

        if not summary.get("molar_mass"):
            summary["molar_mass"] = make_lazymol(summary).molar_weight
        if not summary.get("molecular_formula"):
            summary["molecular_formula"] = \
                make_lazymol(summary).molecular_formula
        if not summary.get["mol_block"]:
            summary["mol_block"] = make_lazymol(summary).molblock
    return summary


def check_and_correct(summary):
    """
    Method checks: 
        if there are mol_block, molecular_formula 
           or molar_mass with no structure
    If there are: 
        exception 
    but if vice versa,
        method 'if_lacks_add_items' 
        adds lacking fields to summary dict
    """
    if summary.get('structure'):
        if not summary['structure'].get('inchi'):
            raise ValueError("fiels 'structure' in 'summary' dict' "
                             "doesn't contain inchi")
        summary = if_lacks_add_items(summary)
    else:
        if any(map(lambda x: summary.get(x), 
                   ["molar_mass", "molecular_formula", "mol_block"])):
            raise ValueError("Summary can't contain 'molecular_formula', "
                             "'mol_block' or 'molar_mass' if it doesn't "
                             "contain 'structure', as it's a sign of "
                             "incomplete or wrong data")
    return summary


def are_there_required_keys(summary):
    if not REQUIRED_KEYS <= set(summary):
        raise ValueError("Not all required keys are in summary")
