<template>
    <input
        type="text"
        v-bind:name="inputName"
        v-bind:disabled="disabled"
        class="simple_text_value"
        v-on:blur="inputValidationOnBlur"
        v-on:focus="hideInvalidCasWarning"
        v-on:input="inputValidationOnInput"
        v-model="inputValue"
    >
    <div v-bind:class="{warning: true, 'hide-me': !warningWrongSymbol}">
        You  are trying to enter a symbol that is not allowed in this field
    </div>
    <div v-bind:class="{warning: true, 'hide-me': !warningInvalidCas}">
        Invalid value of CAS RN. If you didn't completed input of CAS RN, you can ignore this message
    </div>
    <div v-bind:class="{warning: true, 'hide-me': !warningTooLongValue}">
        You are trying to input too long value for CAS RN. Valid CAS RN can't contain more than 10 digits.
    </div>
    <div v-bind:class="{warning: true, 'hide-me': !warningThreeHyphens}">
        You  are trying to enter third hyphen, but CAS RN can contain only two hyphens
    </div>
    <div v-bind:class="{warning: true, 'hide-me': !warningHyphensTogether}">
        You  are trying to enter two hyphens together, but hyphens must separate groups of digits
    </div>
</template>

<script>
export default {
    name: "CasInput",
    props: ["inputName", "disabled"],
    data() {
        return {
            expectedSymbols: new Set("0123456789-"),
            digits: new Set("0123456789"),
            oldInputValue: "",
            inputValue: "",
            warningInvalidCas: false,
            warningTooLongValue: false,
            warningWrongSymbol: false,
            warningThreeHyphens: false,
            warningHyphensTogether: false,
        }
    },
    methods: {
        charCheck() {
            let ok = true
            for (let char of this.inputValue) {
                if (!this.expectedSymbols.has(char)) {
                    ok = false
                    break
                }
            }
            if (!ok) {
                this.warningWrongSymbol = true
                this.inputValue = this.oldInputValue
            } else {
                this.warningWrongSymbol = false
            }
        },
        twoHyphensCheck() {
            if (this.inputValue.split("-").length > 3) {
                this.warningThreeHyphens = true
                this.inputValue = this.oldInputValue
            } else {
                this.warningThreeHyphens = false
            }
        },
        hyphensTogetherCheck() {
            if (this.inputValue.indexOf("--") !== -1) {
                this.warningHyphensTogether = true
                this.inputValue = this.oldInputValue
            } else {
                this.warningHyphensTogether = false
            }
        },
        tooManyDigits() {
            let digitsCount = 0
            for (let char of this.inputValue) {
                if (this.digits.has(char)) {
                    digitsCount += 1
                }
            }
            if (digitsCount > 10) {
                this.warningTooLongValue = true
                this.inputValue = this.oldInputValue
            } else {
                this.warningTooLongValue = false
            }
        },
        inputValidationOnInput() {
            //1. Only digits and hyphens
            this.charCheck()
            //2. Not more than two hyphens
            this.twoHyphensCheck()
            //3. Two hyphens can't be together
            this.hyphensTogetherCheck()
            //4. Not more than 10 digits
            this.tooManyDigits()
            this.oldInputValue = this.inputValue
        },
        inputValidationOnBlur() {
            //5. CAS RN validation rule
            let onlyDigits = ""
            for (let char of this.inputValue) {
                if (this.digits.has(char)) {
                    onlyDigits += char
                }
            }
            let sum = 0
            for (let i = 1; i < onlyDigits.length; i++) {
                let j = onlyDigits.length - 1 - i
                sum += Number(onlyDigits[j]) * i
            }
            this.warningInvalidCas = !(Number(onlyDigits.slice(-1)) === sum % 10)
        },
        hideInvalidCasWarning() {
            this.warningInvalidCas = false
        }
    }
}
</script>

<style scoped>

</style>