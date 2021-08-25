import shutil
from base_app.mol_classes import LazyMol


PICS_DIRECTORY_PATH = "./static/base_app/"


def render_pics(found_records):
    result = []
    for record in found_records:
        substance = LazyMol(record["mol_block"], "mol", False)
        substance.save_to_picture(filename=record["uuid"] + ".svg", file_type="svg")
        shutil.move(f'./{record["uuid"]}.svg', PICS_DIRECTORY_PATH)
        result.append(record["uuid"] + '.svg')
    return result
