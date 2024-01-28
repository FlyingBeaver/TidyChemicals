<template>
    <div v-if="showButtons">
        <button
            v-on:click="$emit('completeEditing')"
            v-if="statusIsParentName"
        >Complete editing</button>
        <button
            v-on:click="discardChangesClicked"
        >Discard changes</button>
    </div>
</template>

<script>
export default {
    name: "TwoButtons",
    props: ["parentName"],
    inject: ["status"],
    emits: ["completeEditing", "discardChanges", "clearEditor"],
    methods: {
        discardChangesClicked() {
            if (this.statusIsParentName) {
                this.$emit('discardChanges')
            } else if (this.status === "create") {
                this.$emit('clearEditor')
            }
        }
    },
    computed: {
        statusIsParentName() {
            return this.status === this.parentName.toLowerCase()
        },
        showButtons() {
            return (
                this.statusIsParentName ||
                this.status === "create"
            )
        }
    }
}
</script>

<style scoped>

</style>