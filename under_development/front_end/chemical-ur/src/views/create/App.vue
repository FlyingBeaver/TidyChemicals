<template>
    <div class="grid-container">
        <name-editor></name-editor>
        <structure-editor></structure-editor>
        <water-number></water-number>
        <quantity-editor></quantity-editor>
        <location-editor></location-editor>
        <hazard-pictograms></hazard-pictograms>
        <cas-rn></cas-rn>
        <synonyms-editor ref="synonyms"></synonyms-editor>
        <comment-editor></comment-editor>
        <tags-editor ref="tags"></tags-editor>
    </div>

    <div class="buttons-container">
        <button v-on:click="dontSaveChanges">
            Don't save
        </button>
        <button v-on:click="saveChanges">
            Save
        </button>
    </div>
</template>

<script>
import {computed} from "vue"
import NameEditor from "../../components/NameEditor.vue"
import HazardPictograms from "../../components/HazardPictograms.vue"
import WaterNumber from "../../components/WaterNumber.vue"
import StructureEditor from "../../components/StructureEditor.vue"
import TagsEditor from "../../components/TagsEditor.vue"
import LocationEditor from "../../components/LocationEditor.vue"
import QuantityEditor from "../../components/QuantityEditor.vue"
import CasRn from "../../components/CasRn.vue"
import SynonymsEditor from "../../components/SynonymsEditor.vue"
import CommentEditor from "../../components/CommentEditor.vue"
import UsersDates from "../../components/UsersDates.vue"
import {dataKeys} from "../../utils/constants.js"

export default {
    name: "App",
    components: {
        TagsEditor,
        StructureEditor,
        WaterNumber,
        HazardPictograms,
        NameEditor,
        LocationEditor,
        QuantityEditor,
        CasRn,
        SynonymsEditor,
        CommentEditor,
        UsersDates
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
            setView: this.notImplemented,
            URLsSettings: this.URLsSettings,
        }
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
    methods: {
        dontSaveChanges() {
            this.editedData = {}
        },
        async saveChanges() {
            let formData = new FormData()
            for (let key in this.editedData) {
                formData.append(key, this.editedData[key])
            }
            await fetch(
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
        //this.initialData doesn't contain storageId field,
        // so setting it with completeEditing() is impossible
        updateStorageId(value) {
            this.editedData.storageId = value
        },
        notImplemented() {
            throw Error("Not implemented!")
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