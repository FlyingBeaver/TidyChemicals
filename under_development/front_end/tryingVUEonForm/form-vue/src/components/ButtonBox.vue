<template>
    <div class="row" id="buttons_box">
        <button
            class="dark_button"
            id="more_conditions"
            v-on:click.prevent="addCondition"
            v-bind:disabled="deletionMode"
        >Add one more search condition</button>
<!--        <button-->
<!--            class="dark_button"-->
<!--            id="more_conditions_disabled"-->
<!--            disabled-->
<!--        >Add one more search condition</button>-->
        <button
            class="dark_button"
            id="exit_from_deletion"
            v-on:click.prevent="toggleDeletionMode"
            v-if="deletionMode"
        >Exit from deletion mode</button>
        <button
            class="dark_button"
            id="delete_button"
            v-on:click.prevent="toggleDeletionMode"
            v-if="(!deletionMode) && rowsNumber > 1"
        >Delete a search condition</button>
        <button type="submit"
                class="dark_button"
                id="search_button"
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
            console.log(this.subformsCounter)
        },
    },
    props: ["submitForm", "deletionMode", "rowsNumber"]
}
</script>