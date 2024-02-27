<template>
    <div>
        <p class="section-header">
            Structure:
        </p>
        <div
            v-if="!activateEditors"
            class="structure-body"
        >
            <img
                v-if="structurePic"
                v-bind:src="structurePic"
                v-bind:alt="structureName"
            >
            <div
                v-else
                class="blank-data"
            >No structural formula</div>
            <span
                v-if="showWaterNumber"
                class="water-number"
            >
                <span class="dot">⋅</span>
                <span
                    v-if="waterNumberType === 'fractional'"
                    class="fraction"
                >
                    <span>{{numerator}}</span>
                    <span class="fraction-line"></span>
                    <span>{{denominator}}</span>
                </span>
                <span class="h2o">
                    {{waterNumberType === "whole" ? waterNumber : ""}}H<sub>2</sub>O
                </span>
            </span>
        </div>
        <div v-if="activateEditors">
            <structure-input
                ref="structureInput"
                v-on:ketcher-loaded="ketcherLoadListener">
            </structure-input>
            <two-buttons
                v-on:complete-editing="localCompleteEditing"
                v-on:discard-changes="discardChanges"
                v-on:clear-editor="clearEditor"
                v-bind:parent-name="$options.name"
            ></two-buttons>
        </div>
    </div>
    <div>
        <button
            v-if="status === 'choose'"
            v-on:click="editStructure"
        >Edit structure
        </button>
        <button
            v-if="status === 'choose'"
            v-on:click="sectionChosen('waternumber')"
        >Edit water number
        </button>
    </div>
</template>

<script>
import TwoButtons from "./TwoButtons.vue"
import StructureInput from "./StructureInput.vue"
import {emptyMol} from "../utils/constants.js"
import activateEditors from "../mixins/activateEditors.js"
import discardChanges from "../mixins/discardChanges.js"
import clearEditor from "../mixins/clearEditor.js"
import getParentData from "../mixins/getParentData.js";

export default {
    name: "StructureEditor",
    components: {StructureInput, TwoButtons},
    mixins: [
        activateEditors,
        discardChanges,
        clearEditor,
        getParentData
    ],
    inject: [
        "sectionChosen",
        "completeEditing",
        "setChoose",
        "URLsSettings",
        "status",
        "initialData",
        "editedData",
    ],
    data() {
        return {
            waterNumber: "",
            numerator: "",
            denominator: "",
            imageEdited: false,
            svgCode: "",
            listenToKetcherLoad: false
        }
    },
    computed: {
        showWaterNumber() {
            return (
                this.waterNumberType !== 'dry' &&
                Number(this.structureAq) !== 0 &&
                Boolean(this.structurePic)
            )
        },
        structureName() {
            let delta = this.parentData(
                ["name_data", "delta"], ""
            )
            if (delta === "") {
                return ""
            }
            if (delta.ops && delta.ops[0] && delta.ops[0].insert) {
                return delta.ops[0].insert.slice(0, -1)
            } else {
                return ""
            }
        },
        structurePic() {
            if ('structure_pic' in this.editedData &&
                this.editedData.structure_pic !== null
            ) {
                return (this.URLsSettings.structurePicBaseURL +
                    this.editedData.structure_pic)
            } else if ('structure_pic' in this.initialData &&
                this.initialData.structure_pic !== null
            ) {
                return (this.URLsSettings.structurePicBaseURL +
                    this.initialData.structure_pic)
            } else {
                return ""
            }
        },
        structureAq() {
            return this.parentData(
                ["structure_aq"], null
            )
        },
        structureMol() {
            return this.parentData(
                ["structure_mol"], emptyMol
            )
        },
        waterNumberType() {
            if (this.structureAq === null) {
                return "dry"
            } else if (
                Number.isInteger(Number(this.structureAq)) &&
                Number(this.structureAq) !== 1
            ) {
                this.waterNumber = String(this.structureAq)
                return "whole"
            } else if (
                Number.isInteger(Number(this.structureAq)) &&
                Number(this.structureAq) === 1
            ) {
                this.waterNumber = ""
                return "whole"
            } else if (Array.isArray(this.structureAq) && this.structureAq.length === 2) {
                this.numerator = String(this.structureAq[0])
                this.denominator = String(this.structureAq[1])
                return "fractional"
            } else {
                throw Error("Wrong structure_aq format!")
            }
        },
    },
    mounted() {
        window.addEventListener("message", this.acceptMessage)
    },
    methods: {
        discardChanges() {
            this.discardChangesCommon("structure_mol")
            this.discardChangesCommon("structure_pic")
        },
        editStructure() {
            this.sectionChosen('structureeditor')
            this.listenToKetcherLoad = true
        },
        ketcherLoadListener() {
            if (this.listenToKetcherLoad) {
                this.$refs.structureInput.setMolecule(this.structureMol)
                this.listenToKetcherLoad = false
            }
        },
        localCompleteEditing() {
            this.$refs.structureInput.getMolecule()
        },
        async acceptMessage(event) {
            if (typeof event.data === "string" &&
                event.data.indexOf("molBlock") !== -1
            ) {
                let molObject = JSON.parse(event.data)
                //let newImageLink = result.link_to_file
                // теперь он должен отправить на сервер mol и получить имя новой картинки
                // м изменить старое имя картинки на новое имя картинки
                this.completeEditing("structure_mol", molObject.molBlock)
                this.completeEditing(
                    "structure_pic",
                    molObject.pictureName
                )
            }
        },
    },
}
</script>

<style scoped>

div.structure-body {
    display: inline-grid;
    grid-template-columns: auto auto;
    grid-template-rows: auto;
    align-items: center;
}

span.water-number {
    display: inline-grid;
    grid-template-columns: auto auto auto;
    grid-template-rows: auto;
    align-items: center;
    font-size: 25px;
}

span.fraction {
    display: grid;
    grid-template-rows: auto auto auto;
    grid-template-columns: auto;
    padding-left: 5px;
    padding-right: 5px;
}

span.fraction-line {
    border: solid black 1px;
    width: 100%;
    height: 0;
    display: inline-block;
}
span.dot {
    padding-right: 5px;
    padding-left: 5px;
    padding-bottom: 4px;
    font-weight: bold;
}
</style>