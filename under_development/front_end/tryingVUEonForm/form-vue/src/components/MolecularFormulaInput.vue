<template>
    <input
        type="text"
        class="simple_text_value"
        v-bind:name="inputName"
        v-bind:disabled="disabled"
        v-model="inputValue"
    >
    <div v-bind:class="{warning: true, 'hide-me': !warningWrongChar}">
        You  are trying to enter a symbol that is not allowed in this field
    </div>
    <div v-bind:class="{warning: true, 'hide-me': !warningUnrecognizedElement}">
        Element {{ plural ? "symbols were" : "symbol was" }}
        not recognized: {{unrecognizedSymbols}}
    </div>
    <div v-bind:class="{warning: true, 'hide-me': !warningFirstChar}">
        First character of the molecular formula must be an uppercase latin letter
    </div>
    <div v-bind:class="{warning: true, 'hide-me': !warningDigitLowercase}" >
        After a digits must be an uppercase letter
    </div>
    <input type="hidden" v-model="molecularFormulaJSON">
</template>

<script>
import {elementSymbols} from "@/components/constants"
export default {
    name: "MolecularFormulaInput",
    props: ["inputName", "disabled"],
    data() {
        return {
            plural: false,
            unrecognizedSymbols: "",
            inputValue: "",
            warningWrongChar: false,
            warningUnrecognizedElement: false,
            unrecognizedElementState: false,
            warningFirstChar: false,
            warningDigitLowercase: false,
            uppercaseRE: new RegExp("[A-Z]"),
            lettersDigitsRE: new RegExp("^[A-Za-z0-9]*$"),
            elementSymbolIndexRE: new RegExp("[A-Z][a-z]*[0-9]*", 'g'),
            elementSymbolRE: new RegExp("[A-Z][a-z]*", 'g'),
            onlyLatinRE: new RegExp("[A-Za-z]+"),
            digitLowercaseRE: new RegExp("[0-9][a-z]"),
            watcherStop: false,
        }
    },
    methods: {
        elementsExist(elementsList) {
            if (!elementsList && elementsList === []) {
                return [false, null]
            } else {
                let nonexistentSymbols = []
                for (let i = 0; i < elementsList.length; i++) {
                    if (elementSymbols.indexOf(elementsList[i]) === -1) {
                        nonexistentSymbols.push(elementsList[i])
                    }
                }
                if (nonexistentSymbols.length === 0) {
                    return [true, null]
                } else {
                    return [false, nonexistentSymbols]
                }
            }
        },
        makeJSON(inputText) {
            let result = {}
            let symbolsWithIndicesList = inputText.match(this.elementSymbolIndexRE)
            for (let i = 0; i < symbolsWithIndicesList.length; i++) {
                let symbolWithIndex = symbolsWithIndicesList[i]
                let symbol = symbolWithIndex.match(this.onlyLatinRE)[0]
                if (symbol === symbolWithIndex) {
                    result[symbol] = 1
                } else {
                    let indexString = symbolWithIndex.replace(symbol, "")
                    result[symbol] = Number(indexString)
                }
            }
            return JSON.stringify(result)
        },
        firstCharCheck(inputText) {
            this.warningFirstChar = !inputText[0].match(this.uppercaseRE)
        },
        wrongCharCheck(inputText) {
            this.warningWrongChar = !inputText.match(this.lettersDigitsRE)
        },
        digitLowercaseCheck(inputText) {
            this.warningDigitLowercase = Boolean(inputText.match(this.digitLowercaseRE))
        },
        updateUnrecognizedSymbols(symbolsArr) {
            this.unrecognizedSymbols = symbolsArr.join(", ")
            this.plural = (symbolsArr.length > 1)
        },
        elementsCheck(inputText) {
            let elementsList = inputText.match(this.elementSymbolRE)
            let elementsExistResult = this.elementsExist(elementsList)
            if (elementsExistResult[0]) {
                this.warningUnrecognizedElement = false
            } else {
                this.warningUnrecognizedElement = true
                this.updateUnrecognizedSymbols(elementsExistResult[1])
            }
        },
        setOldValue(oldTextInput) {
            this.watcherStop = true
            this.inputValue = oldTextInput
        },
    },
    watch: {
        inputValue(inputText, oldInputText) {
            if (this.watcherStop) {
                this.watcherStop = false
            } else {
                if (inputText === "") {
                    this.warningWrongChar = false
                    this.warningUnrecognizedElement = false
                } else {
                    this.firstCharCheck(inputText)
                    this.wrongCharCheck(inputText)
                    this.digitLowercaseCheck(inputText)
                    if (!this.warningFirstChar &&
                        !this.warningWrongChar &&
                        !this.warningDigitLowercase
                    ) {
                        this.elementsCheck(inputText)
                    } else {
                        this.setOldValue(oldInputText)
                    }
                }
            }
        }
    },
    computed: {
        molecularFormulaJSON() {
            if (!this.warningDigitLowercase &&
                !this.warningUnrecognizedElement &&
                !this.warningWrongChar &&
                !this.warningFirstChar &&
                (this.inputValue !== "")) {
                return this.makeJSON(this.inputValue)
            } else {
                return ""
            }
        }
    }
}
</script>

<style scoped>

</style>