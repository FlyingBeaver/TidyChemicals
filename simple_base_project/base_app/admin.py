from django.contrib import admin
from base_app.models import *


class ChemicalAdmin(admin.ModelAdmin):
	list_display = ("id",
		            "name", 
		            "molecular_formula",
		            "molar_mass",
		            "storage_place",
		            "quantity",
		            "quantity_unit")


class ElementAdmin(admin.ModelAdmin):
	list_display = ("z", 
		            "name", 
		            "symbol", 
		            "atomic_weight")


class ElementAbundanceAdmin(admin.ModelAdmin):
	list_display = ("element", "n_of_chemicals")


class StructElementRelAdmin(admin.ModelAdmin):
	list_display = ("element",
		            "chemical",
		            "index")


class StoragePlaceAdmin(admin.ModelAdmin):
	list_display = ("id", 
		            "name", 
		            "level", 
		            "parent", 
		            "terminal", 
		            "path_str")


class QuantityUnitAdmin(admin.ModelAdmin):
	list_display = ("name", 
		            "unit_symbol",
		            "measure_type")


admin.site.register(Chemical, ChemicalAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(ElementAbundance, 
	                ElementAbundanceAdmin)
admin.site.register(StructElementRel, 
	                StructElementRelAdmin)
admin.site.register(StoragePlace, 
	                StoragePlaceAdmin)
admin.site.register(QuantityUnit,
	                QuantityUnitAdmin)

