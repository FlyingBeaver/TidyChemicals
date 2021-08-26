from shutil import move
from base_app.mol_classes import LazyMol
from simple_base_project.settings import NOTATION_FOR_RENDERING


PICS_DIRECTORY_PATH = "./base_app/static/base_app/"


class RenderingError(BaseException):
    pass
        

def render_pics(found_records):
    result = []
    for record in found_records:
        if NOTATION_FOR_RENDERING == "inchi":
            substance = record["structure_container"]
        elif NOTATION_FOR_RENDERING == "mol":
            substance = LazyMol(record["structure_container"], "mol", False)
        else:
            raise RenderingError("Unknown NOTATION_FOR_RENDERING value")
        substance.save_to_picture(filename=str(record["id"]) + ".svg", 
                                  file_type="svg")
        move(f'./{str(record["id"])}.svg', PICS_DIRECTORY_PATH)
        result.append(str(record["id"]) + '.svg')
    return result

# Было бы здорово, если бы она ещё проверяла, какие 
# структуры уже есть
