from chemicals.services.mol_classes import LazyMol



class ValidationFailed(BaseException):
    pass


def validate_aq(aq):
    if structure["aq"].__class__ not in (int, list):
        raise ValidationFailed(
            "structure['aq'] must be int or list"
        )
    if (isinstance(structure["aq"], list) and
            len(structure["aq"]) != 2):
        raise ValidationFailed(
            "In case if structure['aq'] is list, "
            "its length must be 2."
        )
    if not (isinstance(structure["aq"], list) and
            isinstance(structure["aq"][0], int) and
            isinstance(structure["aq"][1], int)
        ):
        raise ValidationFailed(
            "One of values of structure['aq'] list "
            "is not integer."
        )


def empty_structure_validation(mol_block, structure):
    if (not (mol_block and structure) and
            (mol_block or structure)):
        raise ValueError(
            "'mol_block' and 'structure' can be empty or "
            "None only together"
        )


def empty(action):
    if action == "create"
        return dict(), dict(), dict()
    elif action == "update":
        return None, None, None
    else:
        raise ValueError("Wrong value of the"
                         "'action' argument")


def make_summary(mol_block: (str, None.__class__),
                 structure: (dict, None.__class__),
                 profile,
                 action: str):
    summary = dict()
    empty_structure_validation(mol_block, structure)
    if not mol_block:
        elem_dict, path_dict, ring_dict = empty(action)
    else:
        for key in structure.keys():
            if key != "aq":
                del structure[key]
        if "aq" in structure:
            validate_aq(structure["aq"])
        molecule = LazyMol(mol_block, "mol_block")
        inchi = molecule.inchi
        molar_mass = molecule.molar_weight
        molecular_formula = molecule.molecular_formula
        structure["inchi"] = inchi
        elem_dict = molecule.elements_dict()
        path_dict = molecule.path_dict()
        ring_dict = molecule.ring_dict()
        summary = {"molecular_formula": molecular_formula,
                   "molar_mass": molar_mass,
                   "structure": structure}
    if action == "create":
        summary["who_created"] = profile
    elif action == "update":
        summary["who_updated"] = profile
    else:
        raise ValueError("Wrong value of the 'action' argument")
    return (summary, elem_dict, path_dict, ring_dict)
        
