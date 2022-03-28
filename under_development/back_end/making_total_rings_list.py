from re import findall
from copy import deepcopy
from rdkit.Chem import (MolFromSmiles, 
                        MolToSmiles,
                        DeleteSubstructs, 
                        FragmentOnBonds,
                        MolFromSmarts)
from rdkit.Chem.rdchem import Mol


BOND_TYPES = {"SINGLE": "-", 
              "DOUBLE": "=", 
              "TRIPLE": "#", 
              "AROMATIC": ":"}


def generate_canonic(ring_repr: str):
    candidates = []
    candidates.append(ring_repr)
    list_rep1 = findall(r"[a-zA-Z]+[-=#:]+", ring_repr)
    for i in range(1, len(list_rep1)):
        candidates.append(''.join(list_rep1[-i:]) + ''.join(list_rep1[0: -i]))
    raw_rev = ring_repr[-1] + ring_repr[:-1]
    ring_repr_reversed = raw_rev[:: -1]
    
    candidates.append(ring_repr_reversed)
    list_rep_rev = findall(r"[a-zA-Z]+[-=#:]+", ring_repr_reversed)
    for i in range(1, len(list_rep_rev)):
        candidates.append(''.join(list_rep_rev[-i:]) + ''.join(list_rep_rev[0: -i]))
    set_of_reps = set(candidates)
    reps_dict = dict()
    for rep in set_of_reps:
        reps_dict[rep] = hash(rep)
    items_reps = list(reps_dict.items())
    items_reps.sort(key=lambda x: x[1])
    return items_reps[0][0]


def remove_not_unic(some_list: list):
    n = 0
    while n < len(some_list):
        if some_list.count(some_list[n]) > 1:
            some_list.pop(n)
            continue
        else:
            n += 1
    return some_list


class RingsSystem:
    def __init__(self, 
                 structure: Mol):
        self.structure = structure
        self.ring_info = self.structure.GetRingInfo()
        self.bond_rings = self.ring_info.BondRings()
        self.atom_rings = self.ring_info.AtomRings()
        self.intersections = []
        self._make_intersections()
    
    def _make_intersections(self):
        for ring in self.bond_rings:
            for ring2 in self.bond_rings:
                if ring == ring2:
                    continue
                elif set(ring) & set(ring2):
                    list1 = list(ring)
                    list2 = list(ring2)
                    list1.sort()
                    list2.sort()
                    self.intersections.append([list1, 
                                               list2])
        self.intersections = remove_not_unic(self.intersections)

    def get_intersections_n(self):
        return len(self.intersections)

    def how_many_explicit_rings(self):
        return self.ring_info.NumRings()
    
    def remove_intersection(self, intersection_index: int):
        if intersection_index > self.get_intersections_n():
            raise ValueError("intersection_index too big")
        inter1, inter2 = self.intersections[intersection_index]
        common_bonds = set(inter1) & set(inter2)
        if len(common_bonds) == 1:
            new_structure = FragmentOnBonds(self.structure, list(common_bonds))
            DeleteSubstructs(new_structure, MolFromSmarts('[#0]'))
        else:
            new_structure = deepcopy(self.structure)
            bridge_atoms_list = []
            for bond_index in common_bonds:
                bond = new_structure.GetBondWithIdx(bond_index)
                bridge_atoms_list.append(bond.GetBeginAtom())
                bridge_atoms_list.append(bond.GetEndAtom())
            for atom in bridge_atoms_list:
                if bridge_atoms_list.count(atom) == 1:
                    continue
                else:
                    atom.SetAtomicNum(0)
            DeleteSubstructs(new_structure, MolFromSmarts('[#0]'))
            new_structure = FragmentOnBonds(new_structure, 
                                            list(common_bonds))
        return RingsSystem(MolFromSmiles(MolToSmiles(new_structure)))

    def get_rings(self):
        # import pdb; pdb.set_trace()
        ring_strings = []
        for ring in self.atom_rings:
            string_repr = ''
            for i in range(len(ring)):
                atom_index = ring[i]
                atom = self.structure.GetAtomWithIdx(atom_index)
                symbol = atom.GetSymbol()
                string_repr += symbol
                if i < len(ring) - 1:
                    next_atom_index = ring[i + 1]
                else:
                    next_atom_index = ring[0]
                next_atom = self.structure\
                .GetAtomWithIdx(next_atom_index)
                bond = self.structure.GetBondBetweenAtoms(atom_index,
                                                          next_atom_index)
                bond_symbol = BOND_TYPES[str(bond.GetBondType())]
                string_repr += bond_symbol
            ring_strings.append(generate_canonic(string_repr))
        return ring_strings



def main():
    pass

if __name__ == '__main__':
    main()
