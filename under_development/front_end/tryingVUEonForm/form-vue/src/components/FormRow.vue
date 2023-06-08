<template>
    <div
        class="row"
        v-bind:id="rowId"
        v-on:mouseenter="deletionModeOn ? processMouseEnter() : null"
        v-on:mouseleave="deletionModeOn ? processMouseLeave() : null"
        v-on:click="deletionModeOn ? processClick() : null"
        v-bind:class="{ fired: firedId === rowId }"
    >
        <p class="column" v-if="!rowId.includes('_plus_')">
            <select v-bind:name="rowId + '_term'"
                required 
                v-model="termValue" 
                v-on:change="whenTermChanged"
                v-bind:disabled="deletionModeOn"
            >
                <option value='' selected>Choose search option</option>
                <option value='cas'>CAS RN</option>
                <option value='comment'>Comment</option>
                <option value='molar_mass'>Molar mass</option>
                <option value='molecular_formula'>Molecular formula</option>
                <option value='name'>Name</option>
                <option value='quantity_with_unit'>Quantity</option>
                <option value='storage_place'>Storage place</option>
                <option value='structure'>Structure</option>
                <option value='synonym'>Synonym</option>
                <option value='when_created'>Creation date</option>
                <option value='when_updated'>Last update date</option>
                <option value='who_created'>Created by</option>
                <option value='who_updated'>Updated by</option>
            </select>
        </p>
        <p class="operator_box column" v-if="!rowId.includes('_plus_')">
            <span v-if="operatorOptions === ''" class="inactive-field">Operator</span>
            <select 
                v-else
                v-bind:name="rowId + '_term'" 
                required 
                v-model="operatorValue"
                v-bind:disabled="deletionModeOn"
                >
                <option v-for="(verbose, operator) in operatorOptions"
                    v-bind:key="operator"
                    v-bind:value="operator"
                >
                    {{ verbose }}
                </option>
                <option key="null" value="" selected>Choose an operator</option>
            </select>
        </p>
        <p class="value_box column" v-if="!rowId.includes('_plus_')">
            <span class="inactive-field" v-if="widget === 'inactive'">Value</span>
            <text-input 
                v-if="widget === 'text_input'"
                v-bind:disabled="deletionModeOn"
            ></text-input>
        </p>
        <div class="operator_between_box" v-if="rowId.includes('_plus_')">
            <select 
                v-bind:name="rowId"
                required=""
                v-bind:disabled="deletionModeOn"
            >
                <option value="" selected="">AND / NOT / AND NOT</option>
                <option value="and">And</option>
                <option value="or">Or</option>
                <option value="and_not">And not</option>
            </select>
        </div>
    </div>
</template>


<script>
import TextInput from './TextInput.vue';


export default {

    components: {
        TextInput
    },
    computed: {
        operatorOptions() {
            if (this.termValue in this.tree) {
                let optionsObj = this.tree[this.termValue];
                let result = {}
                for (let option in optionsObj) {
                    if (option !== "verbose") {
                        result[option] = optionsObj[option].verbose;
                    }
                }
                return result;
            } else {
                return "";
            }
        },
        widget() {
            if (this.operatorValue && this.termValue) {
                let result = this.tree[this.termValue][this.operatorValue].widget;
                if (this.validWidgets.includes(result)) {
                    return result;
                } else {
                    return "inactive";
                }
            } else {
                return "inactive";
            }
        }
    },
    methods: {
        whenTermChanged() {
            this.operatorValue = "";
        },
        processMouseEnter() {
            this.$emit("mouse-enter-happened", this.rowId)
        },
        processMouseLeave() {
            this.$emit("mouse-leave-happened")
        },
        processClick() {
            this.$emit("click-happened", this.rowId)
        }
    },
    props: ["rowId", "deletionModeOn", 'firedId'],
    emits: ["mouse-enter-happened",
            "mouse-leave-happened", 
            "click-happened"],
    data() {
        return {
            validWidgets: ['text_input'],
            operatorValue: "",
            termValue: "",
            tree: {
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
            }
        }
    }
}
</script>