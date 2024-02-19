<template>
    <input
        type="text"
        class="simple-text-input"
        v-bind:name="inputName"
        v-bind:disabled="disabled"
        v-on:input="inputValidation"
        v-model="inputValue"
    >
    <div 
        class="warning"
        v-show="warningWrongSymbol"
    >
        You  are trying to enter a symbol that is not allowed in numerical field
    </div>
    <div
        class="warning"
        v-show="warningOddDelimiter"
    >
        You  are trying to enter second decimal separator
    </div>
</template>

<script>
import {difference} from "@/components/constants"

export default {
    name: "NumericalInput",
    props: ["inputName", "disabled"],
    data() {
        return {
            numericalSymbols: new Set("0123456789.,"),
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
            if (difference(valueSet, this.numericalSymbols).size > 0) {
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