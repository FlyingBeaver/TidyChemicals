tree = {
  cas: {
    equals: {
      verbose: 'equals',
      widget: 'numeral_input_cas'
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
      widget: 'numeral_input'
    },
    equals_with_epsilon: {
      verbose: 'equals with epsilon',
      widget: 'special_numeral_input'
    },
    in_interval_between: {
      verbose: 'in interval between',
      widget: 'two_numeral_inputs'
    },
    less_than: {
      verbose: 'less than',
      widget: 'numeral_input'
    },
    more_than: {
      verbose: 'more than',
      widget: 'numeral_input'
    },
    verbose: 'Molar mass'
  },
  molecular_formula: {
    exact_match: {
      verbose: 'exact match',
      widget: 'formula_text_input'
    },
    includes: {
      verbose: 'includes',
      widget: 'formula_text_input'
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
      widget: 'numeral_and_unit'
    },
    equals_with_epsilon: {
      verbose: 'in interval around',
      widget: 'numeral_epsilon_unit'
    },
    in_interval_between: {
      verbose: 'in interval between',
      widget: 'two_numerals_and_unit'
    },
    less_than: {
      verbose: 'less than',
      widget: 'numeral_and_unit'
    },
    more_than: {
      verbose: 'more than',
      widget: 'numeral_and_unit'
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
      widget: 'jsme_input'
    },
    substructure: {
      verbose: 'substructure',
      widget: 'jsme_input'
    },
    substructure_greedy: {
      verbose: 'substructure (greedy)',
      widget: 'jsme_input'
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
      widget: 'select_profile_from_list'
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
      widget: 'select_profile_from_list'
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
};
