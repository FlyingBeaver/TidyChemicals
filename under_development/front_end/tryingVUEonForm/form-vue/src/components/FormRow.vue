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
                v-bind:name="rowId + '_operator'"
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
                v-bind:input-name="rowId + '_value'"
            ></text-input>
            <text-input-with-format
                v-if="widget === 'text_input_with_format'"
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'"
            ></text-input-with-format>
            <structure-input-toggle
                v-if="widget === 'jsme_input'"
                v-bind:disabled="deletionModeOn"
                v-on:toggle-editor="toggleEditor"
            >
            </structure-input-toggle>
            <numeral-input
                v-if="widget === 'numeral_input'"
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'"
            ></numeral-input>
            <date-input
                v-if="widget === 'date_input'"
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'"
            ></date-input>
            <date-range-input
                v-if="widget === 'date_range_input'"
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'"
            ></date-range-input>
            <storage-place-input
                v-if="widget === 'storage_place_input'"
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'"
            ></storage-place-input>
            <user-input
                v-if="widget === 'user_input'"
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'"
            ></user-input>
            <cas-input
                v-if="widget === 'cas_input'"
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'"
            ></cas-input>
            <two-numeral-inputs
                v-if="widget === 'two_numeral_inputs'"
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'"
            ></two-numeral-inputs>
            <two-numeral-and-unit
                v-if="widget === 'two_numeral_and_unit'"
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'"
            ></two-numeral-and-unit>
        </p>
        <p class="column ketcher-container"
           v-if="widget === 'jsme_input'"
           v-show="editorShown">
            <structure-input
                v-bind:disabled="deletionModeOn"
                v-bind:input-name="rowId + '_value'">
            </structure-input>
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
import {tree} from "./constants"
import TextInput from './TextInput.vue';
import TextInputWithFormat from "@/components/TextInputWithFormat";
import StructureInput from "@/components/StructureInput";
import StructureInputToggle from "@/components/StructureInputToggle";
import NumeralInput from "@/components/NumeralInput";
import DateInput from "@/components/DateInput";
import DateRangeInput from "@/components/DateRangeInput";
import StoragePlaceInput from "@/components/StoragePlaceInput";
import UserInput from "@/components/UserInput";
import CasInput from "@/components/CasInput";
import TwoNumeralInputs from "@/components/TwoNumeralInputs";
import TwoNumeralAndUnit from "@/components/TwoNumeralAndUnit";

export default {

    components: {
        TwoNumeralAndUnit,
        CasInput,
        UserInput,
        StoragePlaceInput,
        NumeralInput,
        StructureInput,
        TextInput,
        TextInputWithFormat,
        StructureInputToggle,
        DateInput,
        DateRangeInput,
        TwoNumeralInputs,
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
        toggleEditor() {
            this.editorShown = !this.editorShown
        },
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
            validWidgets:
                [
                    'text_input',
                    'text_input_with_format',
                    'jsme_input',
                    'numeral_input',
                    'date_input',
                    'date_range_input',
                    'storage_place_input',
                    'user_input',
                    'cas_input',
                    'two_numeral_inputs',
                    'two_numeral_and_unit',
                ],
            operatorValue: "",
            termValue: "",
            tree,
            editorShown: false,
        }
    }
}
</script>

<style>
    p.column.ketcher-container {
        grid-column-start: 2;
        grid-column-end: 4;
    }

    textarea.cliparea {
        display: none;
    }
</style>