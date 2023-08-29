<template>
    <input
        type="text"
        v-bind:name="inputName"
        v-bind:disabled="disabled"
        class="simple_text_value"
        v-on:input="inputValidation"
        v-model="inputValue"
    >
    <div v-bind:class="{warning: true, 'hide-me': !warningWrongSymbol}">
        You  are trying to enter a symbol that is not allowed in numeric field
    </div>
    <div v-bind:class="{warning: true, 'hide-me': !warningOddDelimiter}">
        You  are trying to enter second decimal separator
    </div>
</template>

<script>
import {difference} from "@/components/constants";

export default {
    name: "NumeralInput",
    props: ["inputName", "disabled"],
    data() {
        return {
            numericSymbols: new Set("0123456789.,"),
            inputValue: "",
            warningWrongSymbol: false,
            warningOddDelimiter: false,
            oldInputValue: "",
        }
    },
    methods: {
        inputValidation() {
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

    }
}
</script>

<style>

</style>