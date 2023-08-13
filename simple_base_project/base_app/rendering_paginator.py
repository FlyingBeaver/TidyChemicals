from os.path import isfile
from os import listdir, remove
from time import time
from rdkit.Chem.inchi import InchiToInchiKey
from django.core.cache import cache
from django.core.paginator import Paginator, Page
from uuid import uuid4
from shutil import move
from simple_base_project.settings import NOTATION_FOR_RENDERING
from base_app.mol_classes import LazyMol


PICS_DIRECTORY_PATH = "./base_app/static/base_app/structures/"
SVG_EXP_TIME_IN_HOURS = 24


def create_svg(lazy_mol, chemical, size=300):
    if lazy_mol is None:
        lazy_mol = LazyMol(chemical.mol_block, "mol")
    inchi = chemical.structure["inchi"]
    inchiKey = InchiToInchiKey(inchi)
    file_name = inchiKey + "-" + str(size) + ".svg"
    full_path = PICS_DIRECTORY_PATH + file_name
    files_dict = cache.get("files_dict", "expired")
    if files_dict == "expired":
        if isfile(full_path):
            files_list = listdir(PICS_DIRECTORY_PATH)
            files_list.remove(file_name)
            for file_to_delete in files_list:
                remove(PICS_DIRECTORY_PATH + file_to_delete)
        else:
            files_list = listdir(PICS_DIRECTORY_PATH)
            for file_to_delete in files_list:
                remove(PICS_DIRECTORY_PATH + file_to_delete)
            lazy_mol.save_to_picture(filename=full_path,
                                     file_type="svg",
                                     size=(size, size))
        expiration_time = int(time()) + SVG_EXP_TIME_IN_HOURS * 3600
        new_files_dict = {file_name: expiration_time}
        cache.set("files_dict",
                  new_files_dict,
                  SVG_EXP_TIME_IN_HOURS * 3600)

    else:
        current_time = int(time())
        if file_name not in files_dict:
            lazy_mol.save_to_picture(filename=full_path,
                                     file_type="svg",
                                     size=(size, size))
        files_dict[file_name] = current_time + SVG_EXP_TIME_IN_HOURS * 3600
        keys_to_delete = []
        for file, expiration_time in files_dict.items():
            if expiration_time < current_time:
                keys_to_delete.append(file)
                remove(PICS_DIRECTORY_PATH + file)
        for key in keys_to_delete:
            del files_dict[key]
        cache.set("files_dict", files_dict, SVG_EXP_TIME_IN_HOURS * 3600)
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

        if type(original_page[0]) == dict:
            for item in original_page:
                chemical = item["chemical"]
                new_object_list.append(chemical)
                lazy_mol = item["lazymol"]
                # create_and_move_file(lazy_mol, filenames)
                filenames.append(create_svg(lazy_mol, chemical))
            rendering_page = RenderingPage(new_object_list,
                                           number,
                                           self,
                                           filenames)
            return rendering_page

        elif NOTATION_FOR_RENDERING == "mol":
            for item in original_page:
                mol_block = item.mol_block
                lazy_mol = LazyMol(mol_block, "mol")
                # create_and_move_file(lazy_mol, filenames)
                filenames.append(create_svg(lazy_mol, item))
            rendering_page = RenderingPage(original_page.object_list,
                                           number,
                                           self,
                                           filenames)
            return rendering_page

        elif NOTATION_FOR_RENDERING == "inchi":
            for item in original_page:
                inchi = item.structure["inchi"]
                lazy_mol = LazyMol(inchi, "inchi")
                # create_and_move_file(lazy_mol, filenames)
                filenames.append(create_svg(lazy_mol, item))
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
