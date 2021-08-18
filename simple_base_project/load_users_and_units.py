import random
from profiles.models import Profile
from base_app.models import QuantityUnit, StoragePlace


STORAGE_PLACES = list(StoragePlace.objects.filter(terminal=True))


def find_user_by_name(name: str):
    return Profile.objects.get(user__username=name)


def find_unit_by_symbol(symbol: str):
    return QuantityUnit.objects.get(unit__symbol=symbol)


def choose_storage_place():
    return random.choice(STORAGE_PLACES)


darth_vader = find_user_by_name("DarthVader")
oleg_gazmanov = find_user_by_name("OlegGazmanov")
billie_eilish = find_user_by_name("BillieEilish")

milliliter = find_unit_by_symbol("ml")
milligram = find_unit_by_symbol('mg')
liter = find_unit_by_symbol('l')
gram = find_unit_by_symbol('g')
kilogram = find_unit_by_symbol('kg')
