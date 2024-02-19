<template>
    <div>
        <p class="section-header">
            Location:
        </p>
        <p v-if="!activateEditors"
           v-bind:class="{'blank-data': location === 'No location data!'}"
        >
            {{location}}
        </p>
        <div v-else class="tree">
            <div ref="tree_container" class="tree_container">
                <div class="background"></div>
                <div class="foreground" data-root_id="0" data-root_name="root">
                    <ul>
                        <li class="closed"><span data-storage_node_id="0">root</span></li>
                    </ul>
                </div>
            </div>
        </div>
        <input type="hidden" name="treeOutput" ref="treeOutput">
        <two-buttons
            v-on:complete-editing="localCompleteEditing"
            v-on:discard-changes="discardChanges"
            v-on:clear-editor="unhighlightStorage"
            v-bind:parent-name="$options.name"
        ></two-buttons>
    </div>
    <div>
        <button
            v-if="status === 'choose'"
            v-on:click="showEditor"
        >
            Edit
        </button>
    </div>
</template>

<script>
import {Tree} from "./trees_editor05.js"
import TwoButtons from "./TwoButtons.vue"
import activateEditors from "../mixins/activateEditors.js"
import discardChanges from "../mixins/discardChanges.js"
import getParentData from "../mixins/getParentData.js"

export default {
    name: "LocationEditor",
    components: {TwoButtons},
    mixins: [activateEditors, discardChanges, getParentData],
    inject: [
        "sectionChosen",
        "completeEditing",
        "updateStorageId",
        "setChoose",
        "URLsSettings",
        "status",
        "initialData",
        "editedData",
    ],
    data() {
        return {
            editorIsOn: false,
            tree: null,
            selectedStorages: "",
        }
    },
    computed: {
        location() {
            return this.parentData(
                ["location"], "No location data!"
            )
        }
    },
    mounted() {
        if (this.status === "create") {
            this.showEditor()
        }
    },
    methods: {
        discardChanges() {
            this.discardChangesCommon("location")
            this.discardChangesCommon("storageId")
        },
        unhighlightStorage () {
            console.log("unhighlight storage")
            let event = new Event("unhighlight-storage")
            this.$refs.tree_container.dispatchEvent(event)
        },
        localCompleteEditing() {
            let treeOutputContent = this.$refs.treeOutput.value
            let treeOutputObj = JSON.parse(treeOutputContent)
            let fullPathNames = treeOutputObj.full_path_names
            let fullPath = fullPathNames.join("/")
            let fullPathIds = treeOutputObj.full_path_ids
            this.completeEditing("location", fullPath)
            this.updateStorageId(fullPathIds.slice(-1))
        },
        async showEditor() {
            if (this.status !== "create") {
                this.sectionChosen(this.$options.name.toLowerCase())
            }
            let response = await fetch(this.URLsSettings.rootStorageURL)
            let root
            if (response.ok) {
                root = await response.json()
            } else {
                root = "error"
            }
            let pathChildren
            if (this.status !== "create") {
                let response2 = await fetch(
                    this.URLsSettings.pathToChemicalURL +
                    String(this.initialData.id)
                )
                pathChildren = await response2.json()
            } else {
                pathChildren = null
            }
            this.tree = new Tree({
                tree_container: this.$refs.tree_container,
                input_name: "treeOutput",
                root: root,
                path_to_node: pathChildren,
                children_storages_url:
                    this.URLsSettings.childrenStoragesURL,
                mode: "chemical_editing"
            })
        }
    },
}
</script>

<style>
/*Not scoped! It breaks tree!*/
.tree {
    background: snow;
    min-height: 100px;
    min-width: 95%;
    margin: 10px;
    resize: horizontal;
    overflow: auto;
    float: left;
}

.tree_container {
    position: relative;
}

.background {
    position: absolute;
    height: 100%;
    width: 100%;
}

.foreground {
    position: relative;
    height: 100%;
    width: 100%;
}

.foreground > ul {
    padding-bottom: 40px;
}

li.open {
    list-style-image: url(../assets/door-open.svg);
}

li.closed {
    list-style-image: url(../assets/door-closed.svg);
}

li.chemical {
    list-style-image: none;
    list-style-type: disc;
}

div.figure {
    margin-top: 50px;
    margin-left: 40px;
    height: 50px;
    width: 50px;
    background: bisque;
    position: relative;
}

.highlighted {
    background: red;
}

ul {
    user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
}
</style>