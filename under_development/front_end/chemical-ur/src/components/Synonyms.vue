<template>
    <div>
        <p class="section-header">
            Synonyms:
        </p>
        <p
            class="name-value"
            ref="listContainer"
        >
            <div>
                <table>
                    <tr v-for="(syn, index) in synonyms">
                        <td class="bullet">•</td>
                        <td v-html="syn.html"></td>
                        <td>
                            <button
                                v-on:click="deleteSynonym(index)"
                                v-if="mode === 'delete' && status === 'synonyms'"
                                class="small-button"
                            >Delete</button>
                            <button
                                v-on:click="updateSynonym(index)"
                                v-if="mode === 'update' && status === 'synonyms'"
                                class="small-button"
                            >Update</button>
                        </td>
                    </tr>
                </table>
            </div>
        </p>
        <p v-if="status === 'synonyms' && mode === 'show'">
            <button
                v-on:click="startCreationOfSynonym"
            >Create a synonym</button>
            <button
                v-on:click="startUpdateOfSynonym"
            >Change one of synonyms</button>
            <button
                v-on:click="startDeletionOfSynonym"
            >Delete a synonym</button>
        </p>
        <p v-if="status === 'synonyms' && (mode === 'updateInProcess' || mode === 'create')">
            <text-input-with-format
                ref="TextInputWithFormat"
                v-bind:content="nameCode"
                v-on:editing-complete="editingCompleteListener"
                v-bind:allow-line-break="false"
                v-bind:char-restriction="false"
            >
            </text-input-with-format>
            <button v-on:click="saveEditingResult"
            >{{ mode === "create" ? "Add the synonym" : "Save changes" }}</button>
            <button v-on:click="mode = 'show'">Discard changes</button>
        </p>
        <div
            v-if="status === 'synonyms' && mode !== 'updateInProcess' && mode !== 'create'"
        >
            <button v-on:click="localCompleteEditing">Complete Editing</button>
            <button v-on:click="exitWithoutSaving">Discard changes</button>
        </div>
    </div>
    <div>
        <button
            v-if="status === 'choose'"
            v-on:click="localSectionChosen"
        >
            Edit
        </button>
    </div>
</template>

<script>
import TextInputWithFormat from "./TextInputWithFormat.vue"
import {toRaw} from "vue";
export default {
    name: "Synonyms",
    components: {TextInputWithFormat},
    props: ["status", "initialData", "editedData"],
    inject: ["sectionChosen", "completeEditing", "setChoose"],
    data() {
        return {
            mode: 'show',
            localCopyOfSynonyms: null,
            nameCode: "",
            indexOfEdited: null,
        }
    },
    methods: {
        startCreationOfSynonym() {
            this.mode = 'create'
            this.nameCode = ''
            this.ensureThatLCOSisNotNull()
        },
        startUpdateOfSynonym() {
            this.mode = 'update'
            this.ensureThatLCOSisNotNull()
        },
        startDeletionOfSynonym() {
            this.mode = 'delete'
            this.ensureThatLCOSisNotNull()
        },
        ensureThatLCOSisNotNull() {
            if (this.localCopyOfSynonyms === null) {
                this.startEditing()
            }
        },
        localSectionChosen() {
            this.sectionChosen(this.$options.name.toLowerCase())
            this.startEditing()
        },
        exitWithoutSaving() {
            this.localCopyOfSynonyms = null
            if (this.status !== 'choose') {
                this.setChoose()
            }
        },
        saveEditingResult() {
            this.$refs.TextInputWithFormat.localCompleteEditing()
        },
        startEditing() {
            let newLocalCopyOfSynonyms = []
            for (let i = 0; i < this.globalCopyOfSynonyms.length; i++) {
                newLocalCopyOfSynonyms.push(toRaw(this.globalCopyOfSynonyms[i]))
            }
            this.localCopyOfSynonyms = newLocalCopyOfSynonyms
        },
        localCompleteEditing() {
            this.mode = 'show'
            this.completeEditing("synonyms", this.localCopyOfSynonyms)
        },
        editingCompleteListener(data) {
            if (this.mode === 'updateInProcess') {
                this.localCopyOfSynonyms[this.indexOfEdited] = data
                this.mode = 'show'
            } else if (this.mode === 'create') {
                this.localCopyOfSynonyms.push(data)
                this.mode = 'show'
            }
        },
        deleteSynonym(index) {
            this.localCopyOfSynonyms.splice(index, 1)
        },
        updateSynonym(index) {
            this.mode = 'updateInProcess'
            this.nameCode = this.synonyms[index].html
            this.indexOfEdited = index
        }
    },
    computed: {
        synonyms() {
            if (this.localCopyOfSynonyms) {
                return this.localCopyOfSynonyms
            } else {
                return this.globalCopyOfSynonyms
            }
        },
        globalCopyOfSynonyms() {
            if ('synonyms' in this.editedData) {
                return this.editedData.synonyms
            } else if ('synonyms' in this.initialData) {
                return this.initialData.synonyms
            } else {
                return null
            }
        },
    },
}
</script>

<style scoped>
p.section-header {
    font-weight: bold;
}
button.small-button {
    margin-left: 20px;
}

table, td {
    border: 0;
}
td > p {
    margin-top: 0;
    margin-bottom: 0;
}

td.bullet {
    padding-left: 10px;
    padding-right: 10px;
    font-weight: bold;
}
</style>

