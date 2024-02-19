<template>
    <header-component></header-component>
    <div class="content-main">
        <form method="post"
              v-on:submit.prevent="doNothing"
              class="search-form"
              ref="form"
              action="http://127.0.0.1:5000/show_request/"
              autocomplete="off"
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
  justify-content: center;
  padding-top: 60px; }

.narrow-date-input, .simple-text-input, .wide-text-input, .narrow-text-input, .inactive-field, .wide-select, .narrow-select {
  font-size: 18px;
  color: CornflowerBlue;
  background-color: Azure;
  border: solid CornflowerBlue 3px;
  width: 285px;
  height: 45px;
  padding-left: 8px; }

.wide-select, .narrow-select {
  appearance: none;
  -moz-appearance: none;
  -webkit-appearance: none;
  background-image: url("./assets/Triangle_in_square.svg");
  background-position: right;
  background-repeat: no-repeat;
  background-size: 45px; }
  .wide-select:hover, .narrow-select:hover, .wide-select:focus, .narrow-select:focus {
    background-color: white; }
  .wide-select:disabled, .narrow-select:disabled, .wide-select:disabled:hover {
    background-color: Azure;
    opacity: 50%;
    cursor: url("./assets/trash.svg"), pointer; }
  .wide-select > option, .narrow-select > option {
    padding-left: 0; }

.narrow-select {
  width: auto; }

.inactive-field {
  box-sizing: border-box;
  display: flex;
  align-items: center;
  opacity: 50%; }

.simple-text-input, .wide-text-input, .narrow-text-input {
  box-sizing: border-box; }
  .simple-text-input:focus, .wide-text-input:focus, .narrow-text-input:focus {
    background-color: white; }
  .simple-text-input:disabled, .wide-text-input:disabled, .narrow-text-input:disabled, .simple-text-input:disabled:hover {
    background-color: Azure;
    opacity: 50%;
    cursor: url("./assets/trash.svg"), pointer; }

.narrow-date-input {
  width: auto;
  box-sizing: border-box; }

.narrow-text-input {
  grid-column: span 1;
  width: auto; }

.wide-text-input {
  grid-column: span 3;
  width: auto; }

.exit-from-deletion, .search-button, .dark-button {
  box-sizing: border-box;
  font-size: 18px;
  width: 285px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center; }
  .exit-from-deletion:hover, .search-button:hover, .dark-button:hover, .exit-from-deletion:active, .search-button:active, .dark-button:active {
    cursor: pointer; }
  .exit-from-deletion:disabled:hover, .search-button:disabled:hover, .dark-button:disabled:hover, .exit-from-deletion:disabled:active, .search-button:disabled:active, .dark-button:disabled:active {
    cursor: inherit; }

.dark-button {
  color: Azure;
  background-color: CornflowerBlue;
  border: solid CornflowerBlue 3px; }
  .dark-button:hover {
    color: white;
    border: solid RoyalBlue 3px;
    background-color: RoyalBlue; }
  .dark-button:active {
    color: white;
    border: solid MidnightBlue 3px;
    background-color: MidnightBlue; }
  .dark-button:disabled, .dark-button:disabled:hover, .dark-button:disabled:active {
    opacity: 65%;
    background-color: CornflowerBlue;
    border: solid CornflowerBlue 3px; }

.search-button {
  color: white;
  font-weight: 700;
  background-color: DodgerBlue;
  border: solid DodgerBlue 3px; }
  .search-button:hover {
    border: solid blue 3px;
    background-color: blue; }
  .search-button:active {
    border: solid Crimson 3px;
    background-color: Crimson; }

.exit-from-deletion {
  color: white;
  border: solid Crimson 3px;
  background-color: Crimson; }
  .exit-from-deletion:hover {
    border: solid DarkRed 3px;
    background-color: DarkRed; }
  .exit-from-deletion:active {
    border: solid #4d0000 3px;
    background-color: #4d0000; }

.search-form {
  display: flex;
  flex-direction: column;
  flex-basis: 100%; }
  .search-form:disabled {
    background-color: Azure;
    opacity: 50%; }

.row, .buttons-box {
  margin: 0 60px 0 60px;
  padding: 20px;
  border: none;
  flex-basis: 100%;
  display: grid;
  grid-template-columns: 285px 285px 285px;
  grid-template-rows: auto auto;
  grid-column-gap: 20px;
  justify-content: space-between; }
  .deletion_mode .row:hover, .deletion_mode .buttons-box:hover, .row.fired, .fired.buttons-box {
    background-color: DarkOrange;
    cursor: url("./assets/trash.svg"), pointer; }

.column {
  height: auto; }

@media (max-width: 863px) {
  .row, .buttons-box {
    grid-template-columns: 285px;
    align-items: center;
    justify-content: center; }
  .column {
    margin: 10px; } }

.operator-between {
  grid-column: 2/4;
  display: flex;
  justify-content: center; }

.buttons-box {
  margin-top: 10px;
  display: grid;
  grid-template-rows: 1fr;
  grid-template-columns: 1fr;
  align-self: end;
  grid-row-gap: 20px;
  cursor: default; }
  .deletion_mode .buttons-box:hover {
    cursor: default;
    background-color: Azure; }

.single-checkbox {
  display: grid;
  grid-template-columns: 0 30px 1fr;
  grid-template-rows: 30px;
  margin-top: 10px; }

input.checkbox {
  border: 0;
  width: 0;
  height: 0;
  opacity: 0;
  position: static; }
  input.checkbox:checked ~ .pretty-checkbox {
    background: Cornflowerblue; }
  input.checkbox:checked ~ .pretty-checkbox > .indicator {
    position: relative;
    display: inline-block;
    opacity: 100%;
    left: 9px;
    top: 5px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 3px 3px 0;
    transform: rotate(45deg); }

.checkbox-text {
  color: Cornflowerblue;
  margin: auto; }

.pretty-checkbox {
  width: 30px;
  height: 30px;
  border: solid Cornflowerblue 3px;
  box-sizing: border-box; }
  .pretty-checkbox:hover {
    background-color: white; }

.indicator {
  width: 0;
  height: 0;
  opacity: 0; }

.tree {
  background: Snow;
  min-height: 100px;
  min-width: 95%;
  margin: 10px;
  resize: horizontal;
  overflow: auto;
  float: left; }
  .tree .tree_container {
    position: relative; }
  .tree .background {
    position: absolute;
    height: 100%;
    width: 100%; }
  .tree .foreground {
    position: relative;
    height: 100%;
    width: 100%; }
  .tree .highlighted {
    background: red; }
  .tree .figure {
    margin-top: 50px;
    margin-left: 40px;
    height: 50px;
    width: 50px;
    background: Bisque;
    position: relative; }
  .tree ul {
    user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none; }
    .foreground > .tree ul {
      padding-bottom: 40px; }
  .tree li.open {
    list-style-image: url(./assets/door-open.svg); }
  .tree li.closed {
    list-style-image: url(./assets/door-closed.svg); }
  .tree li.chemical {
    list-style-image: url(./assets/jar.svg); }

#standalone-container {
  margin: auto;
  max-width: 720px; }

