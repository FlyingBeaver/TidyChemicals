<template>
    <header-component></header-component>
    <div class="content-main">
        <form method="post"
              v-on:submit.prevent="doNothing"
              ref="form"
              action="http://127.0.0.1:5000/show_request/"
        >
            <form-row 
                v-for="id in rowsIds"
                v-bind:key="id"
                v-bind:row-id="id"
                v-bind:deletion-mode-on="deletionMode"
                v-on:mouse-enter-happened="fireBroRow"
                v-on:mouse-leave-happened="unfire"
                v-on:click-happened="deleteRowsPair"
                v-bind:fired-id="firedId"
            >
            </form-row>
            <button-box 
                v-on:add-condition="addCondition"
                v-on:toggle-deletion-mode="toggleDeletionMode"
                v-bind:deletion-mode="deletionMode"
                v-bind:rows-number="rowsNumber"
                v-bind:submit-form="submitForm"
            ></button-box>
        </form>
    </div>
</template>



<script>
import HeaderComponent from './components/HeaderComponent.vue'
import FormRow from './components/FormRow.vue'
import ButtonBox from './components/ButtonBox.vue'

export default {
    name: 'App',
    components: {
        HeaderComponent,
        FormRow,
        ButtonBox
    },
    data() {
        return {
            rowsIds: ["subform0"],
            subformsCounter: 1,
            deletionMode: false,
            firedId: "",
            debug: true,
        }
    },
    methods: {
        fireBroRow(rowId) {
            let broIndex = null;
            let rowIndex = this.rowsIds.indexOf(rowId);
            if (rowIndex === this.rowsIds.length - 1) {
                broIndex = this.rowsIds.length - 2;
            } else {
                if (rowIndex % 2 === 0) {
                    broIndex = rowIndex + 1;
                } else {
                    broIndex = rowIndex - 1;
                }
            }
            this.firedId = this.rowsIds[broIndex];
        },
        deleteRowsPair(rowId) {
            let fired = this.firedId;
            this.rowsIds.splice(this.rowsIds.indexOf(rowId), 1)
            this.rowsIds.splice(this.rowsIds.indexOf(fired), 1)
            for (let index = 0; index < this.rowsIds.length; index++) {
                if (index === 0 || index === this.rowsIds.length - 1) {
                    if (this.rowsIds[index].includes("_plus_")) {
                        throw Error("first or last item in array is connector")
                    }
                } else {
                    if ((this.rowsIds[index].includes(this.rowsIds[index - 1]) &&
                         this.rowsIds[index].includes(this.rowsIds[index + 1])) ||
                         !(this.rowsIds[index].includes("_plus_"))) {
                        continue;
                    } else {
                        this.rowsIds[index] = (this.rowsIds[index - 1] + 
                            "_plus_" + this.rowsIds[index + 1])
                    }
                }
            }
            if (this.rowsIds.length === 1) {
                this.toggleDeletionMode()
            }
        },
        unfire() {
            this.firedId = "";
        },
        addCondition() {
            let oldLastSubform = this.rowsIds.slice(-1)[0];
            let newSubform = "subform" + String(this.subformsCounter);
            this.subformsCounter += 1;
            let newSeparatorId = oldLastSubform + "_plus_" + newSubform;
            this.rowsIds.push(newSeparatorId);
            this.rowsIds.push(newSubform);
        },
        toggleDeletionMode() {
            if (this.deletionMode) {
                this.$refs.form.classList.remove("deletion_mode");
                this.deletionMode = false;
            } else {
                this.$refs.form.classList.add("deletion_mode");
                this.deletionMode = true;
            }
        },
        doNothing() {
        },
        submitForm() {
            this.$refs.form.submit();
        }
    },
    computed: {
        rowsNumber() {
            return this.rowsIds.length
        }
    },
    mounted() {
        if (!this.debug) {
            let csrfContainer = document.querySelector("#csrf")
            let csrfInput = csrfContainer.querySelector("input")
            let newCsrfInput = csrfInput.cloneNode(true)
            this.$refs.form.prepend(newCsrfInput)
        }
    }
}
</script>



<style>

body {
  padding: 0;
  margin: 0;
  background-color: Azure;
  font-family: Roboto, sans-serif; }

/* Header format! */
.header {
  background-color: CornflowerBlue;
  color: Azure;
  width: 100%;
  height: 120px;
  display: flex;
  justify-content: space-between; }

.logo-container {
  height: 100%;
  flex-basis: 50px;
  margin-left: 30px;
  display: flex;
  align-items: center; }

.buttons-container {
  height: 100px;
  margin-right: 30px;
  padding: 10px 0 10px 0;
  display: grid;
  grid-template-columns: minmax(min-content, auto) 1fr;
  grid-gap: 10px; }

