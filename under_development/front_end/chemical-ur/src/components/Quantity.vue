<template>
    <div>
        <p class="section-header">
            <span v-if="status === 'quantity'">*</span>
            Quantity:
        </p>
        <p v-if="status !== 'quantity'">
            {{quantity}}
        </p>
        <one-numeral-and-unit
            v-else
            v-bind:unit="unit"
            v-bind:number="number"
            v-bind:units="availableUnits"
            ref="quantityEditor"
        >
        </one-numeral-and-unit>
        <div v-if="status === 'quantity'">
            <button
                v-on:click="localCompleteEditing"
            >Complete editing</button>
            <button
                v-on:click="setChoose"
            >Discard changes</button>
        </div>
    </div>
    <div>
        <button
            v-if="status === 'choose'"
            v-on:click="showEditor"
        >
            Edit
        </button>
    </div>
</template>

<script>
import OneNumeralAndUnit from "./OneNumeralAndUnit.vue";
export default {
    name: "Quantity",
    props: ["status", "initialData", "editedData"],
    inject: ["sectionChosen", "completeEditing", "setChoose"],
    components: {OneNumeralAndUnit},
    data() {
        return {
            unitsAddress: "http://127.0.0.1:5000/units/",
            availableUnits: []
        }
    },
    methods: {
        async showEditor() {
            let response = await fetch(this.unitsAddress)
            this.availableUnits = await response.json()
            this.sectionChosen("quantity")
        },
        localCompleteEditing() {
            this.$refs.quantityEditor.localCompleteEditing()
        }
    },
    computed: {
        quantity() {
            return this.number + " " + this.unit
        },
        number() {
            if ("quantity" in this.editedData) {
                return this.editedData.quantity.number
            } else if ("quantity" in this.initialData) {
                return this.initialData.quantity.number
            }
        },
        unit() {
            if ("quantity" in this.editedData) {
                return this.editedData.quantity.unit
            } else if ("quantity" in this.initialData) {
                return this.initialData.quantity.unit
            }
        },
    }
}
</script>

<style scoped>

</style>