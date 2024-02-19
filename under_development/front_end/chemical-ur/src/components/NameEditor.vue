<template>
    <div>
        <p class="section-header">
            <span v-if="activateEditors">*</span>
            Name:
        </p>
        <p
            v-if="!activateEditors"
            v-html="nameCode"
            class="name-value"
        ></p>
        <p v-else>
            <text-input-with-format
                ref="TextInputWithFormat"
                v-on:editing-complete="editingCompleteListener"
                v-bind:content="nameCode"
                v-bind:allow-line-break="false"
                v-bind:char-restriction="true"
            >
            </text-input-with-format>
        </p>
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
            v-on:click="sectionChosen($options.name.toLowerCase())"
        >
            Edit
        </button>
    </div>
</template>

<script>
import TextInputWithFormat from "./TextInputWithFormat.vue"
import TwoButtons from "./TwoButtons.vue"
import activateEditors from "../mixins/activateEditors.js"
import discardChanges from "../mixins/discardChanges.js"
import clearEditor from "../mixins/clearEditor.js"
import localCompleteEditing from "../mixins/localCompleteEditing.js"
import getParentData from "../mixins/getParentData.js";

export default {
    name: "NameEditor",
    components: {TwoButtons, TextInputWithFormat},
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
        "status",
        "initialData",
        "editedData"
    ],
    computed: {
        nameCode() {
            return this.parentData(
                ['name_data', 'html'], "<p></p>"
            )
        },
        nameDelta() {
            return this.parentData(
                ["name_data", "delta"], {}
            )
        },
    },
    methods: {
        editingCompleteListener(data) {
            this.completeEditing("name_data", data)
        },
    },
}
</script>

<style>
p.section-header {
    font-weight: bold;
}
</style>
