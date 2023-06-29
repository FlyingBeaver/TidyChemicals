from django.core.paginator import Paginator, Page
from uuid import uuid4
from shutil import move
from simple_base_project.settings import NOTATION_FOR_RENDERING
from base_app.mol_classes import LazyMol


PICS_DIRECTORY_PATH = "./base_app/static/base_app/"


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
        if type(original_page[0]) == dict:
            for item in original_page:
                new_object_list.append(item["chemical"])
                lazy_mol = item["lazymol"]
                create_and_move_file(lazy_mol, filenames)
            rendering_page = RenderingPage(new_object_list,
                                           number,
                                           self,
                                           filenames)
            return rendering_page

        elif NOTATION_FOR_RENDERING == "mol":
            for item in original_page:
                mol_block = item.mol_block
                lazy_mol = LazyMol(mol_block, "mol")
                create_and_move_file(lazy_mol, filenames)
            rendering_page = RenderingPage(original_page.object_list,
                                           number,
                                           self,
                                           filenames)
            return rendering_page

        elif NOTATION_FOR_RENDERING == "inchi":
            for item in original_page:
                inchi = item.structure["inchi"]
                lazy_mol = LazyMol(inchi, "inchi")
                create_and_move_file(lazy_mol, filenames)
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
