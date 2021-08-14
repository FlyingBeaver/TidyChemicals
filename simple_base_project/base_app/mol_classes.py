'''
Created on 29.07.2021

@author: Александр
Есть два варианта:
    1) Сделать класс молекулы, где в экземплярах уже будут все
    основные представления структуры записаны в 
    качестве свойств. Но тогда если что-то не понравится 
    сишному коду (при том что это ещё не значит, что структура
    невалидна), то выскочит исключение при инстанцировании.
    
    2) Сделать молекулу, где представления будут записаны 
    в виде геттеров и, соответственно, будут генерироваться
    динамически. Однако потом исключения могут возникнуть в
    самый неподходящий момент.
    
Скорее всего нужно делать оба. Допустим, один будет 
называться MyMol, а второй LazyMol
'''


from collections import OrderedDict
from re import fullmatch, search, findall, ASCII

from rdkit.Chem import MolFromSmiles
from rdkit.Chem import MolToSmiles
from rdkit.Chem import MolFromMolFile
from rdkit.Chem import MolToMolBlock
from rdkit.Chem.Descriptors import MolWt
from rdkit.Chem.Draw import MolToFile
from rdkit.Chem.inchi import MolToInchi
from rdkit.Chem.inchi import MolToInchiKey
from rdkit.Chem.inchi import MolFromInchi
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdMolDescriptors import CalcMolFormula
from rdkit.Chem.rdmolfiles import MolFromPDBBlock
from rdkit.Chem.rdmolfiles import MolFromPDBFile
from rdkit.Chem.rdmolfiles import MolFromMolBlock
from rdkit.Chem.rdmolfiles import MolToMolFile
from rdkit.Chem.rdmolfiles import MolToPDBFile
from rdkit.Chem.rdmolfiles import MolToPDBBlock



class MyMolError(BaseException):
    pass


