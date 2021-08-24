from mol_classes import LazyMol
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
    for field_name in ["id", "when_created", "who_updated"]:
        if field_name in summary:
            raise ValueError(f"summary dict can't contain '"
                             f"{field_name}' key, {field_name} "
                             f"field is generated"
                             f"automatically")
    extra_keys = set(summary) - set(FIELD_VALUES_TYPES)
    if extra_keys:
        raise ValueError(f"Some extra keys in 'summary' dict: "
                         f"'{"', '".join(list(extra_keys))}'")
    for key, value in summary.items():
        if (isinstance(summary[key], FIELD_VALUES_TYPES[key]) or 
                (summary[key].__class__.__name__ == 
                 FIELD_VALUES_TYPES[key])):
            raise TypeError("Some values in 'summary' dict have "
                            "wrong types")


def if_lacks_add_items(summary):
    """If 'summary' dict does contains 'structure' but
    'molar_mass', 'molecular_formula' and 'mol_block'
    for some reason doesn's, this method will add
    them to 'summary'. Otherwise 'summary' won't be
    changed.
    Returns 'summary'
    """
    lacking_keys = filter(lambda x: not summary.get(x), 
                          ["molar_mass", 
                           "molecular_formula", 
                           "mol_block"])
    if lacking_keys:
        lazy_mol = LazyMol(summary["structure"])
        if not summary.get("molar_mass"):
            summary["molar_mass"] = lazy_mol.molar_weight
        if not summary.get("molecular_formula"):
            summary["molecular_formula"] = lazy_mol.molecular_formula
        if not summary.get["mol_block"]:
            summary["mol_block"] = lazy_mol.molblock
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
