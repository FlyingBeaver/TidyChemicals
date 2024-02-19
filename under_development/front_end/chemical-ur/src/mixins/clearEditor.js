export default {
    methods: {
        clearEditorCommon(editorRef) {
            this.$refs[editorRef].clear()
        },
        clearEditor() {
            const editorsRefs = {
                CasRn: "casInput",
                CommentEditor: "TextInputWithFormat",
                NameEditor: "TextInputWithFormat",
                QuantityEditor: "quantityEditor",
                StructureEditor: "structureInput"
            }
            const editorRef = editorsRefs[this.$options.name]
            if (editorRef === undefined) {
                throw Error("Unknown component!")
            }
            this.clearEditorCommon(editorRef)
        },
    }
}