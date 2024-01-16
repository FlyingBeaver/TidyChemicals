<template>
    <div>
        <p class="section-header">
            Location:
        </p>
        <p v-if="status !== 'location'">
            {{location}}
        </p>
        <div class="tree" v-else>
            <div class="tree_container" ref="tree_container">
                <div class="background"></div>
                <div class="foreground" data-root_id="0" data-root_name="root">
                    <ul>
                        <li class="closed"><span data-storage_node_id="0">root</span></li>
                    </ul>
                </div>
            </div>
        </div>
        <input type="hidden" name="treeOutput" ref="treeOutput">
        <div v-if="status === 'location'">
            <button
                v-on:click="localCompleteEditing"
            >Complete editing</button>
            <button
                v-on:click="setChoose"
            >Discard changes</button>
        </div>
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
import {Tree} from "./trees_editor05.js";

export default {
    name: "Location",
    props: ["status", "initialData", "editedData"],
    inject: [
        "sectionChosen",
        "completeEditing",
        "updateStorageId",
        "setChoose",
    ],
    data() {
        return {
            editorIsOn: false,
            tree: null,
            selectedStorages: "",
        }
    },
    methods: {
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
            this.sectionChosen(this.$options.name.toLowerCase())
            let response = await fetch("http://localhost:5000/root/")
            let root
            if (response.ok) {
                root = await response.json()
            } else {
                root = "error"
            }
            console.log(this.initialData.id)
            let response2 = await fetch(
                "http://localhost:5000/path_to_chemical/" +
                String(this.initialData.id)
            )
            let pathChildren = await response2.json()
            this.tree = new Tree(
                this.$refs.tree_container,
                "treeOutput",
                root,
                pathChildren
            )
        }
    },
    computed: {
        location() {
            if ("location" in this.editedData) {
                return this.editedData.location
            } else if ("location" in this.initialData) {
                return this.initialData.location
            } else {
                return null
            }
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