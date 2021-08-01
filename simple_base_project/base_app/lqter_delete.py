# from collections import OrderedDict
# from rdkit import Chem
# from rdkit.Chem.inchi import MolToInchi
# from rdkit.Chem.Descriptors import ExactMolWt
# from functools import reduce


class BruttoException(BaseException):
    pass




result = []
small_bruttos_cut = []
small_bruttos[-1] = '2H2O'
for short_brutto in small_bruttos:
    separated = []
    separated.append(short_brutto[0])
    short_brutto = short_brutto[1:]
    while True:
        try:
            if separated[-1][-1].isdigit() == short_brutto[0].isdigit():
                separated[-1] += short_brutto[0]
                short_brutto = short_brutto[1:]
            else:
                separated.append(short_brutto[0])
                short_brutto = short_brutto[1:]
        except IndexError:
            break

    brutto_dict = dict()
    multiplier = 1
    if separated[0].isdigit():
        multiplier = int(separated.pop(0))

    if separated[0].isdigit():
        raise BruttoException('Two indices in a row')
    while len(separated) > 1:
        if separated[0].isalpha() and separated[1].isdigit:
            element = separated.pop(0)
            index = separated.pop(0)
            brutto_dict[element] = int(index)
        elif separated[0].isalpha() and separated[1].isalpha():
            element = separated.pop(0)
            brutto_dict[element] = 1
    # Если остался 1 элемент списка
    if separated:
        element = separated.pop(0)
        brutto_dict[element] = 1
    result.append(brutto_dict)

first_brutto = result.pop(0)
while len(result):
    brutto_intersection = set(first_brutto) & set(result[0])
    if brutto_intersection:
        for element in brutto_intersection:
            first_brutto[element] += result[0][element]
        result.pop(0)
    else:
        first_brutto |= result.pop(0)

print(first_brutto)