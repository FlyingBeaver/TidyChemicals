<template>
    <div class="three-columns-container">
        <input
            type="text"
            v-bind:name="inputName + '_left'"
            v-bind:disabled="disabled"
            class="narrow-text-input"
            v-on:input="inputValidationLeft"
            v-model="inputValueLeft"
        >
        <input
            type="text"
            v-bind:name="inputName + '_right'"
            v-bind:disabled="disabled"
            class="narrow-text-input"
            v-on:input="inputValidationRight"
            v-model="inputValueRight"
        >
        <select
            type="text"
            v-bind:name="inputName + '_unit'"
            v-bind:disabled="disabled"
            class="narrow-select"
        >
            <option value="g">g</option>
            <option value="kg">kg</option>
            <option value="mg">mg</option>
            <option value="l">l</option>
            <option value="ml">ml</option>
        </select>
        <div
            class="warning-width-3"
            v-show="warningWrongSymbol"
        >
            You  are trying to enter a character that is not allowed
            in numerical field
        </div>
        <div
            class="warning-width-3"
            v-show="warningOddDelimiter"
        >
            You  are trying to enter second decimal separator
        </div>
    </div>
</template>

<script>
import {difference} from "@/components/constants"

export default {
    name: "TwoNumericalAndUnit",
    props: ["inputName", "disabled"],
    data() {
        return {
            numericSymbols: new Set("0123456789.,"),
            inputValueLeft: "",
            inputValueRight: "",
            oldInputValueLeft: "",
            oldInputValueRight: "",
            warningWrongSymbol: false,
            warningOddDelimiter: false,
        }
    },
    methods: {
        inputValidationLeft() {
            this.warningOddDelimiter = false
            let valueSet = new Set(this.inputValueLeft)
            if (difference(valueSet, this.numericSymbols).size > 0) {
                this.inputValueLeft = this.oldInputValueLeft
                this.warningWrongSymbol = true
            } else if (this.warningWrongSymbol) {
                this.warningWrongSymbol = false
            }
            this.singleDelimiterCheck(valueSet, "left")
            if (!this.warningWrongSymbol && !this.warningOddDelimiter) {
                this.oldInputValueLeft = this.inputValueLeft
            }
        },
        inputValidationRight() {
            this.warningOddDelimiter = false
            let valueSet = new Set(this.inputValueRight)
            if (difference(valueSet, this.numericSymbols).size > 0) {
                this.inputValueRight = this.oldInputValueRight
                this.warningWrongSymbol = true
            } else if (this.warningWrongSymbol) {
                this.warningWrongSymbol = false
            }
            this.singleDelimiterCheck(valueSet, "right")
            if (!this.warningWrongSymbol && !this.warningOddDelimiter) {
                this.oldInputValueRight = this.inputValueRight
            }
        },
        singleDelimiterCheck(valueSet, whichField) {
            if (valueSet.has(".") || valueSet.has(",")) {
                if (whichField === "left") {
                    if ((this.inputValueLeft.split(".").length +
                        this.inputValueLeft.split(",").length - 2) >= 2) {
                        this.inputValueLeft = this.oldInputValueLeft
                        this.warningOddDelimiter = true
                    }
                } else if (whichField === "right") {
                    if ((this.inputValueRight.split(".").length +
                        this.inputValueRight.split(",").length - 2) >= 2) {
                        this.inputValueRight = this.oldInputValueRight
                        this.warningOddDelimiter = true
                    }
                }
            }
        },
    }
}
</script>

<style>
</style>