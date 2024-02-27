<template>
    <div class="container">
        <input
            v-model="inputValue"
            v-on:input="inputValidation"
            type="text"
            name="numerical_input"
            class="simple_text_value"
        >
        <select
            v-model="unitValue"
            name="unit_input"
            class="narrow-select"
        >
            <option
                v-for="unit_ in units"
                v-bind:value="unit_"
            >{{unit_}}</option>
            <option value="" selected>—</option>
        </select>
        <div
            v-show="warningWrongSymbol"
            class="warning"
        >
            You  are trying to enter a symbol that is not allowed
            in numeric field
        </div>
        <div
            v-show="warningOddDelimiter"
            class="warning"
        >
            You  are trying to enter second decimal separator
        </div>
        <div
            v-show="warningEmptyField"
            class="warning"
        >
            You  are trying to commit empty field. Some value
            needed for commit.
        </div>
        <div
            v-show="warningInvalidValue"
            class="warning"
        >
            Invalid value
        </div>
        <div
            v-show="warningEmptyUnit"
            class="warning"
        >
            Unit must be filled
        </div>
    </div>
</template>

<script>
import {difference} from "../utils/constants.js"

export default {
    name: "OneNumericalAndUnit",
    inject: ["completeEditing"],
    props: ["unit", "number", "units"],
    data() {
        return {
            numericSymbols: new Set("0123456789.,"),
            inputValue: String(this.number),
            oldInputValue: String(this.number),
            unitValue: this.unit,
            warningWrongSymbol: false,
            warningOddDelimiter: false,
            warningEmptyField: false,
            warningInvalidValue: false,
            warningEmptyUnit: false,
        }
    },
    watch: {
        unitValue() {
            this.warningEmptyUnit = false
        }
    },
    methods: {
        localCompleteEditing() {
            if (this.validationBeforeCommit()) {
                let result = {number: this.inputValue, unit: this.unitValue}
                this.completeEditing("quantity", result)
            }
        },
        validationBeforeCommit() {
            if (this.inputValue === "") {
                this.warningEmptyField = true
            }
            if (
                isNaN(Number(this.inputValue)) ||
                Number(this.inputValue) <= 0
            ) {
                this.warningInvalidValue = true
            }
            if (this.unitValue === "") {
                this.warningEmptyUnit = true
            }
            return !(
                this.warningEmptyField ||
                this.warningInvalidValue ||
                this.warningEmptyUnit
            )
        },
        inputValidation() {
            this.warningEmptyField = false
            this.warningOddDelimiter = false
            this.warningInvalidValue = false
            this.warningEmptyUnit = false
            let valueSet = new Set(this.inputValue)
            if (difference(valueSet, this.numericSymbols).size > 0) {
                this.inputValue = this.oldInputValue
                this.warningWrongSymbol = true
            } else if (this.warningWrongSymbol) {
                this.warningWrongSymbol = false
            }
            this.singleDelimiterCheck(valueSet)
            if (!(this.warningWrongSymbol || this.warningOddDelimiter)) {
                this.oldInputValue = this.inputValue
            }
        },
        singleDelimiterCheck(valueSet) {
            if (valueSet.has(".") || valueSet.has(",")) {
                if ((this.inputValue.split(".").length +
                    this.inputValue.split(",").length - 2) >= 2) {
                    this.inputValue = this.oldInputValue
                    this.warningOddDelimiter = true
                }
            }
        },
        clear() {
            this.inputValue = ""
            this.unitValue = ""
        },
    },
}
</script>

<style scoped>
div.container {
    display: grid;
    grid-template-columns: 31% 31% 31%;
    column-gap: 3.5%;
}
div.warning {
    grid-column: span 3;
}
input.simple_text_value {
    grid-column: span 1;
    width: auto;
}
select.narrow-select {
    font-size: 18px;
    color: cornflowerblue;
    background-color: azure;
    border: solid cornflowerblue 3px;
    border-radius: 0;
    width: auto;
    height: 45px;
    padding-left: 8px;
    appearance: none;
    -moz-appearance: none;
    -webkit-appearance: none;
    background-image: url("../assets/Triangle_in_square.svg");
    background-position: right;
    background-repeat: no-repeat;
    background-size: 45px;
}
</style>