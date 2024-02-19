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
            ref="quantityEditor"
            v-bind:unit="unit"
            v-bind:number="number"
            v-bind:units="availableUnits"
        >
        </one-numerical-and-unit>
        <two-buttons
            v-on:complete-editing="localCompleteEditing"
            v-on:discard-changes="discardChanges"
            v-on:clear-editor="clearEditor"
            v-bind:parent-name="$options.name"
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
import activateEditors from "../mixins/activateEditors.js"
import discardChanges from "../mixins/discardChanges.js"
import clearEditor from "../mixins/clearEditor.js"
import localCompleteEditing from "../mixins/localCompleteEditing.js"
import getParentData from "../mixins/getParentData.js"

export default {
    name: "QuantityEditor",
    components: {OneNumericalAndUnit, TwoButtons},
    mixins: [
        activateEditors,
        discardChanges,
        clearEditor,
        localCompleteEditing,
        getParentData,
    ],
    inject: [
        "sectionChosen",
        "completeEditing",
        "setChoose",
        "URLsSettings",
        "status",
        "initialData",
        "editedData",
    ],
    data() {
        return {
            availableUnits: [],
        }
    },
    computed: {
        quantity() {
            return this.number + " " + this.unit
        },
        number() {
            return this.parentData(["quantity", "number"], "")
        },
        unit() {
            return this.parentData(["quantity", "unit"], "")
        },
    },
    async created() {
        if (this.status === "create") {
            let response = await fetch(this.URLsSettings.unitsURL)
            this.availableUnits = await response.json()
        }
    },
    methods: {
        async showEditor() {
            let response = await fetch(this.URLsSettings.unitsURL)
            this.availableUnits = await response.json()
            this.sectionChosen("quantityeditor")
        },
    },
}
</script>

<style scoped>

</style>