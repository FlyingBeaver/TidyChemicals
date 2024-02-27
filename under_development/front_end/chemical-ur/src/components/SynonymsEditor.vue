<template>
    <div>
        <p class="section-header">
            Synonyms:
        </p>
        <p
            ref="listContainer"
            class="name-value"
        >
            <div>
                <div
                    v-if="synonyms.length === 0"
                    class="blank-data"
                >No synonyms
                </div>
                <table>
                    <tr v-for="(syn, index) in synonyms"
                        v-bind:key="index"
                    >
                        <td class="bullet">•</td>
                        <td v-html="syn.html"></td>
                        <td>
                            <button
                                v-if="mode === 'delete' && activateEditors"
                                v-on:click="deleteSynonym(index)"
                                class="small-button"
                            >Delete</button>
                            <button
                                v-if="mode === 'update' && activateEditors"
                                v-on:click="updateSynonym(index)"
                                class="small-button"
                            >Update
                            </button>
                        </td>
                    </tr>
                </table>
            </div>
        </p>
        <p v-if="activateEditors && mode === 'show'">
            <button
                v-on:click="startCreationOfSynonym"
            >Create a synonym
            </button>
            <button
                v-on:click="startUpdateOfSynonym"
            >Change one of synonyms
            </button>
            <button
                v-on:click="startDeletionOfSynonym"
            >Delete a synonym
            </button>
        </p>
        <p v-if="showTextEditor">
            <text-input-with-format
                ref="TextInputWithFormat"
                v-on:editing-complete="editingCompleteListener"
                v-bind:content="nameCode"
                v-bind:allow-line-break="false"
                v-bind:char-restriction="false"
            >
            </text-input-with-format>
            <button
                v-on:click="saveEditingResult"
            >{{ mode === "create" ? "Add the synonym" : "Save changes" }}
            </button>
            <button v-on:click="mode = 'show'">
                Close editor
            </button>
        </p>
        <two-buttons
            v-on:complete-editing="localCompleteEditing"
            v-on:discard-changes="discardChanges"
            v-on:clear-editor="clearEditor"
            v-bind:parent-name="$options.name"
        >
        </two-buttons>
    </div>
    <div>
        <button
            v-if="status === 'choose'"
            v-on:click="localSectionChosen"
        >Edit
        </button>
    </div>
</template>

<script>
import TextInputWithFormat from "./TextInputWithFormat.vue"
import TwoButtons from "./TwoButtons.vue"
import activateEditors from "../mixins/activateEditors.js"
import discardChanges from "../mixins/discardChanges.js"
import clearEditor from "../mixins/clearEditor.js"
import getParentData from "../mixins/getParentData.js"

export default {
    name: "SynonymsEditor",
    components: {TextInputWithFormat, TwoButtons},
    mixins: [
        activateEditors,
        discardChanges,
        clearEditor,
        getParentData,
    ],
    inject: [
        "sectionChosen",
        "completeEditing",
        "setChoose",
        "status",
        "initialData",
        "editedData",
    ],
    data() {
        return {
            mode: 'show',
            localCopyOfSynonyms: null,
            nameCode: "",
            indexOfEdited: null,
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
            return this.parentData(["synonyms"], [])
        },
        showTextEditor() {
            return this.activateEditors &&
            (
                this.mode === 'updateInProcess' ||
                this.mode === 'create'
            )
        },
    },
    methods: {
        discardChanges() {
            this.discardChangesCommon("synonyms")
            this.startEditing()
        },
        clearEditor() {
            if (this.showTextEditor) {
                this.clearEditorCommon(
                    "TextInputWithFormat"
                )
            }
            this.localCopyOfSynonyms = []
            this.mode = "show"
        },
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
            newLocalCopyOfSynonyms.push(...this.globalCopyOfSynonyms)
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
    margin-bottom: 0;
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