#editor-container {
  height: 45px;
  border: solid Cornflowerblue; }

#toolbar-container {
  margin: -25px 0 0 0; }

.ql-toolbar.ql-snow {
  padding: 0; }

.ql-editor.ql-blank {
  overflow-y: hidden; }

.greek-palette {
  bottom: 25px;
  right: 0;
  border: 1px Grey solid;
  background: white;
  position: absolute;
  width: 432px;
  height: 81px;
  display: grid;
  grid-template: repeat(3, 1fr)/repeat(16, 1fr); }
  .greek-palette .input-button {
    width: 27px;
    height: 27px; }

.ql-formats {
  position: relative; }

.pretty-toggle {
  grid-column: span 1;
  width: 100%;
  background-color: CornflowerBlue;
  height: 25px;
  cursor: pointer;
  position: relative;
  margin-top: 10px;
  margin-bottom: 10px; }
  .pretty-toggle .pretty-toggle-checkbox {
    height: 0;
    width: 0;
    opacity: 0; }
    .pretty-toggle .pretty-toggle-checkbox:checked ~ .toggle-indicator {
      right: 0;
      position: absolute;
      background-color: white;
      margin-top: 3px;
      margin-right: 3px;
      margin-bottom: 3px;
      height: 19px;
      width: 19px; }
  .pretty-toggle .toggle-indicator {
    display: inline-block;
    background-color: white;
    margin-top: 3px;
    margin-left: 3px;
    margin-bottom: 3px;
    height: 19px;
    width: 19px; }

.left-label {
  grid-column: span 1;
  justify-self: end;
  align-self: center;
  margin-right: 10px;
  color: CornflowerBlue; }

.right-label {
  grid-column: span 1;
  justify-self: start;
  align-self: center;
  margin-left: 10px;
  color: CornflowerBlue; }

.prompt, .prompt-width-3, .warning, .warning-width-3, .warning-width-2, .date-warning {
  margin: 10px;
  padding: 10px;
  font-family: sans-serif; }

.warning, .warning-width-3, .warning-width-2, .date-warning {
  background: Peachpuff;
  color: maroon; }

.date-warning {
  margin: 0 10px 10px 10px;
  grid-column: span 3; }

.warning-width-2 {
  grid-column: span 2; }

.warning-width-3 {
  grid-column: span 3; }

.prompt, .prompt-width-3 {
  background: #cde4fa;
  color: CornflowerBlue; }

.prompt-width-3 {
  grid-column: span 3; }

.user-input-container {
  display: grid;
  grid-template-columns: 40% 20% 40%;
  grid-template-rows: auto;
  margin-top: 5px; }

.selected-users .nobody, .users-to-select .one-user, .selected-users .one-user, .users-to-select .cross, .selected-users .cross {
  color: CornflowerBlue;
  padding-left: 5px;
  margin-top: 10px;
  margin-bottom: 10px; }

.users-to-select, .selected-users {
  border: solid CornflowerBlue 3px;
  grid-column: span 3; }
  .users-to-select .one-user.highlighted-username, .selected-users .one-user.highlighted-username, .users-to-select .cross.highlighted-username, .selected-users .cross.highlighted-username {
    background-color: CornflowerBlue;
    color: Azure; }
  .users-to-select .one-user:hover, .selected-users .one-user:hover, .users-to-select .cross:hover, .selected-users .cross:hover {
    background-color: white;
    cursor: pointer; }

.selected-users {
  border-top: 0;
  border-bottom: 0; }

.small-grid {
  display: grid;
  grid-template-columns: 1fr 20px; }

.date-range-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 10px; }

.column.ketcher-container {
  grid-column-start: 2;
  grid-column-end: 4; }

/*Needed for non-iframe ketcher*/
textarea.cliparea {
  display: none; }

/*These two rules for StructureInput*/
div#ifKetcher {
  height: 400px; }

div.disabled {
  opacity: 50%;
  background-color: Azure; }

.three-columns-container {
  display: grid;
  grid-template-columns: 31% 31% 31%;
  column-gap: 3.5%; }

.two-columns-container {
  display: grid;
  grid-template-columns: 48% 48%;
  column-gap: 4%; }

</style>