<template>
    <div id="ifKetcher" v-on:click="getMolPromise">
        <html lang="en">
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width,initial-scale=1" />
                <meta name="theme-color" content="#000000" />
                <meta name="description" content="Ketcher is a web-based chemical structure editor" />
                <link rel="shortcut icon" type="image/x-icon" href="./static/favicon.ico" />
                <link rel="icon" type="image/png" sizes="32x32" href="./static/favicon-32x32.png" />
                <link rel="icon" type="image/png" sizes="16x16" href="./static/favicon-16x16.png" />
                <link rel="apple-touch-icon" sizes="180x180" href="./static/apple-touch-icon.png" />
                <link rel="manifest" href="./static/manifest.json" />
                <title>Ketcher v2.6.4</title>
            </head>
            <body><noscript>You need to enable JavaScript to run this app.</noscript>
                <div id="root"></div>
            </body>
        </html>
    </div>
    <input type="hidden" value="" v-bind:name="inputName" ref="hiddenInput">
</template>

<script>
import {qazqwerty} from './static/static/js/jsviewer.js'
export default {
    name: "StructureInput",
    mounted() {
        qazqwerty()
    },
    methods: {
        updateInput(result) {
            this.$refs.hiddenInput.value = result
        },
        getMolPromise() {
            let molPromise = window.ketcher.getMolfile()
            molPromise.then(this.updateInput)
        }
    },
    props: ["inputName"]
}
</script>

<style>
@import "./static/static/css/main.8e693d51.css";

div#ifKetcher {
    height: 400px;
}

</style>