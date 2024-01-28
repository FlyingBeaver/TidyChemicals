<template>
    <div>
        <p class="section-header"
        >
            <span v-if="activateEditors">*</span>
            Name:
        </p>
        <p
            class="name-value"
            v-if="!activateEditors"
            v-html="nameCode"
        ></p>
        <p v-else>
            <text-input-with-format
                ref="TextInputWithFormat"
                v-bind:content="nameCode"
                v-on:editing-complete="editingCompleteListener"
                v-bind:allow-line-break="false"
                v-bind:char-restriction="true"
            >
            </text-input-with-format>
        </p>
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
            v-on:click="sectionChosen($options.name.toLowerCase())"
        >
            Edit
        </button>
    </div>
</template>

<script>
import TextInputWithFormat from "./TextInputWithFormat.vue";
import TwoButtons from "./TwoButtons.vue";
export default {
    name: "Name",
    components: {TwoButtons, TextInputWithFormat},
    inject: [
        "sectionChosen",
        "completeEditing",
        "setChoose",
        "status",
        "initialData",
        "editedData"
    ],
    methods: {
        discardChanges() {
            if ("name_data" in this.editedData) {
                delete this.editedData["name_data"]
            }
            this.setChoose()
        },
        localCompleteEditing() {
            this.$refs.TextInputWithFormat.localCompleteEditing()
        },
        editingCompleteListener(data) {
            this.completeEditing("name_data", data)
        },
        clearEditor() {
            this.$refs.TextInputWithFormat.clear()
        }
    },
    computed: {
        nameCode() {
            if ('name_data' in this.editedData) {
                return this.editedData.name_data.html
            } else if ('name_data' in this.initialData) {
                return this.initialData.name_data.html
            } else {
                return "<p></p>"
            }
        },
        nameDelta() {
            if ('name_data' in this.editedData) {
                return this.editedData.name_data.delta
            } else if ('name_data' in this.initialData) {
                return this.initialData.name_data.delta
            } else {
                return {}
            }
        },
        activateEditors() {
            return (
                this.status === this.$options.name.toLowerCase() ||
                this.status === "create"
            )
        },
    }
}
</script>

<style>
p.section-header {
    font-weight: bold;
}
</style>
