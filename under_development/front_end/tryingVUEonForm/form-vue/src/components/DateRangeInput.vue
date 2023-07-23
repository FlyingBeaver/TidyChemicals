<template>
    <div class="date-range-wrapper">
        <input v-model="leftDate" type="date" v-bind:name="inputName" v-bind:disabled="disabled" class="narrow-date-input">
        <input v-model="rightDate" type="date" v-bind:name="inputName" v-bind:disabled="disabled" class="narrow-date-input">
        <label class="date-checkbox">
            <input
                type="checkbox"
                v-bind:name="inputName.concat('_include_left')"
                class="checkbox"
            >
            <div class="pretty-checkbox">
                <div class="indicator">
                </div>
            </div>
            <div class="checkbox-text">include date above</div>
        </label>
        <label class="date-checkbox">
            <input
                type="checkbox"
                v-bind:name="inputName.concat('_include_right')"
                class="checkbox"
            >
            <div class="pretty-checkbox">
                <div class="indicator">
                </div>
            </div>
            <div class="checkbox-text">include date above</div>
        </label>
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

<style scoped>
    div.date-range-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: auto auto;
        row-gap: 10px;
        column-gap: 10px;
    }
    input.narrow-date-input {
        box-sizing: border-box;
        font-size: 18px;
        color: cornflowerblue;
        background-color: azure;
        border: solid cornflowerblue 3px;
        border-radius: 0;
        padding-left: 8px;
        width: auto;
        height: 45px;
    }
    div.checkbox-text {
        color: cornflowerblue;
        margin-left: 10px;
        /*align-self: center;*/
        /*justify-self: center;*/
    }
    label.date-checkbox {
        display: grid;
        grid-template-columns: 0 30px 1fr;
        grid-template-rows: auto;
    }
    div.pretty-checkbox {
        width: 30px;
        height: 30px;
        border: solid cornflowerblue 3px;
        box-sizing: border-box;
        align-self: center;
    }
    div.date-warning {
        background: peachpuff;
        margin: 0 10px 10px 10px;
        font-family: sans-serif;
        color: maroon;
        padding: 10px 10px 10px 10px;
        grid-column-start: 1;
        grid-column-end: 3;
    }
</style>