<template>
    <input type="text" class="simple_text_value" v-bind:name="inputName">
</template>


<script>
export default {
    props: ["inputName"]
}
</script>