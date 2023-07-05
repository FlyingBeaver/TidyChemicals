<template>
    <button
        class="dark_button"
        v-on:click.prevent="toggleEditor"
    >{{ editorIsOn ? "Hide editor" : "Show editor" }}</button>
</template>

<script>
export default {
    name: "StructureInputToggle",
    methods:
        {
            toggleEditor() {
                this.editorIsOn = !this.editorIsOn
                this.$emit("toggle-editor")
            }
        },
    data() {
        return {
            editorIsOn: false,
        }
    },
    emits:
        ["toggle-editor"]
}
</script>

<style>

</style>