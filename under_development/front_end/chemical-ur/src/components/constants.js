export const tree = {
    cas: {
        equals: {
            verbose: 'equals',
                widget: 'cas_input'
        },
        verbose: 'CAS RN'
    },
    comment: {
        ends_with: {
            verbose: 'ends with',
                widget: 'text_input'
        },
        exact_match: {
            verbose: 'exact match',
                widget: 'text_input'
        },
        includes: {
            verbose: 'includes',
                widget: 'text_input'
        },
        starts_with: {
            verbose: 'starts with',
                widget: 'text_input'
        },
        verbose: 'Comment'
    },
    molar_mass: {
        equals: {
            verbose: 'equals',
                widget: 'numerical_input'
        },
        in_interval_between: {
            verbose: 'in interval between',
                widget: 'two_numerical_inputs'
        },
        less_than: {
            verbose: 'less than',
                widget: 'numerical_input'
        },
        more_than: {
            verbose: 'more than',
                widget: 'numerical_input'
        },
        verbose: 'Molar mass'
    },
    molecular_formula: {
        exact_match: {
            verbose: 'exact match',
                widget: 'molecular_formula_input'
        },
        includes: {
            verbose: 'includes',
                widget: 'molecular_formula_input'
        },
        verbose: 'Molecular formula'
    },
    name: {
        ends_with: {
            verbose: 'ends with',
                widget: 'text_input_with_format'
        },
        exact_match: {
            verbose: 'exact match',
                widget: 'text_input_with_format'
        },
        includes: {
            verbose: 'includes',
                widget: 'text_input_with_format'
        },
        starts_with: {
            verbose: 'starts with',
                widget: 'text_input_with_format'
        },
        verbose: 'Name'
    },
    quantity_with_unit: {
        equals: {
            verbose: 'equals',
                widget: 'numerical_and_unit'
        },
        in_interval_between: {
            verbose: 'in interval between',
                widget: 'two_numerical_and_unit'
        },
        less_than: {
            verbose: 'less than',
                widget: 'numerical_and_unit'
        },
        more_than: {
            verbose: 'more than',
                widget: 'numerical_and_unit'
        },
        verbose: 'Quantity'
    },
    storage_place: {
        choose_from_list: {
            verbose: 'choice from the list',
                widget: 'storage_place_input'
        },
        verbose: 'Storage place'
    },
    structure: {
        exact_match: {
            verbose: 'exact match',
                widget: 'ketcher_input'
        },
        substructure: {
            verbose: 'substructure',
                widget: 'ketcher_input'
        },
        substructure_greedy: {
            verbose: 'substructure (greedy)',
                widget: 'ketcher_input'
        },
        verbose: 'Structure'
    },
    synonym: {
        ends_with: {
            verbose: 'ends with',
                widget: 'text_input'
        },
        exact_match: {
            verbose: 'exact match',
                widget: 'text_input'
        },
        includes: {
            verbose: 'includes',
                widget: 'text_input'
        },
        starts_with: {
            verbose: 'starts with',
                widget: 'text_input'
        },
        verbose: 'Synonym'
    },
    when_created: {
        date_before: {
            verbose: 'date before',
                widget: 'date_input'
        },
        date_from: {
            verbose: 'date from',
                widget: 'date_input'
        },
        date_range: {
            verbose: 'date range',
                widget: 'date_range_input'
        },
        verbose: 'Creation date'
    },
    when_updated: {
        date_before: {
            verbose: 'date before',
                widget: 'date_input'
        },
        date_from: {
            verbose: 'date from',
                widget: 'date_input'
        },
        date_range: {
            verbose: 'date range',
                widget: 'date_range_input'
        },
        verbose: 'Last update date'
    },
    who_created: {
        choose_profile_from_list: {
            verbose: 'choice of profile from the list',
                widget: 'user_input'
        },
        type: {
            verbose: 'text input',
                widget: 'text_input'
        },
        type_with_prompts: {
            verbose: 'prompted text input',
                widget: 'prompted_text_input'
        },
        verbose: 'Created by'
    },
    who_updated: {
        choose_profile_from_list: {
            verbose: 'choice of profile from the list',
                widget: 'user_input'
        },
        type: {
            verbose: 'text input',
                widget: 'text_input'
        },
        type_with_prompts: {
            verbose: 'prompted text input',
                widget: 'prompted_text_input'
        },
        verbose: 'Updated by'
    }
}

export const characters = {
    alpha: "α",
    beta: "β",
    gamma: "γ",
    delta: "δ",
    epsilon: "ε",
    zeta: "ζ",
    eta: "η",
    theta: "θ",
    iota: "ι",
    kappa: "κ",
    lambda: "λ",
    mu: "μ",
    nu: "ν",
    xi: "ξ",
    omicron: "ο",
    pi: "π",
    rho: "ρ",
    sigma: "σ",
    tau: "τ",
    upsilon: "υ",
    phi: "φ",
    chi: "χ",
    psi: "ψ",
    omega: "ω",
    capital_alpha: "Α",
    capital_beta: "Β",
    capital_gamma: "Γ",
    capital_delta: "Δ",
    capital_epsilon: "Ε",
    capital_zeta: "Ζ",
    capital_eta: "Η",
    capital_theta: "Θ",
    capital_iota: "Ι",
    capital_kappa: "Κ",
    capital_lambda: "Λ",
    capital_mu: "Μ",
    capital_nu: "Ν",
    capital_xi: "Ξ",
    capital_omicron: "Ο",
    capital_pi: "Π",
    capital_rho: "Ρ",
    capital_sigma: "Σ",
    capital_tau: "Τ",
    capital_upsilon: "Υ",
    capital_phi: "Φ",
    capital_chi: "Χ",
    capital_psi: "Ψ",
    capital_omega: "Ω",
    prime: "′",
    em_dash: "—",
    plus_minus: "±"
}

export const characters_in_string = ("0123456789 .,()[]{}+-/:;abcdefg" +
    "hijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρστ" +
    "υφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ′—±")

export const difference = function (setA, setB) {
    const _difference = new Set(setA);
    for (const elem of setB) {
        _difference.delete(elem);
    }
    return _difference;
}

export const charactersForTags = ("#&0123456789abcdefghijklmnopqrstu" +
    "vwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")

export const emptyMol = `
  Ketcher  1182418572D 1   1.00000     0.00000     0

  0  0  0  0  0  0  0  0  0  0999 V2000
M  END`

export const dataKeys = [
    'id',
    'name_data',
    'structure_pic',
    'structure_mol',
    'structure_aq',
    'location',
    'quantity',
    'hazard_pictograms',
    'molar_mass',
    'cas',
    'synonyms',
    'comment',
    'tags',
    'created_by',
    'creation_date',
    'last_change_by',
    'last_change_date'
]

export const elementSymbols = [
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
    'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni',
    'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb',
    'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd',
    'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs',
    'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
    'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
    'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb',
    'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa',
    'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
    'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt',
    'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
]