class LazyMol(object):
    '''
    Клас, который призван облегчить
    работу с химическими структурами, чтобы не обязательно было
    запоминать функции РДКИТа

    Экземпляр класса -- объект, содержащий в себе объект типа
    rdkit.Chem.rdchem.Mol, который при инстанцировании передаётся
    конструктору или создаётся конструктором конвертированием строки
    со smiles, inchi, mol block, pdb block, или содержащей путь к файлу
    типа .mol или .pdb
    '''
    # SMILES_RE is a regular expression that checks
    # potential smiles string. re.fullmatch() matches if
    # all symbols in evaluated string can be in smiles
    SMILES_RE = r"[-A-Za-z0-9=#:@[\]+()/\\$.]+"
    TYPE_ERROR_MSG = ("Type of a 'structure' argument must be "
                      "'rdkit.Chem.rdchem.Mol' or str, but it's {}")
    WRONG_FORM_VALUE = ("Unknown 'form' value: {}. It says what kind of "
                        "text data 'structure' variable contains and must be "
                        "one of these: 'mol', 'pdb', 'inchi', 'smiles'. For "
                        "paths to files they are not required")
    STRING_VALUE_ERROR_MSG = ("Invalid 'structure' value. If string '{}' "
                              "supposed to be smiles, it most likely to be "
                              "caused by some issues with it's validity, but "
                              "for some valid representations (like C#O, not "
                              "CO) cause aren't recognized as valid because "
                              "of some rdkit bugs")

    FUNCS_TO = {"smiles": MolToSmiles,
                "inchi": MolToInchi,
                "inchikey": MolToInchiKey,
                "mol_file": MolToMolFile,
                "mol_block": MolToMolBlock,
                "pdb_file": MolToPDBFile,
                "pdb_block": MolToPDBBlock}

    FUNCS_FROM = {"smiles": MolFromSmiles,
                  "inchi": MolFromInchi,
                  "mol_file": MolFromMolFile,
                  "mol_block": MolFromMolBlock,
                  "pdb_file": MolFromPDBFile,
                  "pdb_block": MolFromPDBBlock}

    def __init__(self, structure, form:(None, str)=None):
        self._rdmol = None
        self.molecular_formula = None
        self.molar_weight = None
        self._charge = None
        self._inchi = None
        self._inchikey = None
        self._smiles = None
        self._mol_block = None
        self._pdb_block = None
        self.source_file_path = None
        self._image_path = None
        self._elements_list = None
        self._elements_dict = None

        if isinstance(structure, Mol):
            self.process_rdmol(structure)
        elif not isinstance(structure, str):
            arg_type = str(type(structure))
            message = self.TYPE_ERROR_MSG.format(arg_type)
            raise TypeError(message)
        elif form:
            self.process_block(structure, form)
        else:
            self.process_path_or_strrepr(structure)
        
    def process_rdmol(self, structure: Mol):
        if structure is None:
            msg = "Mol object is None. Looks like convertion error happened"
            raise MyMolError(msg)
        self._rdmol = structure
        self.molecular_formula = CalcMolFormula(structure)
        self.molar_weight = MolWt(structure)
        
    def process_block(self, structure: str, form: str):
        if form.lower() in ('mol', 'pdb'):
            self.make_rdmol(structure, form.lower() + "_block")
        elif form.lower() in ('smiles', 'inchi'):
            self.make_rdmol(structure, form.lower())
        else:
            msg = self.WRONG_FORM_VALUE.format(form)
            raise ValueError(msg)

    def process_path_or_strrepr(self, structure: str):
        if structure.lower().startswith("inchi="):
            rdmol = self.make_rdmol(structure, "inchi")
        elif structure.lower().endswith(".mol"):
            self.source_file_path = structure
            rdmol = self.make_rdmol(structure, "mol_file")
        elif structure.lower().endswith(".pdb"):
            rdmol = self.make_rdmol(structure, "pdb_file")
        # The check if it can be smiles:
        elif bool(fullmatch(self.SMILES_RE, structure)):
            # and if it is valid smiles (according to rdkit):
            rdmol = self.make_rdmol(structure, 'smiles')
            if rdmol is None:
                msg = self.STRING_VALUE_ERROR_MSG.format(structure)
                raise ValueError(msg)
        else:
            raise ValueError("Data format not recognized")
        self.process_rdmol(rdmol)

    def make_rdmol(self, structure, key: str):
        return self.FUNCS_FROM[key](structure)

    def convert_to(self, key: str):
        return self.FUNCS_TO[key](self._rdmol)

    @property
    def smiles(self):
        self._smiles = self.convert_to('smiles')
        return self._smiles

    @property
    def inchi(self):
        self._inchi = self.convert_to('inchi')
        return self._inchi

    @property
    def molblock(self):
        self._mol_block = self.convert_to('mol_block')
        return self._mol_block

    @property
    def pdbblock(self):
        self._pdb_block = self.convert_to('pdb_block')
        return self._pdb_block

    @property
    def inchikey(self):
        self._inchikey = self.convert_to('inchikey')
        return self._inchikey

    def save_to_mol(self, path: str):
        if not path.lower().endswith('.mol'):
            path += '.mol'
        self.FUNCS_TO['mol_file'](path)

    def save_to_pdb(self, path: str):
        if not path.lower().endswith('.pdb'):
            path += '.pdb'
        self.FUNCS_TO['mol_pdb'](path)

    def save_to_picture(self, filename, file_type=None,
                        size: tuple = (300, 300),
                        kekulize=True,
                        wedge_bonds=True,
                        fit_image=False,
                        options=None, **kwargs):
        """
        Wrapper for rdkit function MolToFile
        MolToFile can save only to pdf, svg, ps, and png
        """
        MolToFile(self._rdmol, filename, size=size, kekulize=kekulize,
                  wedgeBonds=wedge_bonds, imageType=file_type,
                  fitImage=fit_image, options=options, **kwargs)
        self._image_path = filename

    def __contains__(self, element_symbol):
        return element_symbol in self.molecular_formula

    @property
    def charge(self):
        formula = self.molecular_formula
        # r"[+-]\d*" is for example to cut '-2' from 'HPO4-2'
        match = search(r"[+-]\d*", formula, ASCII)
        if match:
            self._charge = int(match[0])
        else:
            self._charge = 0
        return self._charge

    @property
    def elements_list(self):
        formula = self.molecular_formula
        # for example 'C9H21SiCl- -> ['C', 'H', 'Si', 'Cl']
        self._elements_list = findall(r"[A-Z][a-z]?", formula)
        return self._elements_list

    @property
    def elements_dict(self, template: list = None):
        """
        In case of template != None
            template is a list of element symbols, which defines
            order of elements in OrderedDict returned.
        If template have some elements which the structure doesn't
            contain, they are just ignored.
        If the structure have some elements which template doesn't
            contain, they appear in OrderedDict after those in template.
        If template is None, method returns usual dict
        """
        dictionary = dict()
        formula = self.molecular_formula
        symbols = self.elements_list

        for i in symbols:
            # re searching for a number after string i
            match = search(r"(?<=%s)+\d+" % i, formula, ASCII)
            dictionary[i] = (1 if not match else int(match[0]))

        if template:
            template_odict = OrderedDict(zip(template, [0]*len(template)))
            raw_odict = template_odict | OrderedDict(dictionary)
            result = OrderedDict(filter(lambda x: x[1], raw_odict.items()))
            return result
        else:
            return dictionary

    def __mod__(self, other):
        """Check for presence of substructure in structure.
        The order is:
        STRUCTURE % SUBSTRUCTURE,
        not vice versa!"""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Second arg has wrong type: "
                            f"{other.__class__}, must be LazyMol")
        super_rdmol = self._rdmol
        sub_rdmol = other._rdmol
        return super_rdmol.HasSubstructMatch(sub_rdmol)


