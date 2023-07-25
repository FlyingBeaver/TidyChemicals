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
        v-model="inputContent"
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
    <div v-bind:class="{users:true, 'small-grid':recentShown}" v-show="editorIsOn">
        <div>
            <p
                v-for="id in usersToChoose"
                v-bind:key="id"
                v-on:click="selectUser(id)"
            >{{ showName(id) }}
            </p>
        </div>
        <div v-if="recentShown">
            <p
                v-for="id in usersToChoose"
                v-bind:key="id"
                v-on:click="deleteUserFromRecent(id)"
            >X</p>
        </div>
    </div>
    <input
        type="hidden"
        v-bind:name="'real_' + inputName"
        ref="real_input"
        v-bind:value="chosenUsersStr"
    >
    <input
        type="hidden"
        v-bind:name="'delFromRecent_' + inputName"
        ref="delFromRecent"
        v-bind:value="deletedFromRecentStr"
    >
</template>

<script>
export default {
    name: "UserInput",
    props: ["disabled", "inputName"],
    data() {
        return {
            editorIsOn: false,
            usernameIsOn: false,
            recentShown: true,
            usersObject: {},
            chosenUsers: [],
            usersToChoose: [],
            recent: [],
            deletedFromRecent: [],
            inputContent: "",
        }
    },
    methods: {
        toggleEditor() {
            this.editorIsOn = !this.editorIsOn
        },
        async getUsers(response) {
            let responseObj = await response.json()
            this.usersObject = responseObj["users"]
            this.usersToChoose = responseObj["recent"]
            this.recent = responseObj["recent"]
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
        deleteUserFromRecent(id) {
            let index = this.recent.indexOf(id)
            if (index !== -1) {
                this.recent.splice(index, 1)
                this.deletedFromRecent.push(id)
            }
        },
    },
    computed: {
        chosenUsersEmpty() {
            return (JSON.stringify(this.chosenUsers) === '[]')
        },
        chosenUsersStr() {
            return JSON.stringify(this.chosenUsers)
        },
        deletedFromRecentStr() {
            return JSON.stringify(this.deletedFromRecent)
        }
    },
    watch: {
        inputContent(value) {
            if (value === "") {
                this.usersToChoose = this.recent
                this.recentShown = true
            } else {
                let usersToShow = []
                if (this.usernameIsOn) {
                    for (let username in this.usersObject) {
                        if (username.toLowerCase()
                                .indexOf(value.toLowerCase()) !== -1) {
                            usersToShow.push(username)
                        }
                    }
                } else {
                    for (let username in this.usersObject) {
                        if (this.usersObject[username].toLowerCase()
                                .indexOf(value.toLowerCase()) !== -1) {
                            usersToShow.push(username)
                        }
                    }
                }
                this.usersToChoose = usersToShow
                this.recentShown = false
            }
        },
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
div.small-grid {
    display: grid;
    grid-template-columns: 1fr 20px;
}
</style>