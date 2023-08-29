<template>
    <div class="grid-container">
        <name v-bind:initialData="initialData"
              v-bind:editedData="editedData"
              v-bind:status="status"
        >
        </name>
        <!--    <structure content="./assets/TBDMSCl.png" v-bind:status="status"></structure>-->
        <hazard-pictograms
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
        >
        </hazard-pictograms>
    </div>
    <div v-if="status === 'view'">
        <button>Add tag</button>
        <button>Remove from favorites</button>
        <button v-on:click="setChoose">Edit</button>
    </div>
    <div v-if="status === 'choose' && !changed">
        <button v-on:click="setView">Exit from editing mode</button>
    </div>
    <div v-if="status === 'choose' && changed">
        <button v-on:click="dontSaveChanges">Don't save changes</button>
        <button v-on:click="saveChanges">Save changes</button>
    </div>
    <div v-else>
        <button v-on:click="dontSaveChanges">Don't save changes</button>
    </div>
</template>

<script>
import Name from "./components/Name.vue";
import HazardPictograms from "./components/HazardPictograms.vue";
export default {
    name: "App",
    components: {HazardPictograms, Name},
    data() {
        return {
            status: "view",
            initialData: {},
            editedData: {},
            getContentFromServer: true,
        }
    },
    methods: {
        sectionChosen(newStatus) {
            console.log(newStatus)
            this.status = newStatus
        },
        setChoose() {
            this.status = "choose"
        },
        setView() {
            this.status = "view"
        },
        dontSaveChanges() {
            this.status = "view"
            this.editedData = {}
        },
        async saveChanges() {
            let formData = new FormData()
            for (let key in this.editedData) {
                if (JSON.stringify(this.editedData) !==
                    JSON.stringify(this.initialData)) {
                    formData.append(key, this.editedData[key])
                }
            }
            let address = ""
            if (this.getContentFromServer) {
                address = "http://127.0.0.1:5000/chemical/"
            } else {
                address = window.location.href
            }
            let response = await fetch(address, {
                method: "POST",
                body: formData,
            })
            let result = await response.json()
            if (result.error) {
                alert("Error happened!")
            } else {
                delete result["error"]
                this.initialData = result
                this.editedData = {}
                this.status = "view"
            }
        },
        completeEditing(whatEdited, newValue) {
            console.log("complete editing")
            if (whatEdited in this.initialData) {
                this.editedData[whatEdited] = newValue
            }
            this.status = "choose"
        }
    },
    computed: {
        changed() {
            return !(JSON.stringify(this.editedData) === "{}")
        }
    },
    provide() {
        return {
            sectionChosen: this.sectionChosen,
            completeEditing: this.completeEditing,
            initialData: this.initialData,
            editedData: this.editedData,
            status: this.status,
        }
    },
    async mounted() {
        if (this.getContentFromServer) {
            let response = await fetch(
                "http://127.0.0.1:5000/chemical/"
            )
            this.initialData = await response.json()
        } else {
            let containerElement = document.getElementById("content")
            this.initialData = JSON.parse(containerElement.innerText)
        }
    }
}
</script>

<style>
div.grid-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
}
</style>