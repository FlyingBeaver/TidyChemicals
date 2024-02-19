<template>
    <div class="grid-container">
        <name-editor></name-editor>
        <structure-editor></structure-editor>
        <water-number v-if="status === 'waternumber'"></water-number>
        <quantity-editor></quantity-editor>
        <location-editor></location-editor>
        <hazard-pictograms></hazard-pictograms>
        <cas-rn></cas-rn>
        <synonyms-editor ref="synonyms"></synonyms-editor>
        <comment-editor></comment-editor>
        <users-dates></users-dates>
        <tags-editor ref="tags"></tags-editor>
    </div>
    <div
        v-if="status === 'view'"
        class="buttons-container"
    >
        <button v-on:click="addTag">
            Add or remove tag
        </button>
        <button>
            Remove from favorites
        </button>
        <button v-on:click="setChoose">
            Edit
        </button>
    </div>
    <div
        v-if="status === 'choose' && !changed"
        class="buttons-container"
    >
        <button v-on:click="setView">
            Exit from editing mode
        </button>
    </div>
    <div
        v-if="status === 'choose' && changed"
        class="buttons-container"
    >
        <button v-on:click="dontSaveChanges">
            Don't save changes
        </button>
        <button v-on:click="saveChanges">
            Save changes
        </button>
    </div>
    <div v-if="status !== 'choose' && status !== 'view'">
        <button v-on:click="dontSaveChanges">
            Exit without saving
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
            setView: this.setView,
            URLsSettings: this.URLsSettings,
        }
    },
    data() {
        return {
            // status can be: "view", "choose", "create"
            // ("create" not used here)
            // or equal to component name in lowercase
            status: "view",
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
    async created() {
        if (this.getContentFromServer) {
            let response = await fetch(
                this.URLsSettings.dataURL
            )
            this.initialData = await response.json()
        } else {
            let containerElement = document.getElementById("content")
            this.initialData = JSON.parse(containerElement.innerText)
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
            this.sectionChosen('tagseditor')
        },
        async saveChanges() {
            let formData = new FormData()
            for (let key in this.editedData) {
                if (JSON.stringify(this.editedData) !==
                    JSON.stringify(this.initialData)) {
                    formData.append(key, this.editedData[key])
                }
            }
            let response = await fetch(
                this.URLsSettings.postURL,
                {
                method: "POST",
                body: formData,
                }
            )
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
        //this.initialData don't contain storageId field,
        // so setting it with completeEditing() is impossible
        updateStorageId(value) {
            this.editedData.storageId = value
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

.blank-data {
    font-style: italic;
}
</style>