<template>
    <div class="grid-container">
        <name></name>
        <structure></structure>
        <water-number></water-number>
        <quantity></quantity>
        <location></location>
        <hazard-pictograms></hazard-pictograms>
        <cas-rn></cas-rn>
        <synonyms ref="synonyms"></synonyms>
        <comment></comment>
        <tags ref="tags"></tags>
    </div>

    <div class="buttons-container">
        <button v-on:click="dontSaveChanges">Don't save</button>
        <button v-on:click="saveChanges">Save</button>
    </div>
<!--    <div v-if="status !== 'view'">-->
<!--        <button v-on:click="dontSaveChanges">Don't save changes</button>-->
<!--    </div>-->
</template>

<script>
import {computed} from "vue"
import Name from "./components/Name.vue"
import HazardPictograms from "./components/HazardPictograms.vue"
import WaterNumber from "./components/WaterNumber.vue"
import Structure from "./components/Structure.vue"
import Tags from "./components/Tags.vue"
import Location from "./components/Location.vue"
import Quantity from "./components/Quantity.vue"
import CasRn from "./components/CasRn.vue"
import Synonyms from "./components/Synonyms.vue"
import Comment from "./components/Comment.vue"
import UsersDates from "./components/UsersDates.vue"
import {dataKeys} from "./components/constants.js"
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
        UsersDates
    },
    data() {
        return {
            // status can be: "view", "choose", "create"
            // or equal to component name in lowercase,
            // but here only "create" used
            status: "create",
            initialData: {},
            editedData: {},
            getContentFromServer: true,
            availableTags: {}
        }
    },
    methods: {
        dontSaveChanges() {
            this.editedData = {}
        },
        async saveChanges() {
            let formData = new FormData()
            for (let key in this.editedData) {
                formData.append(key, this.editedData[key])
            }
            let response = await fetch(
                this.URLsSettings.postURL,
                {
                method: "POST",
                body: formData,
                }
            )
        },
        completeEditing(whatEdited, newValue) {
            if (whatEdited in dataKeys) {
                this.editedData[whatEdited] = newValue
            }
        },
        //this.initialData don't contain storageId field,
        // so setting it with completeEditing() is impossible
        updateStorageId(value) {
            this.editedData.storageId = value
        }
    },
    computed: {
        changed() {
            return !(JSON.stringify(this.editedData) === "{}")
        },
        URLsSettings() {
            let basicUrl = "http://127.0.0.1:5000"
            return {
                dataURL: basicUrl + "/chemical/",
                postURL: basicUrl + "/chemical/",
                tagsURL: basicUrl + "/tags/",
                unitsURL: basicUrl + "/units/",
                rootStorageURL: basicUrl + "/root/",
                pathToChemicalURL: basicUrl + "/path_to_chemical/",
                childrenStoragesURL: basicUrl + "/children/",
                favoritesURL: "/favorites/",
                hashtagsURL: "/hashtags/",
                ampersandtagsURL: "/ampersandtags/",
                usersURL: "/users/",
                structurePicBaseURL: basicUrl,
                ketcherIframeURL: basicUrl,
            }
        },
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
            initialData: computed(() => this.initialData),
            editedData: computed(() => this.editedData),
            status: computed(() => this.status),
            updateStorageId: this.updateStorageId,
            setChoose: this.setChoose,
            URLsSettings: this.URLsSettings,
        }
    },
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