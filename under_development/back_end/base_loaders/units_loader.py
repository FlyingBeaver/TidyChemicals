from base_app.models import QuantityUnit


def load_units():
    kilogram = QuantityUnit.objects.create(name="kilogram",
                                           unit_symbol="kg",
                                           measure_type="mass",
                                           relation_to_basic=D(1))
    kilogram.save()
    gram = QuantityUnit.objects.create(name="gram",
                                       unit_symbol="g",
                                       measure_type="mass",
                                       relation_to_basic=D(0.001))
    gram.save()
    milligram = QuantityUnit.objects.create(name="milligram",
                                            unit_symbol="mg",
                                            measure_type="mass",
                                            relation_to_basic=D(0.000001))
    milligram.save()
    liter = QuantityUnit.objects.create(name="liter",
                                        unit_symbol="l",
                                        measure_type="volume",
                                        relation_to_basic=D(1))
    liter.save()
    milliliter = QuantityUnit.objects.create(name="milliliter",
                                             unit_symbol="ml",
                                             measure_type="volume",
                                             relation_to_basic=D(0.001))
    milliliter.save()
    kilogram = QuantityUnit.objects.create(name="kilogram",
                                           unit_symbol="kg",
                                           measure_type="mass",
                                           relation_to_basic=D(1))
    kilogram.save()
    gram = QuantityUnit.objects.create(name="gram",
                                       unit_symbol="g",
                                       measure_type="mass",
                                       relation_to_basic=D(0.001))
    gram.save()
    milligram = QuantityUnit.objects.create(name="milligram",
                                            unit_symbol="mg",
                                            measure_type="mass",
                                            relation_to_basic=D(0.000001))
    milligram.save()
    liter = QuantityUnit.objects.create(name="liter",
                                        unit_symbol="l",
                                        measure_type="volume",
                                        relation_to_basic=D(1))
    liter.save()
    milliliter = QuantityUnit.objects.create(name="milliliter",
                                             unit_symbol="ml",
                                             measure_type="volume",
                                             relation_to_basic=D(0.001))
    milliliter.save()
    kilogram = QuantityUnit.objects.create(name="kilogram",
                                           unit_symbol="kg",
                                           measure_type="mass",
                                           relation_to_basic=D(1))
    kilogram.save()
    gram = QuantityUnit.objects.create(name="gram",
                                       unit_symbol="g",
                                       measure_type="mass",
                                       relation_to_basic=D(0.001))
    gram.save()
    milligram = QuantityUnit.objects.create(name="milligram",
                                            unit_symbol="mg",
                                            measure_type="mass",
                                            relation_to_basic=D(0.000001))
    milligram.save()
    liter = QuantityUnit.objects.create(name="liter",
                                        unit_symbol="l",
                                        measure_type="volume",
                                        relation_to_basic=D(1))
    liter.save()
    milliliter = QuantityUnit.objects.create(name="milliliter",
                                             unit_symbol="ml",
                                             measure_type="volume",
                                             relation_to_basic=D(0.001))
    milliliter.save()
