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
                <input type="text"
                       v-model="waterNumber"
                       v-on:input="hideWarnings"
                >
            </p>
            <p v-if="waterNumberType === 'fractional'"
               class="water-number-container"
            >
                <span>Numerator:</span>
                <input type="text"
                       v-model="numerator"
                       v-on:input="hideWarnings"
                >
                <span>Denominator:</span>
                <input type="text"
                       v-model="denominator"
                       v-on:input="hideWarnings"
                >
            </p>
            <p class="warning" v-show="leadingZeroWarning">
                This number can't start with zero
            </p>
            <p class="warning" v-show="oddCharsWarning">
                Only digits are allowed
            </p>
            <p class="warning" v-show="emptyFieldWarning">
                {{ waterNumberType === "whole" ? "Water number field " : "" }}
                {{ waterNumberType === "fractional" ? "Both numerator and denominator fields " : "" }}
                must be filled
            </p>
        </div>
        <div>
            <button
                v-on:click="localCompleteEditing"
                class="bottom"
            >Complete editing</button>
            <button
                v-on:click="setChoose"
                class="bottom"
            >Discard changes</button>
        </div>
    </div>
    <div>
    </div>
</template>

<script>
export default {
    name: "WaterNumber",
    props: ["status", "initialData", "editedData"],
    inject: ["sectionChosen", "completeEditing", "setChoose"],
    data() {
        return {
            waterNumberType: "dry",
            waterNumber: "",
            numerator: "",
            denominator: "",
            digits: new Set("0123456789"),
            oddCharsWarning: false,
            leadingZeroWarning: false,
            emptyFieldWarning: false,
        }
    },
    methods: {
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
                this.completeEditing("structure_aq", [numeratorInt, denominatorInt])
            }
        },
        difference(setA, setB) {
            const _difference = new Set(setA);
            for (const elem of setB) {
                _difference.delete(elem);
            }
            return _difference;
        },
        containsOnlyDigits(text) {
            let textSet = new Set(text)
            return this.difference(textSet, this.digits).size === 0
        },
        hideWarnings() {
            this.oddCharsWarning = false
            this.leadingZeroWarning = false
            this.emptyFieldWarning = false
        },
        commonWatcher(newVal, oldVal, watcherName) {
            if (!this.containsOnlyDigits(newVal)) {
                this[watcherName] = oldVal
                this.oddCharsWarning = true
            }
            if (newVal[0] === "0") {
                this[watcherName] = oldVal
                this.leadingZeroWarning = true
            }
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
        }
    },
    watch: {
        waterNumber(newValue, oldValue) {
            this.commonWatcher(newValue, oldValue, "waterNumber")
        },
        numerator(newValue, oldValue) {
            this.commonWatcher(newValue, oldValue, "numerator")
        },
        denominator(newValue, oldValue) {
            this.commonWatcher(newValue, oldValue, "denominator")
        },
    },
    mounted() {
        let structureAq = null
        if ("structure_aq" in this.editedData) {
            structureAq = this.editedData.structure_aq
        } else if ("structure_aq" in this.initialData) {
            structureAq = this.initialData.structure_aq
        } else {
            throw Error("No structure_aq data!")
        }
        if (structureAq === null) {
            this.waterNumberType = "dry"
        } else if (Number.isInteger(Number(structureAq))) {
            this.waterNumberType = "whole"
            this.waterNumber = String(structureAq)
        } else if (Array.isArray(structureAq) && structureAq.length === 2) {
            this.waterNumberType = "fractional"
            this.numerator = String(structureAq[0])
            this.denominator = String(structureAq[1])
        } else {
            throw Error("Wrong structure_aq format!")
        }
    }
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