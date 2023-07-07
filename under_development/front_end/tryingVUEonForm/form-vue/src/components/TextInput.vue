<template>
    <input
        type="text"
        class="simple_text_value"
        v-bind:name="inputName"
        v-bind:disabled="disabled"
    >
</template>


<script>
export default {
    props: ["inputName", "disabled"]
}
</script>