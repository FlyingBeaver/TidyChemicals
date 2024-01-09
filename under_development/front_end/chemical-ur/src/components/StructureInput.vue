<template>
    <iframe id="ifKetcher"
            ref="ifKetcher"
            name="ifKetcher"
            src="http://localhost:5000/"
            width="650"
            height="400"
            v-on:load="$emit('ketcherLoaded')"
    >
    </iframe>
</template>

<script>
export default {
    name: "StructureInput",
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
            console.log("sending message...")
        },
        getMolecule() {
            let ifKetcherWindow = window.frames.ifKetcher
            ifKetcherWindow.postMessage('{"action": "getMolecule", "pictureNeeded": true}', "*")
        },
    },
    props: ["inputName", "disabled"]
}
</script>

<style>

</style>