<template>
    <input
        v-model="inputValue"
        v-on:blur="actionOnBlur"
        v-on:focus="hideInvalidCasWarning"
        v-on:input="inputValidationOnInput"
        v-on:cut="inputValidationOnInput"
        v-on:copy="inputValidationOnInput"
        v-on:paste="inputValidationOnInput"
        type="text"
        class="simple_text_value"
    >
    <div
        v-show="warningWrongSymbol"
        class="warning"
    >
        You  are trying to enter a symbol that is not allowed in
        this field
    </div>
    <div
        v-show="warningInvalidCas"
        class="warning"
    >
        Invalid value of CAS RN. If you didn't completed input of CAS RN,
        you can ignore this message
    </div>
    <div
        v-show="warningTooLongValue"
        class="warning"
    >
        You are trying to input too long value for CAS RN. Valid CAS RN
        can't contain more than 10 digits.
    </div>
    <div
        v-show="warningThreeHyphens"
        class="warning"
    >
        You  are trying to enter third hyphen, but CAS RN can contain
        only two hyphens
    </div>
    <div
         v-show="warningHyphensTogether"
         class="warning"
    >
        You  are trying to enter two hyphens together, but hyphens must
        separate groups of digits
    </div>
    <div
        v-show="warningStartsWithZero"
        class="warning"
    >
        You  are trying to enter value that starts with zero, but CAS RN
        can't start with zero
    </div>
</template>

<script>
export default {
    name: "CasInput",
    inject: ["completeEditing"],
    props: ["cas"],
    emits: ["discardChanges"],
    data() {
        return {
            expectedSymbols: new Set("0123456789-"),
            digits: new Set("0123456789"),
            oldInputValue: this.cas,
            inputValue: this.cas,
            warningInvalidCas: false,
            warningTooLongValue: false,
            warningWrongSymbol: false,
            warningThreeHyphens: false,
            warningHyphensTogether: false,
            warningStartsWithZero: false,
        }
    },
    methods: {
        clear() {
            this.inputValue = ""
            this.warningInvalidCas = false
            this.warningTooLongValue = false
            this.warningWrongSymbol = false
            this.warningThreeHyphens = false
            this.warningHyphensTogether = false
            this.warningStartsWithZero = false
        },
        localCompleteEditing() {
            this.completeEditing("cas", this.inputValue)
        },
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
        cantStartWithZeroCheck() {
            if (this.inputValue[0] === "0") {
                this.warningStartsWithZero = true
                this.inputValue = this.oldInputValue
            } else {
                this.warningStartsWithZero = false
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
            //5. Can't start with zero
            this.cantStartWithZeroCheck()
            this.oldInputValue = this.inputValue
        },
        actionOnBlur(event) {
            let relTarget = event.relatedTarget
            if (!(relTarget &&
                  (relTarget.textContent.trim() === "Discard changes" ||
                   relTarget.textContent.trim() === "Complete editing")
                  )
            ) {
                this.inputValidationOnBlur()
            }
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
        },
    },
}
</script>

<style>
</style>
