<template>
    <input
        type="date"
        class="simple-text-input"
        v-bind:name="inputName"
        v-bind:disabled="disabled">
</template>

<script>
export default {
    name: "DateInput",
    props: ["inputName", "disabled"]
}
</script>

<style>
</style>