<template>
    <div class="date-range-wrapper">
        <input type="date" v-bind:name="inputName" v-bind:disabled="disabled" class="narrow-date-input">
        <input type="date" v-bind:name="inputName" v-bind:disabled="disabled" class="narrow-date-input">
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
                v-bind:name="inputName.concat('_include_left')"
                class="checkbox"
            >
            <div class="pretty-checkbox">
                <div class="indicator">
                </div>
            </div>
            <div class="checkbox-text">include date above</div>
        </label>
    </div>
</template>

<script>
export default {
    name: "DateRangeInput",
    props: ["inputName", "disabled"]
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
        margin-bottom: 10px;
    }
    div.pretty-checkbox {
        width: 30px;
        height: 30px;
        border: solid cornflowerblue 3px;
        box-sizing: border-box;
        align-self: center;
    }
</style>