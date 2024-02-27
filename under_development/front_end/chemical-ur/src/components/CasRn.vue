<template>
    <div>
        <p class="section-header">
            CAS RN:
        </p>
        <p v-if="!activateEditors"
           v-bind:class="{'blank-data': casRn === ''}"
        >
            {{casRn === '' ? 'No CAS RN!' : casRn}}
        </p>
        <cas-input
            v-else
            ref="casInput"
            v-bind:cas="casRn"
            v-on:discard-changes="discardChanges"
        ></cas-input>
        <two-buttons
            v-on:complete-editing="completeEditing"
            v-on:discard-changes="discardChanges"
            v-on:clear-editor="clearEditor"
            v-bind:parent-name="$options.name"
        ></two-buttons>
    </div>
    <div>
        <button
            v-if="status === 'choose'"
            v-on:click="sectionChosen('casrn')"
        >
            Edit
        </button>
    </div>
</template>

<script>
import CasInput from "./CasInput.vue"
import TwoButtons from "./TwoButtons.vue"
import activateEditors from "../mixins/activateEditors.js"
import getParentData from "../mixins/getParentData.js"
import discardChanges from "../mixins/discardChanges.js"
import clearEditor from "../mixins/clearEditor.js"
import localCompleteEditing from "../mixins/localCompleteEditing.js"

export default {
    name: "CasRn",
    components: {CasInput, TwoButtons},
    mixins: [
        activateEditors,
        discardChanges,
        getParentData,
        clearEditor,
        localCompleteEditing,
    ],
    inject: [
        "sectionChosen",
        "setChoose",
        "status",
        "initialData",
        "editedData",
    ],
    computed: {
        casRn() {
            return String(this.parentData(["cas"], ""))
        },
    },
    methods: {
        completeEditing() {
            this.$refs.casInput.inputValidationOnBlur()
            if (!this.$refs.casInput.warningInvalidCas) {
                this.localCompleteEditing()
            }
        }
    },
}
</script>

<style>
</style>