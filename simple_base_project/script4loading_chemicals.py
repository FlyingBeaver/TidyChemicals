import datetime
import time
from random import choice, randint
from base_app.mol_classes import LazyMol
from normal_files import normal_files
from profiles.models import Profile
from base_app.models import QuantityUnit, StoragePlace, Chemical


def wait():
    time.sleep(0.2)


STORAGE_PLACES = list(StoragePlace.objects.filter(terminal=True))
fake_name_position = 0


def find_user_by_name(name: str):
    return Profile.objects.get(user__username=name)


def find_unit_by_symbol(symbol: str):
    return QuantityUnit.objects.get(unit_symbol=symbol)


def choose_storage_place():
    return choice(STORAGE_PLACES)


darth_vader = find_user_by_name("DarthVader")
oleg_gazmanov = find_user_by_name("OlegGazmanov")
billie_eilish = find_user_by_name("BillieEilish")

milliliter = find_unit_by_symbol("ml")
milligram = find_unit_by_symbol('mg')
liter = find_unit_by_symbol('l')
gram = find_unit_by_symbol('g')
kilogram = find_unit_by_symbol('kg')


with open("11thousands_of_fake_names.txt", "rt", encoding="utf-8") as f:
    long_string = f.read()
    GENERATED_NAMES = list(map(lambda x: x.strip(), long_string.split('\n')))
name_number = 0


def make_name():
    global name_number
    name_number += 1
    return GENERATED_NAMES[name_number]


def smart_choice(prob_dict: dict):
    """Принимает словарь, где ключи -- какие-нибудь
    объекты либо списки или кортежи из каких-нибудь
    объектов, а значения -- целые числа, показывающие
    вероятность в процентах, или чём-нибудь
    ещё. Если ключ -- не список и не кортеж, то функция
    выдаёт ключ с вероятностью, определённой в значении.
    Если ключ -- список или кортеж, функция выдаёт любой
    из элементов списка или кортежа с вероятностью,
    равной значению для каждого из элементов"""

    if not all(map(lambda x: isinstance(prob_dict[x], int), prob_dict)):
        raise ValueError()
    items = []
    for i in prob_dict:
        if isinstance(i, (tuple, list)):
            items.extend(zip(i, [prob_dict[i]] * len(i)))
        else:
            items.append((i, prob_dict[i]))
    values = list(map(lambda x: x[1], items))
    summa = sum(values)
    small_ranges = []
    for i in range(len(values)):
        if i == 0:
            first = 0
        else:
            first = small_ranges[-1][-1]
        second = sum(values[: i + 1])
        small_ranges.append([first, second])

    random_number = randint(0, summa)
    items_ranges = zip(items, small_ranges)
    # zip element: ((key, value), [rmin, rmax])
    answer = filter(lambda x: x[-1][0] <= random_number <= x[-1][1],
                    items_ranges)

    unpacked = list(answer)[0]
    result = unpacked[0][0]
    return result


class StructureLoader:
    def __init__(self, short_path):
        # Hydrate part
        is_it_hydrate = smart_choice({True: 10, False: 90})
        if is_it_hydrate:
            has_it_whole_index = smart_choice({True: 90, False: 10})
            if has_it_whole_index:
                self.aqua = smart_choice({1: 30, 2: 30, 3: 30, 5: 5, 4: 5})
            else:
                self.aqua = smart_choice({(1, 2): 1, (3, 2): 1, (2, 5): 1})
        else:
            self.aqua = ''

        # Unit part
        is_it_mass_or_volume = smart_choice({"mass": 70, "volume": 30})
        if is_it_mass_or_volume == "mass":
            self.quantity_unit = smart_choice({kilogram: 10,
                                               milligram: 10,
                                               gram: 80})
        elif is_it_mass_or_volume == "volume":
            self.quantity_unit = smart_choice({liter: 10, milliliter: 90})

        # Quantity part
        if self.quantity_unit in [gram, milligram, milliliter]:
            self.quantity = float(choice([100, 200, 300, 400, 500,
                                          600, 700, 800, 900]))
        else:
            self.quantity = choice([1.0, 2.0, 1.5, 0.5])

        # Name part
        self.name = make_name()

        # Storage place part
        self.storage_place = choose_storage_place()

        # created_by and updated_by part
        who_created_and_updated = choice([billie_eilish,
                                          darth_vader,
                                          oleg_gazmanov])
        self.created_by = who_created_and_updated
        self.updated_by = who_created_and_updated

        # structure block
        self.loaded_structure = LazyMol(short_path)
        with open(short_path, "rt", encoding="utf-8") as file:
            mol_block_text = file.read()
            self.mol_block = mol_block_text.strip()
        self.molecular_formula = self.loaded_structure.molecular_formula
        self.inchi = self.loaded_structure.inchi
        structure_dict = {"inchi": self.inchi}
        if self.aqua:
            structure_dict["aq"] = self.aqua
        self.structure = structure_dict
        self.molar_mass = self.loaded_structure.molar_weight

    def create_summary(self):
        fields_dict = {'name': self.name,
                       'structure': self.structure,
                       'mol_block': self.mol_block,
                       'molecular_formula': self.molecular_formula,
                       'molar_mass': self.molar_mass,
                       'storage_place': self.storage_place,
                       'quantity': self.quantity,
                       'quantity_unit': self.quantity_unit,
                       'who_created': self.created_by}
        return fields_dict


counter = 0
for i in normal_files:
    loader = StructureLoader(i)
    summary_for_chemical_creation = loader.create_summary()
    Chemical.create(summary_for_chemical_creation,
                    loader.loaded_structure.elements_dict())
    counter += 1
    if counter % 100 == 0:
        print(counter, " loaded")
