<template>
    <div>
        <p class="section-header">
            Hazard pictograms:
        </p>
        <p v-if="!activateEditors">
            <img v-for="(value, key) in picUrls"
                 v-bind:src="value"
                 v-bind:alt="key"
                 width="100"
                 height="100">
            <div
                v-if="Object.keys(picUrls).length === 0"
                class="blank-data"
            >No hazard pictograms</div>
        </p>
        <p v-else>
            <table>
                <tr class="table-header">
                    <td>Chosen:</td>
                    <td>Available:</td>
                </tr>
                <tr>
                    <td>
                        <img
                            v-for="(value, key) in chosenPictograms"
                            v-bind:key="key"
                            v-on:click="highlightPictogram"
                            v-on:dblclick="unChoose"
                            v-bind:src="value"
                            v-bind:alt="key"
                            v-bind:class="{frame: key === this.highlighted}"
                            width="100"
                            height="100">
                    </td>
                    <td>
                        <img
                            v-for="(value, key) in unChosenPictograms"
                            v-bind:key="key"
                            v-on:click="highlightPictogram"
                            v-on:dblclick="choose"
                            v-bind:src="value"
                            v-bind:alt="key"
                            v-bind:class="{frame: key === this.highlighted}"
                            width="100"
                            height="100"
                        >
                    </td>
                </tr>
                <tr>
                    <td colspan="2">{{ descriptionOfHighlighted }}</td>
                </tr>
            </table>
        <two-buttons
            v-on:complete-editing="localCompleteEditing"
            v-on:discard-changes="discardChanges"
            v-on:clear-editor="clearEditor"
            v-bind:parent-name="$options.name"
        ></two-buttons>
        </p>
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
import compressedGasUrl from "../assets/hazard_pictograms/compressed_gas.svg"
import corrosiveUrl from "../assets/hazard_pictograms/corrosive.svg"
import environmentalHazardUrl from "../assets/hazard_pictograms/environmental_hazard.svg"
import explosiveUrl from "../assets/hazard_pictograms/explosive.svg"
import flammableUrl from "../assets/hazard_pictograms/flammable.svg"
import harmfulUrl from "../assets/hazard_pictograms/harmful.svg"
import healthHazardUrl from "../assets/hazard_pictograms/health_hazard.svg"
import ionizingRadiationUrl from "../assets/hazard_pictograms/ionizing_radiation.svg"
import oxidizingUrl from "../assets/hazard_pictograms/oxidizing.svg"
import toxicUrl from "../assets/hazard_pictograms/toxic.svg"
import TwoButtons from "./TwoButtons.vue"
import activateEditors from "../mixins/activateEditors.js"
import discardChanges from "../mixins/discardChanges.js"
import getParentData from "../mixins/getParentData.js"

export default {
    name: "HazardPictograms",
    components: {TwoButtons},
    mixins: [
        activateEditors,
        discardChanges,
        getParentData,
    ],
    inject: [
        "sectionChosen",
        "completeEditing",
        "setChoose",
        "initialData",
        "editedData",
        "status",
    ],
    data() {
        return {
            picturesUrls: {
                compressed_gas: compressedGasUrl,
                corrosive: corrosiveUrl,
                environmental_hazard: environmentalHazardUrl,
                explosive: explosiveUrl,
                flammable: flammableUrl,
                harmful: harmfulUrl,
                health_hazard: healthHazardUrl,
                ionizing_radiation: ionizingRadiationUrl,
                oxidizing: oxidizingUrl,
                toxic: toxicUrl
            },
            chosenPictograms: {},
            unChosenPictograms: {},
            highlighted: "",
        }
    },
    computed: {
        picUrls() {
            let actual_list = []
            actual_list.push(
                ...this.parentData(["hazard_pictograms"], [])
            )
            let result = {}
            for (let hazard of actual_list) {
                result[hazard] = this.picturesUrls[hazard]
            }
            return result
        },
        descriptionOfHighlighted() {
            if (this.highlighted === "") {
                return "Double-click on pictogram to choose it"
            } else {
                let withSpaces = this.highlighted.replace("_", " ")
                return withSpaces[0].toUpperCase() + withSpaces.slice(1)
            }
        },
    },
    created() {
        if (this.status === "create") {
            this.unChosenPictograms = Object.assign({}, this.picturesUrls)
            this.chosenPictograms = {}
        }
    },
    methods: {
        clearEditor() {
            this.unChosenPictograms = Object.assign(
                this.unChosenPictograms,
                this.chosenPictograms
            )
            this.chosenPictograms = {}
        },
        localCompleteEditing() {
            this.completeEditing(
                'hazard_pictograms',
                Object.keys(this.chosenPictograms)
            )
        },
        discardChanges() {
            this.discardChangesCommon("hazard_pictograms")
            this.setup()
        },
        setup() {
            this.chosenPictograms = Object.assign({}, this.picUrls)
            let unChosen = {}
            for (let hazard in this.picturesUrls) {
                if (!(hazard in this.chosenPictograms)) {
                    unChosen[hazard] = this.picturesUrls[hazard]
                }
            }
            this.unChosenPictograms = unChosen
        },
        localSectionChosen() {
            this.sectionChosen(this.$options.name.toLowerCase())
            this.setup()
        },
        highlightPictogram(event) {
            this.highlighted = event.target.alt
        },
        choose(event) {
            let chosen = event.target.alt
            this.chosenPictograms[chosen] = this.picturesUrls[chosen]
            if (chosen in this.unChosenPictograms) {
                delete this.unChosenPictograms[chosen]
            }
        },
        unChoose(event) {
            let unChosen = event.target.alt
            this.unChosenPictograms[unChosen] = this.picturesUrls[unChosen]
            if (unChosen in this.chosenPictograms) {
                delete this.chosenPictograms[unChosen]
            }
        },
    },
}
</script>

<style>
table {
    border: solid black 1px;
    border-collapse: collapse;
    margin-bottom: 20px;
}

td {
    border: solid black 1px;
}

tr.table-header {
    text-align: center;
    background-color: lightgray;
    font-weight: bold;
}

img.frame {
    border: 3px solid black;
}
</style>