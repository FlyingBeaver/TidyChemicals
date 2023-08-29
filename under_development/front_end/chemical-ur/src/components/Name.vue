<template>
    <div>
        <p class="section-header">
            <span v-if="status === 'name'">*</span>
            Name:
        </p>
        <p
            class="name-value"
            v-if="status !== 'name'"
            v-html="nameCode"
        ></p>
        <p v-else>
            <text-input-with-format
                ref="TextInputWithFormat"
                v-bind:content="nameDelta"
            >
            </text-input-with-format>
        </p>
    </div>
    <div>
        <button
            v-if="status === 'choose'"
            v-on:click="sectionChosen($options.name.toLowerCase())"
        >
            Edit
        </button>
    </div>
    <div
        v-if="status === 'name'"
    >
        <button v-on:click="completeEditing">Complete Editing</button>
    </div>
</template>

<script>
import TextInputWithFormat from "./TextInputWithFormat.vue";
export default {
    name: "Name",
    components: {TextInputWithFormat},
    props: ["status", "initialData", "editedData"],
    inject: ["sectionChosen"],
    methods: {
        completeEditing() {
            this.$refs.TextInputWithFormat.localCompleteEditing()
        }
    },
    computed: {
        nameCode() {
            if ('name_code' in this.editedData) {
                return this.editedData.name_code
            } else {
                return this.initialData.name_code
            }
        },
        nameDelta() {
            if ('name_delta' in this.editedData) {
                return this.editedData.name_delta
            } else {
                return this.initialData.name_delta
            }
        }
    }
}
</script>

<style scoped>

</style>