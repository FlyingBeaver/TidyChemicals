<template>
    <div>
        <p class="section-header">
            Comment:
        </p>
        <p
            class="name-value"
            v-if="!activateEditors"
            v-html="commentCode"
        ></p>
        <p v-else>
            <text-input-with-format
                ref="TextInputWithFormat"
                v-bind:content="commentCode"
                v-bind:allow-line-break="true"
                v-bind:char-restriction="false"
                v-on:editing-complete="editingCompleteListener"
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
import TextInputWithFormat from "./TextInputWithFormat.vue"
import TwoButtons from "./TwoButtons.vue"
export default {
    name: "Comment",
    components: {TextInputWithFormat, TwoButtons},
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
            if ("comment" in this.editedData) {
                delete this.editedData["comment"]
            }
            this.setChoose()
        },
        clearEditor() {
            this.$refs.TextInputWithFormat.clear()
        },
        localCompleteEditing() {
            this.$refs.TextInputWithFormat.localCompleteEditing()
        },
        editingCompleteListener(data) {
            this.completeEditing("comment", data)
        },
        isValid(object, key) {
            return (
                object !== null &&
                object instanceof Object &&
                key in object
            )
        }
    },
    computed: {
        commentCode() {
            if ('comment' in this.editedData) {
                if (this.isValid(this.editedData.comment, "html")) {
                    return this.editedData.comment.html
                } else {
                    return "<p class='blank-data'>No comment</p>"
                }
            } else if ('comment' in this.initialData) {
                if (this.isValid(this.initialData.comment, "html")) {
                    return this.initialData.comment.html
                } else {
                    return "<p class='blank-data'>No comment</p>"
                }
            } else {
                return "<p></p>"
            }
        },
        commentDelta() {
            if ('comment' in this.editedData) {
                if (this.isValid(this.editedData.comment, "delta")) {
                    return this.editedData.comment.delta
                } else {
                    return {}
                }
            } else if ('comment' in this.initialData) {
                if (this.isValid(this.initialData.comment, "delta")) {
                    return this.initialData.comment.delta
                } else {
                    return {}
                }
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
    },
}
</script>

<style>
p.section-header {
    font-weight: bold;
}
</style>
