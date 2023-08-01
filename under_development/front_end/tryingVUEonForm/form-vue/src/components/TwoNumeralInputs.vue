<template>
    <div class="container">
        <input
            type="text"
            v-bind:name="inputName"
            v-bind:disabled="disabled"
            class="simple_text_value"
            v-on:input="inputValidation"
            v-model="inputValueLeft"
        >
        <input
            type="text"
            v-bind:name="inputName"
            v-bind:disabled="disabled"
            class="simple_text_value"
            v-on:input="inputValidation"
            v-model="inputValueRight"
        >
        <div v-bind:class="{warning: true, 'hide-me': !warningWrongSymbol}">
            You  are trying to enter a symbol that is not allowed in numeric field
        </div>
        <div v-bind:class="{warning: true, 'hide-me': !warningOddDelimiter}">
            You  are trying to enter second decimal separator
        </div>
    </div>
</template>

<script>
export default {
    name: "NumeralInput",
    props: ["inputName", "disabled"],
    data() {
        return {
            numericSymbols: new Set("0123456789.,"),
            inputValueLeft: "",
            inputValueRight: "",
            warningWrongSymbol: false,
            warningOddDelimiter: false,
            oldInputValue: "",
        }
    },
    methods: {
        inputValidation() {
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
    grid-template-columns: 50% 50%;
    column-gap: 10px;
}
div.warning {
    grid-column: span 2;
}
input.simple_text_value {
    grid-column: span 1;
    width: auto;
}
</style>