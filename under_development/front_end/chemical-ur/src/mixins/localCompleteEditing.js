export default {
    methods: {
        localCompleteEditing() {
            const editorsRefs = {
                CasRn: "casInput",
                CommentEditor: "TextInputWithFormat",
                NameEditor: "TextInputWithFormat",
                QuantityEditor: "quantityEditor",
            }
            const editorRef = editorsRefs[this.$options.name]
            if (editorRef === undefined) {
                throw Error("Unknown component!")
            }
            this.$refs[editorRef].localCompleteEditing()
        },
    }
}