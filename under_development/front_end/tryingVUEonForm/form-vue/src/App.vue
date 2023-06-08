<template>
    <header-component></header-component>
    <div class="content-main">
        <form method="post">
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
            firedId: ""
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
            console.log("now!");
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
                let form = document.querySelector("form");
                form.classList.remove("deletion_mode");
                this.deletionMode = false;
            } else {
                let form = document.querySelector("form");
                form.classList.add("deletion_mode");
                this.deletionMode = true;
            }
        }
    }
}
</script>



<style>
  body {
      padding: 0;
      margin: 0;
      background-color: azure;
      font-family: Roboto, sans-serif;
  }
  /* Header format */

  .header {
      background-color: CornflowerBlue;
      color: azure;
      width: 100%;
      height: 120px;
      display: flex;
      justify-content: space-between;
  }

  .logo-container {
      height: 100%;
      flex-basis: 50px;
      margin-left: 30px;
      display: flex;
      align-items: center;
  }

  .buttons-container {
      height: 100px;
      margin-right: 30px;
      padding: 10px 0 10px 0;
      display: grid;
      grid-template-columns: minmax(min-content, auto) 1fr;
      grid-gap: 10px;
  }

  .show-username{
      color: azure;
      grid-row: 1/3;
  }

  .light-button {
      display: flex;
      background-color: azure;
      color: cornflowerblue;
      height: 45px;
      width: 150px;
      font-size: 24px;
      align-items: center;
      justify-content: center;
  }

  .light-button:link {
      text-decoration: none;
  }

  .light-button:hover {
      text-decoration: underline;
  }

  /* content format */
  .content-main {
      display: flex;
      justify-content: center;
  }

  form {
      display: flex;
      flex-direction: column;
      flex-basis: 100%;
  }

  div.row.fired,
  form.deletion_mode div.row:hover {
      background-color: darkorange;
      cursor: url("./assets/Vector.svg"), pointer;
  }

  form.deletion_mode div.row#buttons_box:hover {
      cursor: default;
      background-color: azure;
  }

  form:disabled {
      background-color: azure;
      opacity: 50%;
  }

  div.row {
      margin: 0 80px 0 80px;
      border: none;
      flex-basis: 100%;
      height: 300px;
      flex-direction: row;
      display: grid;
      grid-template-columns: 285px 285px 285px;
      grid-template-rows: 65px;
      grid-column-gap: 20px;
      justify-content: space-between;
  }

  div.row:nth-child(1) {
      margin-top: 80px;
  }

  div.row > p {
      height: 50px;
      margin: 0;
  }

  p.row.appendix {
      grid-column: 1/4;
      background-color: bisque;
  }


  form select {
      font-size: 18px;
      color: cornflowerblue;
      background-color: azure;
      border: solid cornflowerblue 3px;
      border-radius: 0;
      width: 285px;
      height: 45px;
      padding-left: 8px;
      appearance: none;
      -moz-appearance: none;
      -webkit-appearance: none;
      background-image: url("./assets/Triangle_in_square.svg");
      background-position: right;
      background-repeat: no-repeat;
      background-size: 45px;
  }

  form select:hover  {
      background-color: white;
  }

  form select:focus  {
      background-color: white;
  }

  /*form.deletion_mode select:hover:disabled {*/
  /*    background-color: azure;*/
  /*}*/

  form.deletion_mode:hover input:not(.dark_button),
  form.deletion_mode:hover select:not(.dark_button),
  form.deletion_mode:hover button:not(.dark_button),
  form.deletion_mode select:hover:not(.dark_button),
  form.deletion_mode select:focus:not(.dark_button),
  form.deletion_mode button:hover:not(.dark_button),
  form.deletion_mode button:focus:not(.dark_button),
  form.deletion_mode input:hover:not(.dark_button),
  form.deletion_mode input:focus:not(.dark_button) {
      background-color: azure;
      opacity: 50%;
      cursor: url("./assets/Vector.svg"), pointer;
  }

  .inactive-field {
      box-sizing: border-box;
      font-size: 18px;
      color: cornflowerblue;
      background-color: azure;
      border: solid cornflowerblue 3px;
      border-radius: 0;
      padding-left: 8px;
      width: 285px;
      height: 45px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      opacity: 50%;
  }

  select > option {
      padding-left: 0;
  }

  @media (max-width: 863px) {
      div.row {
          flex-direction: column;
          align-items: center;
          margin: 80px 0 0 0;
      }
  }

  .simple_text_value, .only_num_value {
      box-sizing: border-box;
      font-size: 18px;
      color: cornflowerblue;
      background-color: azure;
      border: solid cornflowerblue 3px;
      border-radius: 0;
      padding-left: 8px;
      width: 285px;
      height: 45px;
      display: flex;
      flex-direction: column;
      justify-content: center;
  }

  .simple_text_value:focus, .only_num_value:focus {
      background-color: white;
  }

  .dark_button {
      box-sizing: border-box;
      font-size: 18px;
      color: azure;
      background-color: cornflowerblue;
      border: solid cornflowerblue 3px;
      border-radius: 0;
      width: 285px;
      height: 45px;
      display: flex;
      align-items: center;
      justify-content: center;
  }

  .dark_button:disabled {
      opacity: 65%;
  }

  #more_conditions:hover, #delete_button:hover {
      color: white;
      border: solid royalblue 3px;
      background-color: royalblue;
  }

  #more_conditions:active,
  #delete_button:active {
      color: white;
      border: solid midnightblue 3px;
      background-color: midnightblue;
  }

  div#buttons_box:nth-child(-n+3) #delete_button {
      display: none;
  }

  form.deletion_mode #delete_button,
  form.deletion_mode #more_conditions {
      display: none;
  }

  form:not(.deletion_mode) #exit_from_deletion,
  form:not(.deletion_mode) #more_conditions_disabled {
      display: none;
  }

  #search_button {
      color: white;
      font-weight: 700;
      background-color: dodgerblue;
      border: solid dodgerblue 3px;
  }

  #search_button:hover {
      color: white;
      border: solid blue 3px;
      background-color: blue;
  }

  form #exit_from_deletion,
  button#search_button:active {
      color: white;
      border: solid crimson 3px;
      background-color: crimson;
  }

  form button#exit_from_deletion:hover {
      color: white;
      border: solid darkred 3px;
      background-color: darkred;
  }

  form button#exit_from_deletion:active {
      color: white;
      border: solid rgb(77, 0, 0) 3px;
      background-color: rgb(77, 0, 0);
  }

  div#buttons_box {
      margin-top: 10px;
      display: grid;
      grid-template-rows: 1fr;
      grid-template-columns: 1fr;
      align-self: end;
      grid-row-gap: 20px;
      cursor: default;
  }

  div.operator_between_box {
      grid-column: 2/4;
      display: flex;
      justify-content: center;
  }

  div.row.fired {
      background-color: darkorange;
  }
</style>
