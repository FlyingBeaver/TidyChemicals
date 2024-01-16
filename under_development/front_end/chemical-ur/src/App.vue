<template>
    <div class="grid-container">
        <name v-bind:initialData="initialData"
              v-bind:editedData="editedData"
              v-bind:status="status"
        >
        </name>
        <structure
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
        ></structure>
        <water-number
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
            v-if="status === 'waternumber'"
        >
        </water-number>
        <quantity
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
        ></quantity>
        <location
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
        ></location>
        <hazard-pictograms
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
        >
        </hazard-pictograms>
        <cas-rn
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
        ></cas-rn>
        <synonyms
            ref="synonyms"
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
        ></synonyms>
        <comment
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
        ></comment>
        <tags
            v-bind:initialData="initialData"
            v-bind:editedData="editedData"
            v-bind:status="status"
            v-bind:tags-address="tagsAddress"
            ref="tags"
        ></tags>
    </div>
    <div v-if="status === 'view'" class="buttons-container">
        <button v-on:click="addTag">Add or remove tag</button>
        <button>Remove from favorites</button>
        <button v-on:click="setChoose">Edit</button>
    </div>
    <div v-if="status === 'choose' && !changed" class="buttons-container">
        <button v-on:click="setView">Exit from editing mode</button>
    </div>
    <div v-if="status === 'choose' && changed" class="buttons-container">
        <button v-on:click="dontSaveChanges">Don't save changes</button>
        <button v-on:click="saveChanges">Save changes</button>
    </div>
    <div v-if="status !== 'choose' && status !== 'view'">
        <button v-on:click="dontSaveChanges">Exit without saving</button>
    </div>
<!--    <div v-if="status !== 'view'">-->
<!--        <button v-on:click="dontSaveChanges">Don't save changes</button>-->
<!--    </div>-->
</template>

<script>
import Name from "./components/Name.vue";
import HazardPictograms from "./components/HazardPictograms.vue";
import WaterNumber from "./components/WaterNumber.vue";
import Structure from "./components/Structure.vue";
import Tags from "./components/Tags.vue";
import Location from "./components/Location.vue";
import Quantity from "./components/Quantity.vue";
import CasRn from "./components/CasRn.vue";
import Synonyms from "./components/Synonyms.vue";
import Comment from "./components/Comment.vue";
export default {
    name: "App",
    components: {
        Tags,
        Structure,
        WaterNumber,
        HazardPictograms,
        Name,
        Location,
        Quantity,
        CasRn,
        Synonyms,
        Comment,
    },
    data() {
        return {
            status: "view",
            initialData: {},
            editedData: {},
            getContentFromServer: true,
            tagsAddress: "http://127.0.0.1:5000/tags/",
            availableTags: {}
        }
    },
    methods: {
        sectionChosen(newStatus) {
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
        async addTag() {
            this.sectionChosen('tags')
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
            console.log(address)
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
            if (whatEdited in this.initialData) {
                this.editedData[whatEdited] = newValue
            }
            if (whatEdited === "tags") {
                this.status = "view"
            } else {
                this.status = "choose"
            }
        },
        updateStorageId(value) {
            this.editedData.storageId = value
        }
    },
    computed: {
        changed() {
            return !(JSON.stringify(this.editedData) === "{}")
        }
    },
    watch: {
        status(newStatus, oldStatus) {
            if (oldStatus === "synonyms" && newStatus !== "synonyms") {
                this.$refs.synonyms.exitWithoutSaving()
            }
        }
    },
    provide() {
        return {
            sectionChosen: this.sectionChosen,
            completeEditing: this.completeEditing,
            initialData: this.initialData,
            editedData: this.editedData,
            status: this.status,
            updateStorageId: this.updateStorageId,
            setChoose: this.setChoose,
        }
    },
    async created() {
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
    padding: 10px
}

div.buttons-container {
    padding: 10px
}

p {
    margin: 0;
}

p.section-header {
    margin-top: 16px;
    margin-bottom: 8px;
}
</style>