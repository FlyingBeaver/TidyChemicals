<template>
    <div>
        <p class="section-header">
            Created by:
        </p>
        <p>
            <a v-bind:href="createdHref">
                {{this.initialData.created_by}}
            </a>
        </p>
        <p class="section-header">
            Creation date:
        </p>
        <p>{{dateCreated}}</p>
        <p class="section-header">
            Last change by:
        </p>
        <p>
            <a v-bind:href="lastChangeByHref">
                {{this.initialData.last_change_by}}
            </a>
        </p>
        <p class="section-header">
            Last change date:
        </p>
        <p>{{dateUpdated}}</p>
    </div>
    <div></div>
</template>

<script>
export default {
    name: "UsersDates",
    props: ["initialData"],
    inject: ["URLsSettings"],
    methods: {
        formatDate(date) {
            let day = String(date.getDate())
            let dayString = (day.length === 1 ? "0" : "") + day + "."
            let month = String(date.getMonth() + 1)
            let monthString = (month.length === 1 ? "0" : "") + month + "."
            let year = String(date.getFullYear())
            return dayString + monthString + year
        }
    },
    computed: {
        dateCreated() {
            let date = new Date(this.initialData.creation_date)
            return this.formatDate(date)
        },
        dateUpdated() {
            let date = new Date(this.initialData.last_change_date)
            return this.formatDate(date)
        },
        createdHref() {
            if ("created_by" in this.initialData) {
                return (
                    this.URLsSettings.usersURL +
                    this.initialData.created_by.slice(1)
                )
            } else {
                return ""
            }
        },
        lastChangeByHref() {
            if ("last_change_by" in this.initialData) {
                return (
                    this.URLsSettings.usersURL +
                    this.initialData.last_change_by.slice(1)
                )
            } else {
                return ""
            }
        }
    }
}
</script>

<style>

</style>
