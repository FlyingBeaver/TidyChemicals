<template>
    <div v-if="showButtons">
        <button
            v-if="statusIsParentName"
            v-on:click="$emit('completeEditing')"
        >Complete editing
        </button>
        <button
            v-on:click="discardChangesClicked"
        >Discard changes
        </button>
    </div>
</template>

<script>
export default {
    name: "TwoButtons",
    inject: ["status"],
    props: ["parentName"],
    emits: ["completeEditing", "discardChanges", "clearEditor"],
    computed: {
        statusIsParentName() {
            return this.status === this.parentName.toLowerCase()
        },
        showButtons() {
            return (
                this.statusIsParentName ||
                this.status === "create"
            )
        },
    },
    methods: {
        discardChangesClicked() {
            if (this.statusIsParentName) {
                this.$emit('discardChanges')
            } else if (this.status === "create") {
                this.$emit('clearEditor')
            }
        },
    },
}
</script>

<style>
</style>
