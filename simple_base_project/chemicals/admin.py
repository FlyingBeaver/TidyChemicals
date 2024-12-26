from django.contrib import admin
from chemicals.models import *


class ChemicalAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "name", 
                    "molecular_formula",
                    "molar_mass",
                    "storage_place",
                    "quantity",
                    "quantity_unit",
                    "taken_by")


class ElementAdmin(admin.ModelAdmin):
    list_display = ("z", 
                    "name", 
                    "symbol", 
                    "atomic_weight",
                    "n_of_chemicals")


class PathAdmin(admin.ModelAdmin):
    list_display = ("label",
                    "n_of_chemicals")


class RingAdmin(admin.ModelAdmin):
    list_display = ("label",
                    "n_of_chemicals")


class Chemical_ElementAdmin(admin.ModelAdmin):
    list_display = ("element",
                    "chemical",
                    "n_of_occurrences")


class Chemical_PathAdmin(admin.ModelAdmin):
    list_display = ("path",
                    "chemical",
                    "n_of_occurrences")


class Chemical_RingAdmin(admin.ModelAdmin):
    list_display = ("ring",
                    "chemical",
                    "n_of_occurrences")


class StoragePlaceAdmin(admin.ModelAdmin):
    list_display = ("id", 
                    "name", 
                    "level", 
                    "parent", 
                    "contains_chemicals", 
                    "path_str")


class QuantityUnitAdmin(admin.ModelAdmin):
    list_display = ("unit_symbol",
                    "name", 
                    "measure_type",
                    "relation_to_basic")


admin.site.register(Chemical, ChemicalAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(Path, PathAdmin)
admin.site.register(Ring, RingAdmin)
admin.site.register(Chemical_Element, 
                    Chemical_ElementAdmin)
admin.site.register(Chemical_Path, 
                    Chemical_PathAdmin)
admin.site.register(Chemical_Ring, 
                    Chemical_RingAdmin)
admin.site.register(StoragePlace, 
                    StoragePlaceAdmin)
admin.site.register(QuantityUnit,
                    QuantityUnitAdmin)

