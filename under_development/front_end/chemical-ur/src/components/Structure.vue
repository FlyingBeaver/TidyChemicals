<template>
    <div>
        <p class="section-header">
            Structure:
        </p>
        <div class="structure-body"
             v-if="status !== 'structure'"
        >
            <img
                v-bind:src="structurePic"
                v-bind:alt="structureName"
            >
            <span class="water-number" v-if="waterNumberType !== 'dry' && Number(waterNumber) !== 0">
                <span class="dot">⋅</span>
                <span class="fraction" v-if="waterNumberType === 'fractional'">
                    <span>{{numerator}}</span>
                    <div class="fraction-line"></div>
                    <span>{{denominator}}</span>
                </span>
                <span class="h2o">
                    {{waterNumberType === "whole" ? waterNumber : ""}}H<sub>2</sub>O
                </span>
            </span>
        </div>
        <div v-if="status === 'structure'">
            <structure-input
                ref="structureInput"
                v-on:ketcher-loaded="ketcherLoadListener">
            </structure-input>
            <div>
                <button v-on:click="localCompleteEditing">Complete editing</button>
                <button v-on:click="setChoose">Discard changes</button>
            </div>
        </div>
    </div>
    <div>
        <button
            v-if="status === 'choose'"
            v-on:click="editStructure"
        >Edit structure</button>
        <button
            v-if="status === 'choose'"
            v-on:click="sectionChosen('waternumber')"
        >Edit water number</button>
    </div>
</template>

<script>
import waterNumber from "./WaterNumber.vue";
import StructureInput from "./StructureInput.vue";
export default {
    name: "Structure",
    components: {StructureInput},
    props: ["status", "initialData", "editedData"],
    inject: [
        "sectionChosen",
        "completeEditing",
        "setChoose",
        "URLsSettings",
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
    mounted() {
        window.addEventListener("message", this.acceptMessage)
    },
    methods: {
        editStructure() {
            this.sectionChosen('structure')
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
            //this.status = "view"
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
        }
    },
    computed: {
        structureName() {
            let delta
            if ('name_data' in this.editedData) {
                delta = this.editedData.name_data.delta
            } else if ('name_data' in this.initialData) {
                delta = this.initialData.name_data.delta
            } else {
                return ""
            }
            if (delta.ops && delta.ops[0] && delta.ops[0].insert) {
                return delta.ops[0].insert.slice(0, -1)
            } else {
                return ""
            }
        },
        structurePic() {
            if ('structure_pic' in this.editedData) {
                return (this.URLsSettings.structurePicBaseURL +
                    this.editedData.structure_pic)
            } else if ('structure_pic' in this.initialData) {
                return (this.URLsSettings.structurePicBaseURL +
                    this.initialData.structure_pic)
            } else {
                return ""
            }
        },
        structureAq() {
            if ("structure_aq" in this.editedData) {
                return  this.editedData.structure_aq
            } else if ("structure_aq" in this.initialData) {
                return this.initialData.structure_aq
            } else {
                return null
            }
        },
        structureMol() {
            if ("structure_mol" in this.editedData) {
                return this.editedData.structure_mol
            } else if ("structure_mol" in this.initialData) {
                return this.initialData.structure_mol
            } else {
                return null
            }
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
        }
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

div.fraction-line {
    border: solid black 1px;
    width: 100%;
    height: 0;
}
span.dot {
    padding-right: 5px;
    padding-left: 5px;
    padding-bottom: 4px;
    font-weight: bold;
}
</style>