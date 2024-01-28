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
            v-bind:cas="casRn"
            ref="casInput"
        ></cas-input>
        <two-buttons
            v-bind:parent-name="$options.name"
            v-on:complete-editing="localCompleteEditing"
            v-on:discard-changes="discardChanges"
            v-on:clear-editor="clearEditor"
        ></two-buttons>
    </div>
    <div>
        <button
            v-if="activateEditors"
            v-on:click="sectionChosen('casrn')"
        >
            Edit
        </button>
    </div>
</template>

<script>
import CasInput from "./CasInput.vue"
import TwoButtons from "./TwoButtons.vue";
export default {
    name: "CasRn",
    components: {CasInput, TwoButtons},
    inject: [
        "sectionChosen",
        "completeEditing",
        "setChoose",
        "status",
        "initialData",
        "editedData",
    ],
    methods: {
        discardChanges() {
            if ("cas" in this.editedData) {
                delete this.editedData["cas"]
            }
        },
        clearEditor() {
            this.$refs.casInput.clear()
        },
        localCompleteEditing() {
            this.$refs.casInput.localCompleteEditing()
        },
    },
    computed: {
        casRn() {
            if ("cas" in this.editedData && this.editedData.cas !== null) {
                return this.editedData.cas
            } else if ("cas" in this.initialData && this.initialData.cas !== null) {
                return this.initialData.cas
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
}
</script>

<style scoped>

</style>