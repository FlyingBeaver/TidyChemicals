# Лучше всего сделать такую структуру:
# Иерархия пусть хранится в словаре, состоящем из айдишников,
# а названия хранилищ и терминальное/нетерминальное/реактив 
# пусть в отдельном словаре


def children_of(parent_id):
    response_body = []
    is_terminal = None
    parent_type = storages[parent_id]["type"]
    
    if parent_type == 0:
        is_terminal = False
    elif parent_type == 1:
        is_terminal = True
    else:
        raise ValueError()

    if is_terminal:
        children_dict = parent_children_with_dicts[parent_id]
        for child_id in children_dict:
            child_dict = children_dict[child_id]
            child_dict["id"] = child_id
            response_body.append(child_dict)
    else:
        children_list = parent_children_with_dicts[parent_id]
        for child_id in children_list:
            child_dict = storages[child_id]
            child_dict["id"] = child_id
            response_body.append(child_dict)
    return response_body


def path_to_chemical(chemical_id):
    if chemical_id < 10 or chemical_id > 29:
        raise ValueError("Chemical with such id does not exist")
    else:
        node_id = chemical_id
        path_list = []
        while node_id != 0:
            for i in parent_children:
                if node_id in parent_children[i]:
                    path_list.append(i)
                    node_id = i
                    break
        path_list.reverse()
        return path_list


def path_children(chemical_id):
    children = {}
    path_list = path_to_chemical(chemical_id)
    for storage_id in path_list:
        print(storage_id)
        children[storage_id] = children_of(storage_id)
    return {"full_path": path_list, "children": children}





content3 = {
    10: {"name": "Хлорид кальция", "type": 2},
    11: {"name": "Хлорид натрия", "type": 2},
    12: {"name": "Хлорид калия", "type": 2}
}
content4 = {
    13: {"name": "Сульфат натрия", "type": 2},
    14: {"name": "Сульфат меди пятиводный", "type": 2}
}
content5 = {
    15: {"name": "Триэтиламин", "type": 2},
    16: {"name": "Бутиллитий", "type": 2},
    17: {"name": "Диизопропиламин", "type": 2},
}
content6 = {
    18: {"name": "Оксид хрома", "type": 2},
    19: {"name": "Оксид фосфора (V)", "type": 2},
    20: {"name": "Хлорид никеля", "type": 2}
}
content7 = {
    21: {"name": "Сульфат железа (II)", "type": 2},
    22: {"name": "Цитрат натрия", "type": 2},
    23: {"name": "Хлорид аммония", "type": 2}
}
content8 = {
    24: {"name": "Сульфат натрия", "type": 2},
    25: {"name": "Хлорид натрия", "type": 2},
    26: {"name": "Бихромат натрия", "type": 2},
}
content9 = {
    27: {"name": "Ацетоуксусный эфир", "type": 2},
    28: {"name": "Диэтилфталат", "type": 2},
    29: {"name": "tret-Butyldimethylsilyl chloride", "type": 2}
}


hierarchy = {
    0: {
        1: {
            3: content3,
            4: content4,
            5: content5,
        },
        2: {
            6: content6,
            7: content7,
            8: content8,
            9: content9,
        }
    }
}

parent_children = {
                   0: [1, 2],
                   1: [3, 4, 5],
                   2: [6, 7, 8, 9],
                   3: list(content3.keys()),
                   4: list(content4.keys()),
                   5: list(content5.keys()),
                   6: list(content6.keys()),
                   7: list(content7.keys()),
                   8: list(content8.keys()),
                   9: list(content9.keys()),
                   }

parent_children_with_dicts = {
                   0: [1, 2],
                   1: [3, 4, 5],
                   2: [6, 7, 8, 9],
                   3: content3,
                   4: content4,
                   5: content5,
                   6: content6,
                   7: content7,
                   8: content8,
                   9: content9,
                   }


# Пусть шкафы будут без полок
# тип 0 -- нетерминальное хранилище
# тип 1 -- терминальное хранилище
# тип 2 -- реактив
storages = {
    0: {"name": "root", "type": 0},
    1: {"name": "Лаборатория 1", "type": 0},
    2: {"name": "Лаборатория 2", "type": 0},
    3: {"name": "Шкаф 1", "type": 1},
    4: {"name": "Шкаф 2", "type": 1},
    5: {"name": "Холодильник", "type": 1},
    6: {"name": "Шкаф 1", "type": 1},
    7: {"name": "Шкаф 2", "type": 1},
    8: {"name": "Шкаф 3", "type": 1},
    9: {"name": "Холодильник", "type": 1},
}

