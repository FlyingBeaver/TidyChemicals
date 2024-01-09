<template>
    <button
        class="dark_button"
        v-on:click.prevent="toggleEditor"
    >{{ editorIsOn ? "Hide editor" : "Show editor" }}</button>
    <div class="tree" v-show="editorIsOn">
        <div class="tree_container" ref="tree_container">
            <div class="background"></div>
            <div class="foreground" data-root_id="0" data-root_name="root">
                <ul>
                    <li class="closed"><span data-storage_node_id="0">root</span></li>
                </ul>
            </div>
        </div>
    </div>
    <input type="hidden" v-bind:name="inputName">
</template>

<script>
import {Tree} from "@/components/trees_editor05";

export default {
    name: "StoragePlaceInput",
    props: ["disabled", "inputName"],
    data() {
        return {
            editorIsOn: false,
            tree: null,
            selectedStorages: ""
        }
    },
    methods: {
        toggleEditor() {
            this.editorIsOn = !this.editorIsOn
        },
        updateField(newValue) {
            this.selectedStorages = JSON.stringify(newValue)
        }
    },
    async mounted() {
        let response = await fetch("http://localhost:5000/root/")
        let root
        if (response.ok) {
            root = await response.json()
        } else {
            root = "error"
        }
        this.tree = new Tree(
            this.$refs.tree_container,
            this.inputName,
            root
        )
    },
}
</script>

<style>
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