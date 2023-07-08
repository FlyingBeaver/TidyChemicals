<template>
    <input type="date" v-bind:name="inputName" v-bind:disabled="disabled" class="simple_text_value">
    <label class="date-single-checkbox">
        <input
            type="checkbox"
            v-bind:name="inputName.concat('_include')"
            class="checkbox"
        >
        <div class="pretty-checkbox">
            <div class="indicator">
            </div>
        </div>
        <div class="checkbox-text">include date above in the range</div>
    </label>
</template>

<script>
export default {
    name: "DateInput",
    props: ["inputName", "disabled"]
}
</script>

<style>
    label.date-single-checkbox {
        display: grid;
        grid-template-columns: 0 30px 1fr;
        grid-template-rows: 30px;
        margin-top: 10px;
    }
    input.checkbox {
        border: 0;
        width: 0;
        height: 0;
        opacity: 0;
        position: static;
    }
    div.checkbox-text {
        color: cornflowerblue;
        margin: auto;
    }
    /* unchecked */
    div.pretty-checkbox {
        width: 30px;
        height: 30px;
        border: solid cornflowerblue 3px;
        box-sizing: border-box;
    }
    div.indicator {
        width: 0;
        height: 0;
        opacity: 0;
    }
    /* under cursor */
    div.pretty-checkbox:hover {
        background-color: white;
    }
    /* checked */
    input.checkbox:checked ~ div.pretty-checkbox {
        background: cornflowerblue;
    }
    input.checkbox:checked ~ div.pretty-checkbox > div.indicator {
        position: relative;
        opacity: 100%;
        left: 9px;
        top: 5px;
        width: 5px;
        height: 10px;
        border: solid white;
        border-width: 0 3px 3px 0;
        transform: rotate(45deg);
    }
</style>