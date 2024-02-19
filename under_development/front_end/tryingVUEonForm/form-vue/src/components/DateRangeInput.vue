<template>
    <div class="date-range-wrapper">
        <input v-model="leftDate" type="date" v-bind:name="inputName" v-bind:disabled="disabled" class="narrow-date-input">
        <input v-model="rightDate" type="date" v-bind:name="inputName" v-bind:disabled="disabled" class="narrow-date-input">
        <div class="date-warning" v-show="showWarning">
            Left date must be before the right date
        </div>
    </div>
</template>

<script>
export default {
    name: "DateRangeInput",
    props: ["inputName", "disabled"],
    computed: {
        showWarning() {
            if (this.leftDate !== "" && this.rightDate !== "") {
                let leftDateObj = new Date(this.leftDate)
                let rightDateObj = new Date(this.rightDate)
                return rightDateObj < leftDateObj
            } else {
                return false
            }
        }
    },
    data() {
        return {
            leftDate: "",
            rightDate: ""
        }
    }
}
</script>

<style>
</style>