export default {
    methods: {
        discardChangesCommon(key) {
            if (key in this.editedData) {
                delete this.editedData[key]
            }
            this.setChoose()
        },
        discardChanges() {
            const keys = {
                CasRn: "cas",
                CommentEditor: "comment",
                NameEditor: "name_data",
                QuantityEditor: "quantity",
            }
            const key = keys[this.$options.name]
            if (key === undefined) {
                throw Error("Unknown component!")
            }
            this.discardChangesCommon(key)
        }
    }
}