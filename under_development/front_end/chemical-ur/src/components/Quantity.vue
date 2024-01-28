<template>
    <div>
        <p class="section-header">
            <span v-if="activateEditors">*</span>
            Quantity:
        </p>
        <p v-if="!activateEditors">
            {{quantity}}
        </p>
        <one-numerical-and-unit
            v-else
            v-bind:unit="unit"
            v-bind:number="number"
            v-bind:units="availableUnits"
            ref="quantityEditor"
        >
        </one-numerical-and-unit>
        <two-buttons
            v-bind:parent-name="$options.name"
            v-on:complete-editing="localCompleteEditing"
            v-on:discard-changes="discardChanges"
            v-on:clear-editor="clearEditor"
        ></two-buttons>
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
import TwoButtons from "./TwoButtons.vue"
import OneNumericalAndUnit from "./OneNumericalAndUnit.vue"
export default {
    name: "Quantity",
    inject: [
        "sectionChosen",
        "completeEditing",
        "setChoose",
        "URLsSettings",
        "status",
        "initialData",
        "editedData",
    ],
    components: {OneNumericalAndUnit, TwoButtons},
    data() {
        return {
            availableUnits: [],
        }
    },
    methods: {
        discardChanges() {
            if ("quantity" in this.editedData) {
                delete this.editedData["quantity"]
            }
            this.setChoose()
        },
        async showEditor() {
            let response = await fetch(this.URLsSettings.unitsURL)
            this.availableUnits = await response.json()
            this.sectionChosen("quantity")
        },
        localCompleteEditing() {
            this.$refs.quantityEditor.localCompleteEditing()
        },
        clearEditor() {
            this.$refs.quantityEditor.clear()
        },
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
            } else {
                return ""
            }
        },
        unit() {
            if ("quantity" in this.editedData) {
                return this.editedData.quantity.unit
            } else if ("quantity" in this.initialData) {
                return this.initialData.quantity.unit
            } else {
                return ""
            }
        },
        activateEditors() {
            return (
                this.status === this.$options.name.toLowerCase() ||
                this.status === "create"
            )
        },
    },
    async created() {
        if (this.status === "create") {
            let response = await fetch(this.URLsSettings.unitsURL)
            this.availableUnits = await response.json()
        }
    }
}
</script>

<style scoped>

</style>