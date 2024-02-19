<template>
    <div class="buttons-box">
        <button
            class="dark-button"
            v-on:click.prevent="addCondition"
            v-bind:disabled="deletionMode"
        >Add one more search condition</button>
        <button
            class="exit-from-deletion"
            v-on:click.prevent="toggleDeletionMode"
            v-if="deletionMode"
        >Exit from deletion mode</button>
        <button
            class="dark-button"
            v-on:click.prevent="toggleDeletionMode"
            v-if="(!deletionMode) && rowsNumber > 1"
        >Delete a search condition</button>
        <button type="submit"
                class="search-button"
                v-on:click.prevent="submitForm"
        >SEARCH</button>
    </div>
</template>


<script>
export default {
    methods: {
        addCondition() {
            this.$emit("add-condition");
        },
        toggleDeletionMode() {
            this.$emit("toggle-deletion-mode");
        },
    },
    props: ["submitForm", "deletionMode", "rowsNumber"]
}
</script>