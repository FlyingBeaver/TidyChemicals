from collections import namedtuple
from treelib import Tree
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdchem import Atom
from rdkit.Chem import MolFromSmiles


MAX_DEPTH = 7
BOND_SYMBOLS = {"SINGLE": "-",
                "DOUBLE": "=",
                "TRIPLE": "#",
                "AROMATIC": ":",
                "QUADRUPLE": "$"}
AtomData = namedtuple("AtomData", "elem_symbol, bond_to_parent")


class AtomTree(Tree):
    def __init__(self, molecule: Mol, max_depth: int=MAX_DEPTH):
        self.molecule = molecule
        self.root_index = None
        self.next_level = set()
        self.level_no = None
        self.max_depth = max_depth
        super().__init__(self)
    
    def create_atom_node(self, atom: Atom, parent: (None, Atom)=None):
        if parent:
            # IT'S BRANCH
            atom_id = atom.GetIdx()
            parent_id = parent.GetIdx()
            element_symbol = atom.GetSymbol()
            bond = self.molecule.GetBondBetweenAtoms(parent_id,
                                                     atom_id)
            bond_symbol = BOND_SYMBOLS[str(bond.GetBondType())]
            atom_data = AtomData(element_symbol, bond_symbol)
        else:
            # IT'S ROOT
            self.level_no = 0
            self.root_index = atom.GetIdx()
            atom_id = self.root_index
            self.next_level = {atom_id}
            parent_id = None
            element_symbol = atom.GetSymbol()
            atom_data = AtomData(element_symbol, None)
        super().create_node(element_symbol,
                            atom_id,
                            parent=parent_id,
                            data=atom_data)

    def grow(self):
        while self.next_level and self.level_no < self.max_depth:
            current_level = set(self.next_level)
            self.next_level = set()
            self.level_no += 1
            for atom_id in current_level:
                self.process_atom(atom_id)

    def process_atom(self, atom_id):
        atom_Atom = self.molecule.GetAtomWithIdx(atom_id)
        atom_neighbors = atom_Atom.GetNeighbors()
        for neig in atom_neighbors:
            neig_id = neig.GetIdx()
            # if node with this id already not in tree,
            # tree.get_node(id) gives False
            its_new_neighbor_atom = not self.get_node(neig_id)
            if its_new_neighbor_atom:
                self.next_level.add(neig_id)
                self.create_atom_node(neig, parent=atom_Atom)


def main():
    caffeine_smiles = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
    caffeine = MolFromSmiles(caffeine_smiles)
    atom_tree = AtomTree(caffeine)
    atom_tree.create_atom_node(caffeine.GetAtomWithIdx(4))
    atom_tree.grow()
    atom_tree.show()


if __name__ == '__main__':
    main()