# class BuzyMol(LazyMol):
#     def __init__(self, *args, **kwargs):
#         super().__init__(self, *args, **kwargs)
#         properties_to_calc = [self.charge,
#                               self.inchi,
#                               self.inchikey,
#                               self.smiles,
#                               self.molblock,
#                               self.pdbblock,
#                               self.elements_list,
#                               self.elements_dict]
#         for i in properties_to_calc:
#             i()
#
#     @staticmethod
#     def if_already_calculated_just_return(method):
#         method_and_attribute = {super().smiles: '_smiles',
#                                 super().inchi: '_inchi',
#                                 super().molblock: '_mol_block',
#                                 super().pdbblock: '_pdb_block',
#                                 super().inchikey: '_inchikey',
#                                 super().charge: '_charge'}
#
#         def wrapper(self, recalc=False):
#             if recalc or not getattr(self, method_and_attribute[method]):
#                 attr_value = self.method()
#                 setattr(self,
#                         method_and_attribute[method],
#                         attr_value)
#                 return attr_value
#             else:
#                 return getattr(self, method_and_attribute[method])
#         return wrapper
#
#     @if_already_calculated_just_return
#     def smiles(self, *args, **kwargs):
#         super().smiles(self, *args, **kwargs)
#
#     @if_already_calculated_just_return
#     def inchi(self, *args, **kwargs):
#         super().inchi(self, *args, **kwargs)
#
#     @if_already_calculated_just_return
#     def molblock(self, *args, **kwargs):
#         super().molblock(self, *args, **kwargs)
#
#     @if_already_calculated_just_return
#     def pdbblock(self, *args, **kwargs):
#         super().pdbblock(self, *args, **kwargs)
#
#     @if_already_calculated_just_return
#     def inchikey(self, *args, **kwargs):
#         super().inchikey(self, *args, **kwargs)
#
#     @if_already_calculated_just_return
#     def charge(self, *args, **kwargs):
#         super().charge
#
#     @if_already_calculated_just_return
#     def elements_list(self, *args, **kwargs):
#         super().elements_list(self, *args, **kwargs)
