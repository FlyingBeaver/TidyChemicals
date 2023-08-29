<template>
    <div id="standalone-container">
        <div id="toolbar-container" ref="toolbar">
            <span class="ql-formats">
                <button class="ql-bold"></button>
                <button class="ql-italic"></button>
                <button class="ql-script" value="sub"></button>
                <button class="ql-script" value="super"></button>
            </span>
                <span class="ql-formats">
                <button class="input-button" data-character="prime"
                        v-on:click.prevent="enterSymbol">′</button>
                <button class="input-button" data-character="plus_minus"
                        v-on:click.prevent="enterSymbol">±</button>
                <button class="input-button" data-character="em_dash"
                        v-on:click.prevent="enterSymbol">—</button>
                <button class="input-button" v-on:click.prevent="toggleGreek">ΑΩ</button>
                <div v-bind:class="{'greek-palette': true, 'hide-me': greekAlphabetHidden}"
                     v-on:click.prevent="enterSymbol">
                    <button class="input-button" data-character="capital_alpha">Α</button>
                    <button class="input-button" data-character="alpha">α</button>
                    <button class="input-button" data-character="capital_beta">Β</button>
                    <button class="input-button" data-character="beta">β</button>
                    <button class="input-button" data-character="capital_gamma">Γ</button>
                    <button class="input-button" data-character="gamma">γ</button>
                    <button class="input-button" data-character="capital_delta">Δ</button>
                    <button class="input-button" data-character="delta">δ</button>
                    <button class="input-button" data-character="capital_epsilon">Ε</button>
                    <button class="input-button" data-character="epsilon">ε</button>
                    <button class="input-button" data-character="capital_zeta">Ζ</button>
                    <button class="input-button" data-character="zeta">ζ</button>
                    <button class="input-button" data-character="capital_eta">Η</button>
                    <button class="input-button" data-character="eta">η</button>
                    <button class="input-button" data-character="capital_theta">Θ</button>
                    <button class="input-button" data-character="theta">θ</button>
                    <button class="input-button" data-character="capital_iota">Ι</button>
                    <button class="input-button" data-character="iota">ι</button>
                    <button class="input-button" data-character="capital_kappa">Κ</button>
                    <button class="input-button" data-character="kappa">κ</button>
                    <button class="input-button" data-character="capital_lambda">Λ</button>
                    <button class="input-button" data-character="lambda">λ</button>
                    <button class="input-button" data-character="capital_mu">Μ</button>
                    <button class="input-button" data-character="mu">μ</button>
                    <button class="input-button" data-character="capital_nu">Ν</button>
                    <button class="input-button" data-character="nu">ν</button>
                    <button class="input-button" data-character="capital_xi">Ξ</button>
                    <button class="input-button" data-character="xi">ξ</button>
                    <button class="input-button" data-character="capital_omicron">Ο</button>
                    <button class="input-button" data-character="omicron">ο</button>
                    <button class="input-button" data-character="capital_pi">Π</button>
                    <button class="input-button" data-character="pi">π</button>
                    <button class="input-button" data-character="capital_rho">Ρ</button>
                    <button class="input-button" data-character="rho">ρ</button>
                    <button class="input-button" data-character="capital_sigma">Σ</button>
                    <button class="input-button" data-character="sigma">σ</button>
                    <button class="input-button" data-character="capital_tau">Τ</button>
                    <button class="input-button" data-character="tau">τ</button>
                    <button class="input-button" data-character="capital_upsilon">Υ</button>
                    <button class="input-button" data-character="upsilon">υ</button>
                    <button class="input-button" data-character="capital_phi">Φ</button>
                    <button class="input-button" data-character="phi">φ</button>
                    <button class="input-button" data-character="capital_chi">Χ</button>
                    <button class="input-button" data-character="chi">χ</button>
                    <button class="input-button" data-character="capital_psi">Ψ</button>
                    <button class="input-button" data-character="psi">ψ</button>
                    <button class="input-button" data-character="capital_omega">Ω</button>
                    <button class="input-button" data-character="omega">ω</button>
                </div>
            </span>
        </div>
        <div
            class="editor-container"
            id="editor-container"
            ref="editor"
        ></div>
        <!-- здесь будет всплывать предупреждение при вводе недопустимых символов -->
        <div v-bind:class="{warning: true, 'hide-me': warningHidden}">You are trying to enter a character that is not allowed in this field. Only digits, latin and greek letters with no diacritics, space, full stop (period), comma, (), [], {}, +, -, /, :, ;, ±, — and ′ are allowed.</div>
    </div>
</template>

