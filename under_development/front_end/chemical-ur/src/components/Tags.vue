<template>
    <div>
        <p class="section-header">
            Tags
        </p>
        <div v-if="status === 'tags'">
            <div v-for="(tag, index) in editableTagsList"
                 class="tag"
                 v-bind:data-key="index">
                {{ tag }}
                <span v-on:click="deleteTag"
                      class="delete-x"
                >X</span>
            </div>
        </div>
        <div v-if="status === 'tags'"
             class="tags-grid"
        >
            <input class="tag-input"
                   v-on:input="hideWarnings"
                   v-on:keyup.down.prevent="moveHintHighlighting"
                   v-on:keyup.up.prevent="moveHintHighlighting"
                   v-on:keyup.enter="inputEnterKey"
                   v-on:keyup.esc="inputEscKey"
                   v-on:focus="inputFocus"
                   v-model="inputValue"
            >
            <div v-if="hints.length > 0"
                 class="tags-hints-box"
            >
                <div v-for="(tag, index) in hints"
                     class="tag-hint"
                     v-bind:class="{'highlighted-hint': index === highlightedTagIndex}"
                     v-on:click="chooseHintTag"
                >{{ tag }}</div>
            </div>
            <button class="tag-button"
                    v-on:click="toggleHashDropdown"
            >+#</button>
            <button class="tag-button"
                    v-on:click="toggleAmpersandDropdown"
            >+&</button>
            <button class="tag-button"
                    v-on:click="toggleFavorites"
            >★</button>
            <div class="tags-dropdown" v-show="hashDropdownShown">
                <div v-for="tag in availableHashtags"
                     v-on:click="chooseHintTag"
                     class="tag-dropdown"
                >#{{ tag }}</div>
            </div>
            <div v-show="ampersandDropdownShown"></div>
            <div class="tags-dropdown" v-show="ampersandDropdownShown">
                <div v-for="tag in availableAmpersandtags"
                     v-on:click="chooseHintTag"
                     class="tag-dropdown"
                >&{{ tag }}</div>
            </div>
            <p class="warning" v-show="leadingCharWarning">
                Tag name must start with "#" or with "&"
            </p>
            <p class="warning" v-show="tagIsOldWarning">
                You are trying to add the tag that already have been added
            </p>
            <p class="warning" v-show="oddCharsWarning">
                You are trying to enter a character that is not allowed in tag.
                Only lower- and uppercase latin letters, digits and "_" are allowed.
            </p>
            <p class="warning" v-show="tooManySpecialCharsWarning">
                Only one "#" or "&" character is allowed in tag name
            </p>
            <p class="warning" v-show="specialCharNotInStartWarning">
                "#" or "&" must be first character of the tag
            </p>
        </div>
        <p v-else
           v-for="(value, key) in currentTags">
            <a v-bind:href="value">{{ key }}</a>
        </p>
        <div v-if="status === 'tags'"
             class="bottom"
        >
            <button
                v-on:click="localCompleteEditing"
            >Complete Editing</button>
            <button
                v-on:click="setChoose"
            >Discard changes</button>

        </div>
    </div>
    <div>
    </div>
</template>

<script>
import {difference, charactersForTags} from "./constants.js";
export default {
    name: "Tags",
    props: [
        "status",
        "initialData",
        "editedData",
        "tagsAddress",
    ],
    inject: ["sectionChosen", "completeEditing", "setChoose"],
    data() {
        return {
            startOfTagsUrl: "",
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
            availableTags: []
        }
    },
    methods: {
        toggleHashDropdown() {
            this.hashDropdownShown = !this.hashDropdownShown
            this.ampersandDropdownShown = false
        },
        toggleAmpersandDropdown() {
            this.ampersandDropdownShown = !this.ampersandDropdownShown
            this.hashDropdownShown = false
        },
        fillTagsList() {
            if ("tags" in this.editedData) {
                this.editableTagsList = [...this.editedData.tags]
            } else if ("tags" in this.initialData) {
                this.editableTagsList = [...this.initialData.tags]
            }
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
                this.inputValue = ""
            } else if (Number.isInteger(this.highlightedTagIndex)) {
                this.editableTagsList.push(this.hints[this.highlightedTagIndex])
                this.chosenHints.push(this.hints[this.highlightedTagIndex])
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
            } else {
                this.editableTagsList.splice(favouritesIndex, 1)
            }
        },
        localCompleteEditing() {
            this.completeEditing("tags", this.editableTagsList)
        }
    },
    computed: {
        currentTags() {
            let tagsList = []
            if ("tags" in this.editedData) {
                tagsList = this.editedData.tags
            } else if ("tags" in this.initialData) {
                tagsList = this.initialData.tags
            } else {
                return {}
            }
            let result = {}
            for (let tag of tagsList) {
                if (tag === "Favorites") {
                    result[tag] = this.startOfTagsUrl + "/favorites/"
                } else if (tag.startsWith("#")) {
                    result[tag] = (this.startOfTagsUrl +
                        "/hashtags/" + tag.slice(1) + "/")
                } else if (tag.startsWith("&")) {
                    result[tag] = (this.startOfTagsUrl +
                        "/ampersandtags/" + tag.slice(1) + "/")
                } else {
                    throw Error("Unknown format of the tag")
                }
            }
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
        }
    },
    watch: {
        async status(newStatus) {
            if (newStatus === "tags") {
                let tagsResponse = await fetch(this.tagsAddress)
                this.availableTags = await tagsResponse.json()
                this.fillTagsList()
            }
        },
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