.show-username {
  color: Azure;
  grid-row: 1/3; }

.light-button {
  display: flex;
  background-color: Azure;
  color: CornflowerBlue;
  height: 45px;
  width: 150px;
  font-size: 24px;
  align-items: center;
  justify-content: center;
  cursor: pointer; }
  .light-button:link {
    text-decoration: none; }
  .light-button:hover {
    text-decoration: underline; }

/* content format */
.content-main {
  display: flex;
  justify-content: center; }

form {
  display: flex;
  flex-direction: column;
  flex-basis: 100%; }
  form:disabled {
    background-color: Azure;
    opacity: 50%; }

div.row {
  margin: 0 80px 0 80px;
  border: none;
  flex-basis: 100%;
  flex-direction: row;
  display: grid;
  grid-template-columns: 285px 285px 285px;
  grid-template-rows: auto auto;
  grid-column-gap: 20px;
  justify-content: space-between; }
  .deletion_mode div.row:hover, div.row.fired {
    background-color: DarkOrange;
    cursor: url("./assets/Vector.svg"), pointer; }
  .deletion_mode div.row#buttons_box:hover {
    cursor: default;
    background-color: Azure; }
  div.row:nth-child(1) {
    margin-top: 80px; }

.column {
  min-height: 65px;
  height: auto;
  margin: 0; }

p.row.appendix {
  grid-column: 1/4;
  background-color: Bisque; }

@media (max-width: 863px) {
  div.row {
    flex-direction: column;
    align-items: center;
    margin: 80px 0 0 0; } }

div.operator_between_box {
  grid-column: 2/4;
  display: flex;
  justify-content: center;
  padding-bottom: 30px;
  padding-top: 30px; }

.simple_text_value, .only_num_value, .inactive-field, form select {
  font-size: 18px;
  color: CornflowerBlue;
  background-color: Azure;
  border: solid CornflowerBlue 3px;
  width: 285px;
  height: 45px;
  padding-left: 8px; }

form select {
  appearance: none;
  -moz-appearance: none;
  -webkit-appearance: none;
  background-image: url("./assets/Triangle_in_square.svg");
  background-position: right;
  background-repeat: no-repeat;
  background-size: 45px; }
  form select:hover, form select:focus {
    background-color: white; }
  form select:disabled, form select:disabled:hover {
    background-color: Azure;
    opacity: 50%;
    cursor: url("./assets/Vector.svg"), pointer; }
  form select > option {
    padding-left: 0; }

.inactive-field {
  box-sizing: border-box;
  display: flex;
  align-items: center;
  opacity: 50%; }

.simple_text_value, .only_num_value {
  box-sizing: border-box; }
  .simple_text_value:focus, .only_num_value:focus {
    background-color: white; }
  .simple_text_value:disabled, .only_num_value:disabled, .simple_text_value:disabled:hover {
    background-color: Azure;
    opacity: 50%;
    cursor: url("./assets/Vector.svg"), pointer; }

#exit_from_deletion, #search_button, .dark_button {
  box-sizing: border-box;
  font-size: 18px;
  width: 285px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center; }

.dark_button {
  color: Azure;
  background-color: CornflowerBlue;
  border: solid CornflowerBlue 3px; }
  .dark_button:hover {
    color: white;
    border: solid RoyalBlue 3px;
    background-color: RoyalBlue; }
  .dark_button:active {
    color: white;
    border: solid MidnightBlue 3px;
    background-color: MidnightBlue; }
  .dark_button:disabled, .dark_button:disabled:hover, .dark_button:disabled:active {
    opacity: 65%;
    background-color: CornflowerBlue;
    border: solid CornflowerBlue 3px; }

#search_button {
  color: white;
  font-weight: 700;
  background-color: DodgerBlue;
  border: solid DodgerBlue 3px; }
  #search_button:hover {
    border: solid blue 3px;
    background-color: blue; }
  #search_button:active {
    border: solid Crimson 3px;
    background-color: Crimson; }

#exit_from_deletion {
  color: white;
  border: solid Crimson 3px;
  background-color: Crimson; }
  #exit_from_deletion:hover {
    border: solid DarkRed 3px;
    background-color: DarkRed; }
  #exit_from_deletion:active {
    border: solid #4d0000 3px;
    background-color: #4d0000; }

div#buttons_box {
  margin-top: 10px;
  display: grid;
  grid-template-rows: 1fr;
  grid-template-columns: 1fr;
  align-self: end;
  grid-row-gap: 20px;
  cursor: default; }

.warning {
  background: Peachpuff;
  margin: 10px 10px 10px 10px;
  font-family: sans-serif;
  color: maroon;
  padding: 10px 10px 10px 10px; }

</style>