from rest_framework.serializers import ValidationError
from chemicals.services.mol_classes import LazyMol, MyMolError
from api.services.validations import validate_water_number



def empty_structure_validation(mol_block, water_number):
    if not mol_block and water_number != 0:
        raise ValueError(
            "If mol_block is None, water_number must be 0"
        )


# def empty(action):
#     if action == "create":
#         return dict(), dict(), dict()
#     elif action == "update":
#         return None, None, None
#     else:
#         raise ValueError("Wrong value of the"
#                          "'action' argument")


def make_summary(mol_block: (str, None.__class__),
                 water_number: (int, list, None.__class__),
                 profile,
                 action: str):
    summary = dict()
    if (not mol_block or mol_block == "Nothing") and action == "create":
        elem_dict = dict()
        path_dict = dict()
        ring_dict = dict()
    elif not mol_block and action == "update":
        elem_dict = None
        path_dict = None
        ring_dict = None
    elif mol_block == "Nothing" and action == "update":
        elem_dict = dict()
        path_dict = dict()
        ring_dict = dict()
    else:
        if water_number != 0 and water_number is not None:
            validate_water_number(water_number)
        try:
            molecule = LazyMol(mol_block, "mol_block")
        except MyMolError as mme:
            raise ValidationError(
                "Failed to create LazyMol object "
                f"because of MyMolError: '{str(mme)}'"
            )
        except BaseException as be:
            raise ValidationError(
                "Failed to create LazyMol object "
                f"because of the exception: '{repr(be)}'"
            )
        molar_mass = molecule.molar_weight
        molecular_formula = molecule.molecular_formula
        elem_dict = molecule.elements_dict()
        path_dict = molecule.path_dict()
        ring_dict = molecule.ring_dict()
        summary = {"molecular_formula": molecular_formula,
                   "molar_mass": molar_mass}
    if action == "create":
        summary["who_created"] = profile
    elif action == "update":
        summary["who_updated"] = profile
    else:
        raise ValueError("Wrong value of the 'action' argument")
    return (summary, elem_dict, path_dict, ring_dict)


