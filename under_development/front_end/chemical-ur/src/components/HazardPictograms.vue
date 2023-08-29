<template>
    <div>
        <p class="section-header">
            Hazard pictograms:
        </p>
        <p
            v-if="status !== 'hazardpictograms'"
        >
            <img v-for="picture in picUrls" v-bind:src="picture" width="100" height="100">
            <div v-if="picUrls.length === 0">No hazard pictograms</div>
        </p>
        <p v-else>
            <table>
                <tr>
                    <td>Chosen:</td>
                    <td>Available:</td>
                </tr>
                <tr>
                    <td></td>
                    <td></td>
                </tr>
            </table>
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

export default {
    data() {
        return {
            corrosiveUrlHere: corrosiveUrl,
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
            }
        }
    },
    name: "HazardPictograms",
    props: ["initialData", "editedData", "status"],
    inject: ["sectionChosen"],
    methods: {
        completeEditing() {}
    },
    computed: {
        picUrls() {
            let actual_list = []
            if ("hazard_pictograms" in this.editedData) {
                actual_list = this.editedData["hazard_pictograms"]
            } else if ("hazard_pictograms" in this.initialData) {
                actual_list = this.initialData["hazard_pictograms"]
            } else {
                return []
            }
            let result = []
            for (let hazard of actual_list) {
                console.log(hazard)
                result.push(this.picturesUrls[hazard])
            }
            console.log(result)
            return result
        }
    },
    mounted() {
        console.log(this.initialData)
    }
}
</script>

<style scoped>

</style>