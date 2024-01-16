<template>
    <div class="container">
        <input
            type="text"
            name="numeral_input"
            class="simple_text_value"
            v-on:input="inputValidation"
            v-model="inputValue"
        >
        <select
            name="unit_input"
            v-bind:value="unit"
            v-model="unitValue"
            class="narrow-select"
        >
            <option
                v-for="unit in units" v-bind:value="unit"
                v-bind:selected="unit === units[0]"
            >{{unit}}</option>
        </select>
        <div v-bind:class="{warning: true, 'hide-me': !warningWrongSymbol}">
            You  are trying to enter a symbol that is not allowed in numeric field
        </div>
        <div v-bind:class="{warning: true, 'hide-me': !warningOddDelimiter}">
            You  are trying to enter second decimal separator
        </div>
        <div v-bind:class="{warning: true, 'hide-me': !warningEmptyField}">
            You  are trying to commit empty field. Some value needed for commit.
        </div>
    </div>
</template>

<script>
export default {
    name: "OneNumeralAndUnit",
    props: ["unit", "number", "units"],
    inject: ["completeEditing"],
    data() {
        return {
            numericSymbols: new Set("0123456789.,"),
            inputValue: this.number,
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
        // TODO: заменить метод inputValidation на watcher
        inputValidation() {
            this.warningEmptyField = false
            this.warningOddDelimiter = false
            let valueSet = new Set(this.inputValue)
            if (this.difference(valueSet, this.numericSymbols).size > 0) {
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
        difference(setA, setB) {
            const _difference = new Set(setA);
            for (const elem of setB) {
                _difference.delete(elem);
            }
            return _difference;
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