<template>
    <div>
        <p class="section-header">
            <span>*</span>
            Water number:
        </p>
        <div>
            <select v-model="waterNumberType">
                <option value="dry" selected>Dry substance</option>
                <option value="whole">Whole water number</option>
                <option value="fractional">Fractional water number</option>
            </select>
            <p v-if="waterNumberType === 'whole'"
               class="water-number-container"
            >
                <span>Water number:</span>
                <input
                    v-on:input="validateWaterNumber"
                    v-on:cut="validateWaterNumber"
                    v-on:copy="validateWaterNumber"
                    v-on:paste="validateWaterNumber"
                    v-model="waterNumber"
                    type="text"
                />
            </p>
            <p
                v-if="waterNumberType === 'fractional'"
                class="water-number-container"
            >
                <span>Numerator:</span>
                <input
                    v-model="numerator"
                    v-on:input="validateNumerator"
                    v-on:cut="validateNumerator"
                    v-on:copy="validateNumerator"
                    v-on:paste="validateNumerator"
                    type="text"
                />
                <span>Denominator:</span>
                <input
                    v-model="denominator"
                    v-on:input="validateDenominator"
                    v-on:cut="validateDenominator"
                    v-on:copy="validateDenominator"
                    v-on:paste="validateDenominator"
                    type="text"
                />
            </p>
            <p
                v-show="leadingZeroWarning"
                class="warning"
            >
                This number can't start with zero
            </p>
            <p
                v-show="oddCharsWarning"
                class="warning"
            >
                Only digits are allowed
            </p>
            <p
                v-show="emptyFieldWarning"
                class="warning"
            >
                {{ waterNumberType === "whole"
                       ? "Water number field "
                       : "" }}
                {{ waterNumberType === "fractional"
                       ? "Both numerator and denominator fields "
                       : "" }}
                must be filled
            </p>
            <p
                v-show="denominatorIsOneWarning"
                class="warning"
            >
                Denominator can not be 1
            </p>
            <p
                v-show="cancellableFractionWarning"
                class="warning"
            >
                The fraction can be cancelled: both numerator
                and denominator can be divided by
                {{ greatestCommonDivisor }}
            </p>
            <p
                v-show="wholeNumberWarning"
                class="warning"
            >
                The fraction represents the whole number
            </p>
        </div>
        <two-buttons
            v-on:complete-editing="localCompleteEditing"
            v-on:discard-changes="discardChanges"
            v-on:clear-editor="clearEditor"
            v-bind:parent-name="$options.name"
            class="bottom"
        ></two-buttons>
    </div>
    <div>
    </div>
</template>

<script>
import {difference} from "../utils/constants.js"
import TwoButtons from "./TwoButtons.vue"

