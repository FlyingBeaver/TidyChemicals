<template>
    <div>
        <p class="section-header">
            Tags
        </p>
        <div v-if="activateEditors">
            <div
                v-for="(tag, index) in editableTagsList"
                v-bind:data-key="index"
                class="tag"
            >
                {{ tag }}
                <span
                    v-on:click="deleteTag"
                    class="delete-x"
                >X
                </span>
            </div>
        </div>
        <div
            v-if="activateEditors"
            class="tags-grid"
        >
            <input
                v-model="inputValue"
                v-on:input="hideWarnings"
                v-on:keyup.down.prevent="moveHintHighlighting"
                v-on:keyup.up.prevent="moveHintHighlighting"
                v-on:keyup.enter="inputEnterKey"
                v-on:keyup.esc="inputEscKey"
                v-on:focus="inputFocus"
                class="tag-input"
            />
            <div
                v-if="hints.length > 0"
                class="tags-hints-box"
            >
                <div v-for="(tag, index) in hints"
                     v-on:click="chooseHintTag"
                     v-bind:class="{'highlighted-hint': index === highlightedTagIndex}"
                     class="tag-hint"
                >{{ tag }}</div>
            </div>
            <button class="tag-button"
                    v-on:click="toggleHashDropdown"
            >+#
            </button>
            <button class="tag-button"
                    v-on:click="toggleAmpersandDropdown"
            >+&
            </button>
            <button class="tag-button"
                    v-on:click="toggleFavorites"
            >★
            </button>
            <div class="tags-dropdown" v-show="hashDropdownShown">
                <div v-for="tag in availableHashtags"
                     v-on:click="chooseHintTag"
                     class="tag-dropdown"
                >#{{ tag }}
                </div>
            </div>
            <div v-show="ampersandDropdownShown"></div>
            <div class="tags-dropdown" v-show="ampersandDropdownShown">
                <div v-for="tag in availableAmpersandtags"
                     v-on:click="chooseHintTag"
                     class="tag-dropdown"
                >&{{ tag }}
                </div>
            </div>
            <p v-show="leadingCharWarning" class="warning">
                Tag name must start with "#" or with "&"
            </p>
            <p v-show="tagIsOldWarning" class="warning">
                You are trying to add the tag that already have been added
            </p>
            <p v-show="oddCharsWarning" class="warning">
                You are trying to enter a character that is not allowed in tag.
                Only lower- and uppercase latin letters, digits and "_" are allowed.
            </p>
            <p v-show="tooManySpecialCharsWarning" class="warning">
                Only one "#" or "&" character is allowed in tag name
            </p>
            <p v-show="specialCharNotInStartWarning" class="warning">
                "#" or "&" must be first character of the tag
            </p>
        </div>
        <div v-else>
            <p v-for="[key, value] in tagsForViewMode">
                <a v-bind:href="value">{{ key }}</a>
            </p>
            <p v-if="tagsForViewMode.length === 0"
               class="blank-data"
            >No tags
            </p>
        </div>
        <two-buttons
            v-on:complete-editing="localCompleteEditing"
            v-on:discard-changes="discardChanges"
            v-on:clear-editor="clearEditor"
            v-bind:parent-name="$options.name"
        ></two-buttons>
    </div>
    <div>
        <!--It is a placeholder-->
    </div>
</template>

<script>
import {difference, charactersForTags} from "../utils/constants.js"
import TwoButtons from "./TwoButtons.vue"
import activateEditors from "../mixins/activateEditors.js"
import getParentData from "../mixins/getParentData.js"

