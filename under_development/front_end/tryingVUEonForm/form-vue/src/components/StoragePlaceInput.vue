<template>
    <button
        class="dark-button"
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
import {Tree} from "@/components/trees_editor05.js";

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
</style>