<template>
    <input type="date" v-bind:name="inputName" v-bind:disabled="disabled" class="simple_text_value">
    <p>
        <input
            type="checkbox"
            v-bind:name="inputName.concat('_include')"
            v-bind:id="inputName.concat('_include')"
            class="checkbox"
        >
        <label
            v-bind:for="inputName.concat('_include')"
        >include date above in the range</label>
    </p>
</template>

<script>
export default {
    name: "DateInput",
    props: ["inputName", "disabled"]
}
</script>

<style>
    input.checkbox {
        margin: 10px;
    }
</style>