import json
from base_app.models import Chemical, StructElementRel


# Этот скрипт будет
# сгружать все реактивы из базы в json
# Кроме этого, будет скрипт, который читает
# этот json и восстанавливает базу


def create_json():
    all_chemicals = Chemical.objects.all()
    all_data = []

    for chemical in all_chemicals:
        chem_dict = dict()
        chem_dict["name"] = chemical.name # это строка
        chem_dict["structure"] = chemical.structure # это словарь
        chem_dict["mol_block"] = chemical.mol_block # и это строка
        chem_dict["molecular_formula"] = chemical.molecular_formula # тоже строка
        chem_dict["molar_mass"] = chemical.molar_mass
        chem_dict["storage_place"] = chemical.storage_place.path_str
        chem_dict["quantity"] = chemical.quantity
        chem_dict["quantity_unit"] = chemical.quantity_unit.unit_symbol
        chem_dict["who_created"] = chemical.who_created.user.username
        
        ser_queryset = StructElementRel.objects.filter(chemical=chemical) \
            .select_related('element')
        elements_dict = dict()
        for ser in ser_queryset:
            elements_dict[ser.element.symbol] = ser.index
        chem_dict["elements_dict"] = elements_dict
        all_data.append(chem_dict)


    json_string = json.dumps(all_data, sort_keys=True, indent=4)
    with open("dump_001.json", "wt", encoding="utf-8") as file:
        file.write(json_string)


# fields_dict = {'name': self.name,
#                'structure': self.structure,
#                'mol_block': self.mol_block,
#                'molecular_formula': self.molecular_formula,
#                'molar_mass': self.molar_mass,
#                'storage_place': self.storage_place,
#                'quantity': self.quantity,
#                'quantity_unit': self.quantity_unit,
#                'who_created': self.created_by}