export default {
    name: "WaterNumber",
    components: {TwoButtons},
    inject: [
        "sectionChosen",
        "completeEditing",
        "setChoose",
        "status",
        "initialData",
        "editedData",
    ],
    data() {
        return {
            waterNumberType: "dry",
            waterNumber: "",
            numerator: "",
            denominator: "",
            oldWaterNumber: "",
            oldNumerator: "",
            oldDenominator: "",
            digits: new Set("0123456789"),
            oddCharsWarning: false,
            leadingZeroWarning: false,
            emptyFieldWarning: false,
            denominatorIsOneWarning: false,
            cancellableFractionWarning: false,
            wholeNumberWarning: false,
            greatestCommonDivisor: 1,
        }
    },
    mounted() {
        let structureAq = null
        if ("structure_aq" in this.editedData) {
            structureAq = this.editedData.structure_aq
        } else if ("structure_aq" in this.initialData) {
            structureAq = this.initialData.structure_aq
        }
        if (structureAq === null) {
            this.waterNumberType = "dry"
        } else if (Number.isInteger(Number(structureAq))) {
            this.waterNumberType = "whole"
            this.waterNumber = String(structureAq)
            this.oldWaterNumber = String(structureAq)
        } else if (Array.isArray(structureAq) && structureAq.length === 2) {
            this.waterNumberType = "fractional"
            this.numerator = String(structureAq[0])
            this.denominator = String(structureAq[1])
            this.oldNumerator = String(structureAq[0])
            this.oldDenominator = String(structureAq[1])
        } else {
            throw Error("Wrong structure_aq format!")
        }
    },
    methods: {
        validateWaterNumber() {
            this.hideWarnings()
            this.oddCharsWarning = !this.containsOnlyDigits(this.waterNumber)
            this.leadingZeroWarning = this.waterNumber[0] === "0"
            if (this.oddCharsWarning || this.leadingZeroWarning) {
                this.waterNumber = this.oldWaterNumber
            } else {
                this.oldWaterNumber = this.waterNumber
            }
        },
        validateNumerator() {
            this.hideWarnings()
            this.oddCharsWarning = !this.containsOnlyDigits(this.numerator)
            this.leadingZeroWarning = this.numerator[0] === "0"
            if (this.oddCharsWarning || this.leadingZeroWarning) {
                this.numerator = this.oldNumerator
            } else {
                this.oldNumerator = this.numerator
            }
            this.fractionCheck()
        },
        validateDenominator() {
            this.hideWarnings()
            this.oddCharsWarning = !this.containsOnlyDigits(this.denominator)
            this.leadingZeroWarning = this.denominator[0] === "0"
            if (this.oddCharsWarning || this.leadingZeroWarning) {
                this.denominator = this.oldDenominator
            } else {
                this.oldDenominator = this.denominator
            }
            this.denominatorIsOneWarning = this.denominator === "1"
            this.fractionCheck()
        },
        fractionCheck() {
            if (this.numerator !== "" && this.denominator !== "") {
                this.wholeNumberWarning = this.wholeNumberCheck()
                if (!this.wholeNumberWarning) {
                    this.cancellableFractionWarning = this.cancellableFractionCheck()
                }
            }
        },
        cancellableFractionCheck() {
            let numerator = Number(this.numerator)
            let denominator = Number(this.denominator)
            this.greatestCommonDivisor = this.gcd(numerator, denominator)
            return this.greatestCommonDivisor !== 1
        },
        wholeNumberCheck() {
            let numerator = Number(this.numerator)
            let denominator = Number(this.denominator)
            if (numerator === denominator) {
                return true
            } else if (numerator > denominator) {
                let remainder = numerator % denominator
                return remainder === 0
            } else {
                return false
            }
        },
        gcd(a, b) {
            let greater = Math.max(a, b)
            let lesser = Math.min(a, b)
            let remainder = greater % lesser
            while (remainder > 0) {
                greater = lesser
                lesser = remainder
                remainder = greater % lesser
            }
            return lesser
        },
        discardChanges() {
            if ("structure_aq" in this.editedData) {
                delete this.editedData["structure_aq"]
            }
            this.setChoose()
        },
        localCompleteEditing() {
            if (!this.allFieldsFilled()) {
                return null
            }

            if (this.waterNumberType === "dry") {
                this.completeEditing("structure_aq", null)
            } else if (this.waterNumberType === "whole") {
                let waterNumberInt = Number(this.waterNumber)
                if (isNaN(waterNumberInt)) {
                    throw Error("water number is NaN")
                }
                this.completeEditing("structure_aq", waterNumberInt)
            } else if (this.waterNumberType === "fractional") {
                let numeratorInt = Number(this.numerator)
                let denominatorInt = Number(this.denominator)
                if (isNaN(numeratorInt) || isNaN(denominatorInt)) {
                    throw Error("numerator or denominator is NaN")
                }
                this.completeEditing(
                    "structure_aq",
                    [numeratorInt, denominatorInt]
                )
            }
        },
        containsOnlyDigits(text) {
            let textSet = new Set(text)
            return (
                text === "" ||
                difference(textSet, this.digits).size === 0
            )
        },
        hideWarnings() {
            this.oddCharsWarning = false
            this.leadingZeroWarning = false
            this.emptyFieldWarning = false
            this.denominatorIsOneWarning = false
            this.cancellableFractionWarning = false
            this.wholeNumberWarning = false
        },
        allFieldsFilled() {
            if (this.waterNumberType === "whole" && this.waterNumber === "") {
                this.emptyFieldWarning = true
                return false
            } else if (this.waterNumberType === "fractional" &&
                (this.numerator === "" || this.denominator === "")
            ) {
                this.emptyFieldWarning = true
                return false
            } else {
                return true
            }
        },
        clearEditor() {
            this.waterNumberType = "dry"
            this.waterNumber = ""
            this.numerator = ""
            this.denominator = ""
        },
    },
}
</script>

<style>
    button.bottom {
        margin-top: 10px;
    }

    p.water-number-container {
        display: grid;
        grid-template-columns: 1fr 40px;
        width: 150px
    }

    p.warning {
        background: peachpuff;
        margin: 10px 10px 10px 10px;
        font-family: sans-serif;
        color: maroon;
        padding: 10px 10px 10px 10px;
    }
</style>