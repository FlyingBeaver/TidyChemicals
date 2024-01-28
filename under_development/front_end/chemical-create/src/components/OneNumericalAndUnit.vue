<template>
    <div class="container">
        <input
            type="text"
            name="numerical_input"
            class="simple_text_value"
            v-on:input="inputValidation"
            v-model="inputValue"
        >
        <select
            name="unit_input"
            v-model="unitValue"
            class="narrow-select"
        >
            <option
                v-for="unit_ in units"
                v-bind:value="unit_"
            >{{unit_}}</option>
            <option value="" selected>—</option>
        </select>
        <div
            class="warning"
            v-show="warningWrongSymbol"
        >
            You  are trying to enter a symbol that is not allowed
            in numeric field
        </div>
        <div
            class="warning"
            v-show="warningOddDelimiter"
        >
            You  are trying to enter second decimal separator
        </div>
        <div
            class="warning"
            v-show="warningEmptyField"
        >
            You  are trying to commit empty field. Some value
            needed for commit.
        </div>
    </div>
</template>

<script>
import {difference} from "./constants.js"
export default {
    name: "OneNumericalAndUnit",
    props: ["unit", "number", "units"],
    inject: ["completeEditing"],
    data() {
        return {
            numericSymbols: new Set("0123456789.,"),
            inputValue: String(this.number),
            oldInputValue: "",
            unitValue: this.unit,
            warningWrongSymbol: false,
            warningOddDelimiter: false,
            warningEmptyField: false,
        }
    },
    methods: {
        localCompleteEditing() {
            if (this.inputValue !== "") {
                let result = {number: this.inputValue, unit: this.unitValue}
                this.completeEditing("quantity", result)
            } else {
                this.warningEmptyField = true
            }
        },
        inputValidation() {
            this.warningEmptyField = false
            this.warningOddDelimiter = false
            let valueSet = new Set(this.inputValue)
            if (difference(valueSet, this.numericSymbols).size > 0) {
                this.inputValue = this.oldInputValue
                this.warningWrongSymbol = true
            } else if (this.warningWrongSymbol) {
                this.warningWrongSymbol = false
            }
            this.singleDelimiterCheck(valueSet)
            if (!this.warningWrongSymbol && !this.warningOddDelimiter) {
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
        }
    }
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