<script>
import {characters, characters_in_string, difference} from "./constants.js";
import Quill from "quill"
export default {
    name: "TextInputWithFormat",
    data() {
        return {
            editor: null,
            greekAlphabetHidden: true,
            warningHidden: true,
            text: "",
            charactersSet: new Set(characters_in_string),
            qlEditor: null,
            contentInputContent: "",
            formattingInputContent: "",
        }
    },
    props:
        ["content"],
    methods: {
        showWarning() {
            this.warningHidden = false
        },
        hideWarning() {
            this.warningHidden = true
        },
        toggleGreek() {
            this.greekAlphabetHidden = !this.greekAlphabetHidden
        },
        enterSymbol(event) {
            let character = characters[event.target.dataset.character]
            let quill_range = this.editor.getSelection()
            let selection_start = quill_range.index
            let selection_length = quill_range.length
            if (selection_length > 0) {
                console.log("delete3")
                this.editor.deleteText(selection_start, selection_length)
            }
            this.editor.insertText(selection_start, character)
            this.editor.setSelection(selection_start + 1)
        },
        checkInserted(delta, oldDelta, source) {
            console.log(delta)
            let insertedCharacter = ""
            let delta_ops = delta.ops
            for (let i = 0; i < delta_ops.length; i++) {
                if ("insert" in delta_ops[i]) {
                    insertedCharacter = delta_ops[i].insert
                }
            }
            if (insertedCharacter !== "" && insertedCharacter.length === 1 &&
                characters_in_string.indexOf(insertedCharacter) === -1) {
                this.showWarning()
                let fullText = this.editor.getText(0, this.editor.getLength())
                let position = fullText.indexOf(insertedCharacter)
                console.log("delete1")
                this.editor.deleteText(position, 1, "silent")
                let selectionRange = this.editor.getSelection()
                let newPosition = selectionRange.index
                // Otherwise, cursor moves forward. Strange, but works:
                setTimeout(
                    () => this.editor.setSelection(newPosition, 0),
                    0
                )
            } else if (insertedCharacter !== "" && insertedCharacter.length > 1 &&
                difference(new Set(insertedCharacter), this.charactersSet).size > 0) {
                this.showWarning()
                let fullText = this.editor.getText(0, this.editor.getLength() - 1)
                let oddChars = difference(new Set(fullText), this.charactersSet)
                console.log(oddChars)
                for (let char of oddChars) {
                    while (fullText.indexOf(char) !== -1) {
                        console.log("delete2")
                        let charPosition = fullText.indexOf(char)
                        this.editor.deleteText(charPosition, 1, "silent")
                        fullText = this.editor.getText(0, this.editor.getLength() - 1)
                    }
                }
            }
            if (!this.warningHidden &&
                characters_in_string.indexOf(insertedCharacter) !== -1) {
                this.hideWarning()
            }
        },
        updateInputs() {
            this.contentInputContent = this
                .editor.getText(0, this.editor.getLength() - 1)
            this.formattingInputContent = this.qlEditor.innerHTML
        },
        localCompleteEditing() {
            this.completeEditing("name_delta", this.editor.getContents())
            this.completeEditing("name_code", this.formattingInputContent)
        }
    },
    mounted() {
        this.editor = new Quill(
            this.$refs.editor,
            {
                modules: {
                    formula: false,
                    syntax: false,
                    toolbar: this.$refs.toolbar
                },
                placeholder: '',
                theme: "snow"
            }
        )
        this.editor.root.setAttribute('spellcheck', false)
        this.editor.on("text-change", this.checkInserted)
        this.qlEditor = this.$refs.editor.querySelector(".ql-editor")
        this.editor.on("text-change", this.updateInputs)
        this.editor.setContents(this.content)
    },
    inject: ["completeEditing"]
}
</script>

<style>
    @import "quill.snow.css";
    #standalone-container {
        margin: auto;
        max-width: 720px;
    }
    #editor-container {
        height: 45px;
        border: solid cornflowerblue;
    }

    #toolbar-container {
        margin: -25px 0 0 0;
    }

    div.ql-toolbar.ql-snow {
        padding: 0;
    }

    div.ql-editor.ql-blank {
        overflow-y: hidden;
    }

    .greek-palette {
        bottom:25px;
        right: 0;
        border: 1px grey solid;
        background: white;
        position: absolute;
        width: 432px;
        height: 81px;
        display: grid;
        grid-template: repeat(3, 1fr) / repeat(16, 1fr);
    }

    div.greek-palette button.input-button {
        width: 27px;
        height: 27px;
    }

    span.ql-formats {
        position: relative;
    }

    .hide-me {
        display: none;
    }

    div.warning {
        background: peachpuff;
        margin: 10px 10px 10px 10px;
        font-family: sans-serif;
        color: maroon;
        padding: 10px 10px 10px 10px;
    }

    div.disabled {
        opacity: 50%;
        background-color: azure;
    }
</style>