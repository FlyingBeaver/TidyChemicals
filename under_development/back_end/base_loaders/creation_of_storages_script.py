from base_app.models import StoragePlace


def load_storages():
    root = StoragePlace.make_root(root_name="root")
    # root = StoragePlace.objects.get(level=0)

    a = StoragePlace.create("Лаб. 416", root, False)
    a.save()

    b = StoragePlace.create("Шкаф 1", a, False)
    b.save()

    c = StoragePlace.create("Полка 1", b, True)
    c.save()

    d = StoragePlace.create("Полка 2", b, True)
    d.save()

    e = StoragePlace.create("Полка 3", b, True)
    e.save()

    f = StoragePlace.create("Шкаф 2", a, False)
    f.save()

    g = StoragePlace.create("Верхняя полка", f, True)
    g.save()

    h = StoragePlace.create("Средняя полка", f, True)
    h.save()

    i = StoragePlace.create("Нижняя полка", f, True)
    i.save()

    j = StoragePlace.create("Холодильник", a, False)
    j.save()

    k = StoragePlace.create("Верхняя полка", j, True)
    k.save()

    l = StoragePlace.create("Нижняя полка", j, True)
    l.save()

    m = StoragePlace.create("Дверь", j, True)
    m.save()

    n = StoragePlace.create("Лаб. 401", root, False)
    n.save()

    o = StoragePlace.create("Шкаф", n, False)
    o.save()

    p = StoragePlace.create("Коробка 1", o, True)
    p.save()

    q = StoragePlace.create("Коробка 2", o, True)
    q.save()

    r = StoragePlace.create("Верхняя полка", o, True)
    r.save()

    s = StoragePlace.create("Холодильник", n, False)
    s.save()

    t = StoragePlace.create("Верхняя полка", s, True)
    t.save()

    u = StoragePlace.create("Нижняя полка", s, True)
    u.save()

    v = StoragePlace.create("Шуфлядка", s, True)
    v.save()

    w = StoragePlace.create("Сейф", n, True)
    w.save()

    x = StoragePlace.create("Лаб. 425", root, False)
    x.save()

    y = StoragePlace.create("Шкаф 1", x, True)
    y.save()

    z = StoragePlace.create("Полка 1", y, True)
    z.save()

    aa = StoragePlace.create("Полка 2", y, True)
    aa.save()

    ab = StoragePlace.create("Полка 3", y, True)
    ab.save()

    ac = StoragePlace.create("Холодильник 1", x, False)
    ac.save()

    ad = StoragePlace.create("Полка 1", ac, True)
    ad.save()

    ae = StoragePlace.create("Полка 2", ac, True)
    ae.save()

    af = StoragePlace.create("Холодильник 2", x, False)
    af.save()

    ag = StoragePlace.create("Верхняя полка", af, True)
    ag.save()

    ah = StoragePlace.create("Средняя полка", af, True)
    ah.save()

    ai = StoragePlace.create("Нижняя полка", af, True)
    ai.save()
