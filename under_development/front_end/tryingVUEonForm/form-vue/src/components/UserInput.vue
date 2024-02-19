<template>
    <button
        class="dark-button"
        v-on:click.prevent="toggleEditor"
    >{{ editorIsOn ? "Hide widget" : "Show widget" }}
    </button>
    <div class="user-input-container" v-show="editorIsOn">
        <p class="prompt-width-3"
        >Start typing below name of a user you want to select</p>
        <input
            type="text"
            class="wide-text-input"
            v-bind:name="inputName"
            v-bind:disabled="disabled"
            v-model="inputContent"
            v-on:keyup.down="reactOnKeyDown"
            v-on:keydown.down.prevent=""
            v-on:keyup.up="reactOnKeyUp"
            v-on:keydown.up.prevent=""
            v-on:keyup.enter="reactOnKeyEnter"
            v-on:keydown.enter.prevent=""
        >
        <div class="selected-users">
            <p
                v-for="(id, index) in chosenUsers"
                v-bind:key="id"
                v-bind:class="{'one-user': true, 'highlighted-username': index === highlightedUserIndex && highlightInChosen}"
                v-on:click="unselectUser(id)"
            >{{ showName(id) }}
            </p>
            <p
                v-if="chosenUsersEmpty"
                class="nobody"
            >No one chosen!</p>
        </div>
        <div v-bind:class="{'users-to-select': true, 'small-grid': recentShown}">
            <div>
                <p
                    v-for="(id, index) in usersToChoose"
                    v-bind:key="id"
                    v-bind:class="{'one-user': true, 'highlighted-username': index === highlightedUserIndex && !highlightInChosen}"
                    v-on:click="selectUser(id)"
                >{{ showName(id) }}
                </p>
            </div>
            <div v-if="recentShown">
                <p
                    v-for="id in usersToChoose"
                    v-bind:key="id"
                    v-on:click="deleteUserFromRecent(id)"
                    class="cross"
                >X</p>
            </div>
        </div>
        <div class="left-label">Full name</div>
        <label class="pretty-toggle">
            <input
                type="checkbox"
                class="pretty-toggle-checkbox"
                v-model="usernameIsOn"
            >
            <span class="toggle-indicator"></span>
        </label>
        <div class="right-label">Username</div>
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
            highlightedUserIndex: null,
            highlightInChosen: false,
        }
    },
    methods: {
        reactOnKeyEnter() {
            if (this.highlightInChosen) {
                this.unselectUser(this.chosenUsers[this.highlightedUserIndex])
            } else {
                this.selectUser(this.usersToChoose[this.highlightedUserIndex])
            }
            this.highlightedUserIndex = null
            this.highlightInChosen = false
        },
        nullGuardUp() {
            if (this.highlightedUserIndex === null) {
                if (this.usersToChoose.length > 0) {
                    this.highlightedUserIndex = this.usersToChoose.length - 1
                    return
                }
                if (this.chosenUsers.length > 0) {
                    this.highlightedUserIndex = this.chosenUsers.length - 1
                    this.highlightInChosen = true
                    return
                }
            }
        },
        reactOnKeyUp() {
            this.nullGuardUp()

            if (this.highlightedUserIndex > 0) {
                this.highlightedUserIndex--
            } else if (
                this.highlightedUserIndex === 0 &&
                !this.highlightInChosen
            ) {
                if (this.chosenUsers.length > 0) {
                    this.highlightInChosen = true
                    this.highlightedUserIndex = this.chosenUsers.length - 1
                } else {
                    this.highlightedUserIndex = this.usersToChoose.length - 1
                }
            } else if (
                this.highlightedUserIndex === 0 &&
                this.highlightInChosen
            ) {
                if (this.usersToChoose.length > 0) {
                    this.highlightInChosen = false
                    this.highlightedUserIndex = this.usersToChoose.length - 1
                } else if (this.chosenUsers.length > 0) {
                    this.highlightedUserIndex = this.chosenUsers.length - 1
                }
            }
        },
        nullGuardDown() {
            if (this.highlightedUserIndex === null) {
                if (this.usersToChoose.length > 0) {
                    this.highlightedUserIndex = 0
                    return
                }
                if (this.chosenUsers.length > 0) {
                    this.highlightedUserIndex = 0
                    this.highlightInChosen = true
                    return
                }
            }
        },
        reactOnKeyDown() {
            this.nullGuardDown()

            if (this.highlightInChosen) {
                if (this.highlightedUserIndex <
                    this.chosenUsers.length - 1
                ) {
                    this.highlightedUserIndex++
                } else if (this.usersToChoose.length > 0) {
                    this.highlightInChosen = false
                    this.highlightedUserIndex = 0
                } else {
                    this.highlightedUserIndex = 0
                }
            } else {
                if (this.highlightedUserIndex <
                    this.usersToChoose.length - 1
                ) {
                    this.highlightedUserIndex++
                } else if (this.chosenUsers.length > 0) {
                    this.highlightInChosen = true
                    this.highlightedUserIndex = 0
                } else {
                    this.highlightedUserIndex = 0
                }
            }
        },
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
            return (this.chosenUsers.length === 0)
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
                        if (this.chosenUsers.indexOf(username) !== -1) {
                            continue
                        }
                        if (username.toLowerCase()
                                .indexOf(value.toLowerCase()) !== -1) {
                            usersToShow.push(username)
                        }
                    }
                } else {
                    for (let username in this.usersObject) {
                        if (this.chosenUsers.indexOf(username) !== -1) {
                            continue
                        }
                        if (this.usersObject[username].toLowerCase()
                                .indexOf(value.toLowerCase()) !== -1) {
                            usersToShow.push(username)
                        }
                    }
                }
                this.usersToChoose = usersToShow
                this.recentShown = false
            }
            this.highlightedUserIndex = null
            this.highlightInChosen = false
        },
    },
    beforeMount() {
        let usersPromise = fetch("http://127.0.0.1:5000/users/")
        usersPromise.then(this.getUsers)
    }
}
</script>

<style>
</style>