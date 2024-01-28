<template>
    <div class="container">
        <input
            type="text"
            v-bind:name="inputName + '_left'"
            v-bind:disabled="disabled"
            class="simple_text_value"
            v-on:input="inputValidationLeft"
            v-model="inputValueLeft"
        >
        <input
            type="text"
            v-bind:name="inputName + '_right'"
            v-bind:disabled="disabled"
            class="simple_text_value"
            v-on:input="inputValidationRight"
            v-model="inputValueRight"
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
    </div>
</template>

<script>
export default {
    name: "TwoNumericalInputs",
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
            if (this.difference(valueSet, this.numericSymbols).size > 0) {
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
            if (this.difference(valueSet, this.numericSymbols).size > 0) {
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
    grid-template-columns: 48% 48%;
    column-gap: 4%;
}
div.warning {
    grid-column: span 2;
}
input.simple_text_value {
    grid-column: span 1;
    width: auto;
}
</style>