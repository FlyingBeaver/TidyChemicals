<template>
    <iframe
        v-on:load="$emit('ketcherLoaded')"
        v-bind:src="URLsSettings.ketcherIframeURL"
        id="ifKetcher"
        ref="ifKetcher"
        name="ifKetcher"
        width="650"
        height="400"
    >
    </iframe>
</template>

<script>
import {emptyMol} from "../utils/constants.js"

export default {
    name: "StructureInput",
    inject: ["URLsSettings"],
    props: ["inputName", "disabled"],
    emits: ["ketcherLoaded"],
    data() {
        return {
            ketcherInstance: null
        }
    },
    methods: {
        setMolecule(molBlock) {
            let message = {action: "setMolecule", molBlock: molBlock}
            let messageStr = JSON.stringify(message)
            let ifKetcherWindow = window.frames.ifKetcher
            ifKetcherWindow.postMessage(messageStr, "*")
        },
        getMolecule() {
            let ifKetcherWindow = window.frames.ifKetcher
            ifKetcherWindow.postMessage('{"action": "getMolecule", "pictureNeeded": true}', "*")
        },
        clear() {
            this.setMolecule(emptyMol)
        },
    },
}
</script>

<style>

</style>