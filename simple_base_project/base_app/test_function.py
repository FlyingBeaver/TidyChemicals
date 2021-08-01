from rdkit import Chem
from time import sleep
from rdkit.Chem.Descriptors import ExactMolWt


class BruttoException(BaseException):
    pass


def brutto_calc(mol_obj):
    inchi = Chem.inchi.MolToInchi(mol_obj)
    inchi_brutto = inchi.split('/')[1]
    small_bruttos = inchi_brutto.split('.')
    separated = []
    result = []
    for short_brutto in small_bruttos:
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

        for i in brutto_dict:
            brutto_dict[i] *= multiplier

    first_brutto = result.pop(0)
    while len(result):
        brutto_intersection = set(first_brutto) & set(result[0])
        if brutto_intersection:
            for element in brutto_intersection:
                first_brutto[element] += result[0][element]
            result.pop(0)
        else:
            first_brutto |= result.pop(0)

    return first_brutto


def check(molecule, form):
    if form == 'smiles':
        subst = Chem.MolFromSmiles(molecule)
    elif form == 'inchi':
        subst = Chem.inchi.MolFromInchi(molecule)
    else:
        raise BruttoException('чё?')
    sum = 0
    brutto_d = brutto_calc(subst)
    for i in brutto_d:
        sum += (ExactMolWt(Chem.inchi.MolFromInchi(f"InChI=1S/{i}")) *
                brutto_d[i])
    rusult = (sum == ExactMolWt(subst))
    print(rusult)
    if not rusult:
        print(f"sum is {sum}")
        print(f"ExactMolWt(subst) is {ExactMolWt(subst)}")
        print(f"brutto_d {brutto_d}")
    return rusult


smiles_salt = ("[Fe+2].O.O.[O-]P([O-])(=O)C1C[C@H]2[C@@H]3CC"
               "[C@H](O)[C@@]3(C)CC[C@@H]2[C@@]2(C)CCC(=O)C=C12")

salt = Chem.MolFromSmiles(smiles_salt)
print(brutto_calc(salt))

print("\n\n\n\n\################################\n")
