<template>
    <div>
        <p class="section-header">
            Comment:
        </p>
        <p
            class="name-value"
            v-if="status !== 'comment'"
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
        <div
            v-if="status === 'comment'"
        >
            <button v-on:click="localCompleteEditing">Complete editing</button>
            <button v-on:click="setChoose">Discard changes</button>
        </div>
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
export default {
    name: "Comment",
    components: {TextInputWithFormat},
    props: ["status", "initialData", "editedData"],
    inject: ["sectionChosen", "completeEditing", "setChoose"],
    methods: {
        localCompleteEditing() {
            this.$refs.TextInputWithFormat.localCompleteEditing()
        },
        editingCompleteListener(data) {
            this.completeEditing("comment", data)
        }
    },
    computed: {
        commentCode() {
            if ('comment' in this.editedData) {
                return this.editedData.comment.html
            } else if ('comment' in this.initialData) {
                return this.initialData.comment.html
            } else {
                return null
            }
        },
        commentDelta() {
            if ('comment' in this.editedData) {
                return this.editedData.comment.delta
            } else if ('comment' in this.initialData) {
                return this.initialData.comment.delta
            } else {
                return null
            }
        }
    }
}
</script>

<style>
p.section-header {
    font-weight: bold;
}
</style>
