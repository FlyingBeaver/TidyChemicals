<template>
    <input
        type="text"
        class="simple-text-input"
        v-bind:name="inputName"
        v-bind:disabled="disabled"
    >
</template>


<script>
export default {
    props: ["inputName", "disabled"]
}
</script>