from os.path import isfile
from os import listdir, remove
from time import time
from uuid import uuid4
from shutil import move

from rdkit.Chem.inchi import InchiToInchiKey
from rdkit.Chem.Draw import _moltoSVG
from django.core.cache import cache
from django.core.paginator import Paginator, Page

from chemicals.services.mol_classes import LazyMol


PICS_DIRECTORY_PATH = 'chemicals-images/'
SVG_EXP_TIME_IN_HOURS = 24


def create_svg_alt(lazy_mol, chemical, size=300):
    if lazy_mol is None:
        lazy_mol = LazyMol(chemical.mol_block, "mol")
    file_name = str(size) + "-" + str(hash(chemical.mol_block)) + ".svg"
    name_from_cache = cache.get(file_name, "no name in cache")
    
    if name_from_cache == "no name in cache":
        svg_code = _moltoSVG(lazy_mol._rdmol, (size, size), [], "", True)
        cache.set(file_name,
                  svg_code,
                  SVG_EXP_TIME_IN_HOURS * 3600)
    return file_name


def create_and_move_file(lazy_mol, filenames):
    name = str(uuid4()) + ".svg"
    lazy_mol.save_to_picture(filename=name,
                             file_type="svg")
    move("./" + name, PICS_DIRECTORY_PATH)
    filenames.append(name)


class RenderingPaginator(Paginator):
    """This is paginator that renders 
    structures on a page it returns"""
    def page(self, number):
        original_page = super().page(number)
        new_object_list = list()
        filenames = []
        if len(original_page) == 0:
            rendering_page = RenderingPage([], number, self, [])
            return rendering_page

        # если original_page наполнен словарями
        if type(original_page[0]) == dict:
            for item in original_page:
                chemical = item["chemical"]
                new_object_list.append(chemical)
                lazy_mol = item["lazymol"]
                # create_and_move_file(lazy_mol, filenames)
                filenames.append(create_svg_alt(lazy_mol, chemical))
            rendering_page = RenderingPage(new_object_list,
                                           number,
                                           self,
                                           filenames)
            return rendering_page

        # иначе original_page -- фрагмент кверисета
        else:
            for item in original_page:
                mol_block = item.mol_block
                lazy_mol = LazyMol(mol_block, "mol")
                # create_and_move_file(lazy_mol, filenames)
                filenames.append(create_svg_alt(lazy_mol, item))
            rendering_page = RenderingPage(original_page.object_list,
                                           number,
                                           self,
                                           filenames)
            return rendering_page


class RenderingPage(Page):
    def __init__(self, object_list, number, paginator, filenames):
        self.filenames = filenames
        super().__init__(object_list, number, paginator)

    def filename_item(self):
        items_list = self.object_list
        return zip(self.filenames, items_list)