export default {
    name: "TagsEditor",
    components: {TwoButtons},
    mixins: [activateEditors, getParentData],
    inject: [
        "sectionChosen",
        "completeEditing",
        "setView",
        "URLsSettings",
        "status",
        "initialData",
        "editedData",
    ],
    data() {
        return {
            inputValue: "",
            hashDropdownShown: false,
            ampersandDropdownShown: false,
            editableTagsList: [],
            highlightedTagIndex: null,
            leadingCharWarning: false,
            tagIsOldWarning: false,
            chosenHints: [],
            availableChars: new Set(charactersForTags),
            oddCharsWarning: false,
            tooManySpecialCharsWarning: false,
            specialCharNotInStartWarning: false,
            availableTags: [],
        }
    },
    computed: {
        tags() {
            let tagsList = []
            tagsList.push(...this.parentData(["tags"], []))
            return tagsList
        },
        /**
         * Generates tags array for 'view' and 'change' mode
         * Syntax of tags array is [[tag_name, tag_url], ...]
         */
        tagsForViewMode() {
            let result = []
            let link
            for (let tag of this.tags) {
                if (tag === "Favorites") {
                    link = this.URLsSettings.favoritesURL
                    result.push([tag, link])
                } else if (tag.startsWith("#")) {
                    link = (
                        this.URLsSettings.hashtagsURL + tag.slice(1) + "/"
                    )
                    result.push([tag, link])
                } else if (tag.startsWith("&")) {
                    link = (
                        this.URLsSettings.ampersandtagsURL +
                        tag.slice(1) + "/"
                    )
                    result.push([tag, link])
                } else {
                    throw Error("Unknown format of the tag")
                }
            }
            result.sort(this.compareFunction)
            return result
        },
        hints() {
            let result = []
            if (this.inputValue !== "") {
                for (let item of this.tagsArray) {
                    if (item.indexOf(this.inputValue.toLowerCase()) !== -1 &&
                        this.chosenHints.indexOf(item) === -1) {
                        result.push(item)
                    }
                }
            }
            return result
        },
        tagsArray () {
            let result = []
            if ("hashtags" in this.availableTags) {
                for (let item of this.availableTags.hashtags) {
                    result.push("#" + item.toLowerCase())
                }
            }
            if ("ampersandtags" in this.availableTags) {
                for (let item of this.availableTags.ampersandtags) {
                    result.push("&" + item.toLowerCase())
                }
            }
            return result
        },
        availableHashtags() {
            let result = []
            if ("hashtags" in this.availableTags) {
                for (let item of this.availableTags.hashtags) {
                    if (this.chosenHints.indexOf("#" + item) === -1) {
                        result.push(item)
                    }
                }
            }
            return result
        },
        availableAmpersandtags() {
            let result = []
            if ("ampersandtags" in this.availableTags) {
                for (let item of this.availableTags.ampersandtags) {
                    if (this.chosenHints.indexOf("&" + item) === -1) {
                        result.push(item)
                    }
                }
            }
            return result
        },
    },
    watch: {
        async status(newStatus) {
            if (newStatus === "tagseditor") {
                let tagsResponse = await fetch(this.URLsSettings.tagsURL)
                this.availableTags = await tagsResponse.json()
                this.fillTagsList()
            }
        },
        /**
         * Input validator
         */
        inputValue(newValue, oldValue) {
            this.highlightedTagIndex = null
            //Check for odd chars
            if (difference(new Set(newValue), this.availableChars).size > 0) {
                this.inputValue = oldValue
                this.oddCharsWarning = true
            }
            //Check if only one "#" or "&" present
            if (newValue.split("#").length + newValue.split("&").length > 3) {
                this.inputValue = oldValue
                this.tooManySpecialCharsWarning = true
            }
            //Check if "#" or "&" is in start position
            if (newValue.indexOf("#") > 0 || newValue.indexOf("&") > 0) {
                this.inputValue = oldValue
                this.specialCharNotInStartWarning = true
            }
        },
    },
    async created() {
        if (this.status === "create") {
            let tagsResponse = await fetch(this.URLsSettings.tagsURL)
            this.availableTags = await tagsResponse.json()
        }
    },
    methods: {
        compareFunction(a, b) {
            if (a[0] === "Favorites") {
                return -1
            } else if (b[0] === "Favorites") {
                return 1
            } else if (a[0] < b[0]) {
                return -1
            } else if (a[0] > b[0]) {
                return 1
            } else {
                return 0
            }
        },
        discardChanges() {
            if ("tags" in this.editedData) {
                delete this.editedData["tags"]
            }
            this.setView()
        },
        clearEditor() {
            this.inputValue = ""
            this.editableTagsList = []
        },
        toggleHashDropdown() {
            this.hashDropdownShown = !this.hashDropdownShown
            this.ampersandDropdownShown = false
        },
        toggleAmpersandDropdown() {
            this.ampersandDropdownShown = !this.ampersandDropdownShown
            this.hashDropdownShown = false
        },
        fillTagsList() {
            this.editableTagsList = this.tags
            this.sortEditableTagsList()
        },
        deleteTag(event) {
            let index = Number(event.target.parentNode.dataset.key)
            let deletedTag = this.editableTagsList.splice(index, 1)[0]
            let indexInChosenHints = this.chosenHints.indexOf(deletedTag)
            if (indexInChosenHints !== -1) {
                this.chosenHints.splice(indexInChosenHints, 1)
            }
        },
        moveHintHighlighting (event) {
            if (event.key === "ArrowDown" && this.hints.length > 0) {
                if (this.highlightedTagIndex === null) {
                    this.highlightedTagIndex = 0
                } else if (this.highlightedTagIndex <= this.hints.length - 2) {
                    this.highlightedTagIndex += 1
                }
            }
            if (event.key === "ArrowUp" && this.hints.length > 0) {
                if (this.highlightedTagIndex === null) {
                    this.highlightedTagIndex = this.hints.length - 1
                } else if (this.highlightedTagIndex > 0) {
                    this.highlightedTagIndex -= 1
                }
            }
        },
        inputEnterKey() {
            if (this.highlightedTagIndex === null &&
                this.leadingCharCheck() &&
                this.tagIsNewCheck()) {
                this.editableTagsList.push(this.inputValue)
                this.sortEditableTagsList()
                this.inputValue = ""
            } else if (Number.isInteger(this.highlightedTagIndex)) {
                this.editableTagsList.push(
                    this.hints[this.highlightedTagIndex]
                )
                this.sortEditableTagsList()
                this.chosenHints.push(this.hints[this.highlightedTagIndex])
            }
        },
        sortEditableTagsList() {
            this.editableTagsList.sort()
            let favIndex = this.editableTagsList.indexOf("Favorites")
            if (favIndex !== -1 && this.editableTagsList.length > 1) {
                this.editableTagsList.splice(favIndex, 1)
                this.editableTagsList.splice(
                    0, 0, "Favorites"
                )
            }
        },
        leadingCharCheck() {
            if (this.inputValue[0] === "#" || this.inputValue[0] === "&") {
                return true
            } else {
                this.leadingCharWarning = true
                return false
            }
        },
        tagIsNewCheck() {
            if (this.editableTagsList.indexOf(this.inputValue) === -1) {
                return true
            } else {
                this.tagIsOldWarning = true
                return false
            }
        },
        inputEscKey() {
            this.highlightedTagIndex = null
        },
        hideWarnings() {
            this.leadingCharWarning = false
            this.tagIsOldWarning = false
            this.oddCharsWarning = false
            this.tooManySpecialCharsWarning = false
            this.specialCharNotInStartWarning = false

        },
        chooseHintTag(event) {
            let tag = event.target.textContent
            this.editableTagsList.push(tag)
            this.sortEditableTagsList()
            this.chosenHints.push(tag)
        },
        inputFocus() {
            this.hashDropdownShown = false
            this.ampersandDropdownShown = false
        },
        toggleFavorites() {
            this.hashDropdownShown = false
            this.ampersandDropdownShown = false
            let favouritesIndex = this.editableTagsList.indexOf("Favorites")
            if (favouritesIndex === -1) {
                this.editableTagsList.push("Favorites")
                this.sortEditableTagsList()
            } else {
                this.editableTagsList.splice(favouritesIndex, 1)
            }
        },
        localCompleteEditing() {
            this.completeEditing("tags", this.editableTagsList)
        }
    },
}
</script>

<style>
div.tags-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    margin-bottom: 20px;
}
input.tag-input {
    grid-column-start: 1;
    grid-column-end: 4;
}
button.tag-button {
    font-weight: bold;
}
div.tags-dropdown {
    background-color: lightgoldenrodyellow;
}
div.tag-dropdown:hover {
    background-color: lightskyblue;
    cursor: pointer;
}
span.delete-x {
    font-family: sans-serif;
    margin-left: 30px;
}
span.delete-x:hover {
    background-color: lightgoldenrodyellow;
    cursor: pointer;
}
div.tags-hints-box {
    grid-column-start: 1;
    grid-column-end: 4;
}
div.tag-hint:hover {
    background-color: lightgoldenrodyellow;
    cursor: pointer;
}
div.highlighted-hint {
    background-color: lightskyblue;
}

p.warning {
    grid-column-start: 1;
    grid-column-end: 4;
}
div.bottom {
    margin-bottom: 10px;
}
</style>