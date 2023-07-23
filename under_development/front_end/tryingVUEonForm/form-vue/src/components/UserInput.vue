<template>
    <button
        class="dark_button"
        v-on:click.prevent="toggleEditor"
    >{{ editorIsOn ? "Hide widget" : "Show widget" }}
    </button>
    <input
        type="text"
        class="simple_text_value"
        v-bind:name="inputName"
        v-bind:disabled="disabled"
        v-show="editorIsOn"
    >
    <p
        v-show="editorIsOn"
    >Start typing name of user you want to select</p>
    <div class="username-toggle" v-show="editorIsOn">
        <div>Username</div>
        <label class="pretty-toggle">
            <input type="checkbox" v-model="usernameIsOn">
            <div class="toggle-inside"></div>
        </label>
        <div>Full name</div>
    </div>
    <div class="users" v-show="editorIsOn">
        <p
            v-for="id in chosenUsers"
            v-bind:key="id"
            v-on:click="unselectUser(id)"
        >{{ showName(id) }}
        </p>
        <p v-if="chosenUsersEmpty">No one chosen!</p>
    </div>
    <div class="users" v-show="editorIsOn">
        <p
            v-for="id in usersToChoose"
            v-bind:key="id"
            v-on:click="selectUser(id)"
        >{{ showName(id) }}
        </p>
    </div>
</template>

<script>
export default {
    name: "UserInput",
    props: ["disabled", "inputName"],
    data() {
        return {
            editorIsOn: false,
            usernameIsOn: false,
            usersObject: {},
            chosenUsers: [],
            usersToChoose: []
        }
    },
    methods: {
        toggleEditor() {
            this.editorIsOn = !this.editorIsOn
        },
        async getUsers(response) {
            this.usersObject = await response.json()
            for (let id in this.usersObject) {
                this.usersToChoose.push(id)
            }
        },
        showName(id) {
            if (this.usernameIsOn) {
                return id
            } else {
                return this.usersObject[id]
            }
        },
        selectUser(id) {
            let index = this.usersToChoose.indexOf(id)
            this.usersToChoose.splice(index, 1)
            this.chosenUsers.push(id)
        },
        unselectUser(id) {
            let index = this.chosenUsers.indexOf(id)
            this.chosenUsers.splice(index, 1)
            this.usersToChoose.push(id)
        },
    },
    computed: {
        chosenUsersEmpty() {
            return (JSON.stringify(this.chosenUsers) === '[]')
        }
    },
    beforeMount() {
        let usersPromise = fetch("http://127.0.0.1:5000/users/")
        usersPromise.then(this.getUsers)
    }
}
</script>

<style scoped>
div.username-toggle {
    display: grid;
    grid-template-columns: 40% 20% 40%;
}
input[type=checkbox] {
    height: 0;
    width: 0;
    opacity: 0;
}
label.pretty-toggle {
    width: 100%;
    background-color: cornflowerblue;
    height: 25px;
    cursor: pointer;
    position: relative;
}
/*unchecked*/
div.toggle-inside {
    background-color: white;
    margin-top: 3px;
    margin-left: 3px;
    margin-bottom: 3px;
    height: 19px;
    width: 19px;
}
input:checked ~ div.toggle-inside {
    right: 0;
    position: absolute;
    background-color: white;
    margin-top: 3px;
    /*margin-left: 35px;*/
    margin-right: 3px;
    margin-bottom: 3px;
    height: 19px;
    width: 19px;
}
div.users {
    border: solid cornflowerblue 3px;
}
div.users:last-child {
    border-top: solid cornflowerblue 1px;
}
div.users p {
    color: cornflowerblue;
    padding-left: 5px;
}
div.users p:hover {
    background-color: white;
}
</style>