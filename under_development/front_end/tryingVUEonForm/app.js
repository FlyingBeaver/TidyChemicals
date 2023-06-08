const separatorFactory = function(tag1, tag2) {
    let rawTemplate = `
<div class="row" id="subform0_plus_subform1">
  <div class="operator_between_box">
    <select name="subform0_plus_subform1" required="">
      <option value="" selected="">AND / NOT / AND NOT</option>
      <option value="and">And</option>
      <option value="or">Or</option>
      <option value="and_not">And not</option>
    </select>
  </div>
</div>`
    let newId = tag1 + "_plus_" + tag2;
    if (newId != "subform0_plus_subform1") {
        while (rawTemplate.includes("subform0_plus_subform1")) {
            rawTemplate.replace("subform0_plus_subform1", newId)
        }
    }
    return rawTemplate;
}

const config = function(tag) {
    let rawTemplate = `
            <div class="row" id="subform0">
                <p class="column">
                    <select name="subform0_term" required v-model="termValue">
                        <option value='' selected>Choose search option</option>
                        <option value='cas'>CAS RN</option>
                        <option value='comment'>Comment</option>
                        <option value='molar_mass'>Molar mass</option>
                        <option value='molecular_formula'>Molecular formula</option>
                        <option value='name'>Name</option>
                        <option value='quantity_with_unit'>Quantity</option>
                        <option value='storage_place'>Storage place</option>
                        <option value='structure'>Structure</option>
                        <option value='synonym'>Synonym</option>
                        <option value='when_created'>Creation date</option>
                        <option value='when_updated'>Last update date</option>
                        <option value='who_created'>Created by</option>
                        <option value='who_updated'>Updated by</option>
                    </select>
                </p>
                <p class="operator_box column">
                    <select name=subform0_operator required v-bind:disabled="operatorDisabled" v-model="operatorValue">
                        <option value='' selected>Choose operator</option>
                        <option v-for="(value, key) in operatorOptions" v-bind:value="key" v-bind:key="key">{{ value }}</option>
                    </select>
                </p>
                <p class="value_box column">
                    <input type="text" class="simple_text_value" name="text_value" v-if="widget === 'text_input'">
                    <span class="inactive-field" v-else>Value</span>
                </p>
            </div>`
    let rawConfig = {
        data() {
            return {
                termValue: "",
                operatorDisabled: true,
                operatorValue: "",
                supported_widgets: ["text_input"]
            }
        },
        computed: {
            operatorOptions() {
                let result = {}
                if (this.termValue === "") {
                    this.operatorDisabled = true;
                    this.operatorValue = "";
                    return {};
                } else {
                    for (let key in tree[this.termValue]) {
                        if (key !== "verbose") {
                            result[key] = tree[this.termValue][key].verbose;
                        }
                    }
                    this.operatorDisabled = false;
                    this.operatorValue = "";
                    return result;
                }
            },
            widget() {
                if (this.termValue && this.operatorValue) {
                }
                if (this.termValue && this.operatorValue) {
                    return tree[this.termValue][this.operatorValue].widget
                } else {
                    return "";
                }
            }
        },
    }
    if (tag !== "subform0") {
        while (rawTemplate.includes("subform0")) {
            rawTemplate = rawTemplate.replace("subform0", tag)
        }
    }
    rawConfig.template = rawTemplate;
    return rawConfig
}


const app = Vue.createApp({
    data() {
        return {
            subformCounter: 1
        }
    },
    methods: {
        addSearchCondition() {
            let buttons_box = document.querySelector("#buttons_box");
            let subformId = "subform" + String(this.subformCounter);
            this.subformCounter++;
            let previousId = buttons_box.previousElementSibling.getAttribute("id");
            let separator = document.createElement("sepa-rator")
            buttons_box.before(separator)
            app.component("sepa-rator", {template: separatorFactory(previousId, subformId)})
            let subform = document.createElement("sub-form");
            buttons_box.before(subform);
            let config_obj = config(subformId);
            app.component("sub-form", config_obj);
        }
    }
});

app.mount("form");

app.component("sub-form", config("subform0"));