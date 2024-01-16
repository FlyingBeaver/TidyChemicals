<template>
    <div>
        <p class="section-header">
            CAS RN:
        </p>
        <p v-if="status !== 'casrn'">
            {{casRn}}
        </p>
        <cas-input
            v-else
            v-bind:cas="casRn"
            ref="casInput"
        ></cas-input>
        <p v-if="status === 'casrn'">
            <button v-on:click="localCompleteEditing">Complete editing</button>
            <button v-on:click="setChoose">Discard changes</button>
        </p>
    </div>
    <div>
        <button
            v-if="status === 'choose'"
            v-on:click="sectionChosen('casrn')"
        >
            Edit
        </button>
    </div>
</template>

<script>
import CasInput from "./CasInput.vue";
export default {
    name: "CasRn",
    components: {CasInput},
    props: ["status", "initialData", "editedData"],
    inject: ["sectionChosen", "completeEditing", "setChoose"],
    methods: {
        localCompleteEditing() {
            this.$refs.casInput.localCompleteEditing()
        },
    },
    computed: {
        casRn() {
            if ("cas" in this.editedData) {
                return this.editedData.cas
            } else if ("cas" in this.initialData) {
                return this.initialData.cas
            }
        }
    }
}
</script>

<style scoped>

</style>