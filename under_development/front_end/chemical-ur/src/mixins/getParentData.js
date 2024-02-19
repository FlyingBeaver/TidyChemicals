const ensure = function(object, keys) {
    if (keys.length === 1) {
        const key = keys[0]
        return (key in object && object[key] !== null)
    } else if (keys.length === 2) {
        const [key1, key2] = keys
        return (
            key1 in object &&
            key2 in object[key1] &&
            object[key1][key2] !== null
        )
    }
}


const extract = function (object, keys) {
    if (keys.length === 1) {
        const key = keys[0]
        return object[key]
    } else if (keys.length === 2) {
        const [key1, key2] = keys
        return object[key1][key2]
    }
}


export default {
    methods: {
        parentData(keysArr, blank) {
            if (ensure(this.editedData, keysArr)) {
                return extract(this.editedData, keysArr)
            } else if (ensure(this.initialData, keysArr)) {
                return extract(this.initialData, keysArr)
            } else {
                return blank
            }
        }
    }
}