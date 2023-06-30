<template>
    <div class="container is-fluid">
        <form @submit.prevent="onSubmitUser" class="box">
            <div class="field">
                <label class="label">Create User Form:</label>
                <div class="control">
                    <input class="input" type="text" placeholder="Enter username" v-model="userName" required>
                </div>
            </div>
            <div class="field">
                <div class="control">
                    <button class="button is-success" type="submit">Create User</button>
                </div>
            </div>
        </form>

        <button class="button is-danger" @click="onCreateTaskReportClicked">Show Tasks Reports</button>

        <div class="modal" :class="{ 'is-active': isShowTasksReportModal }">
            <div class="modal-background" @click="isShowTasksReportModal = false"></div>
            <div class="modal-card">
                <header class="modal-card-head">
                    <p class="modal-card-title">Task Details</p>
                    <button class="delete" aria-label="close" @click="isShowTasksReportModal = false"></button>
                </header>
                <section class="modal-card-body">
                    <TasksReport :task-report-list="tasksReportList" />
                </section>
            </div>
        </div>

        <UserCard v-for="user in usersList" :key="user.id" :user="user" />
    </div>
</template>

<script setup>

import { onMounted, ref } from 'vue';
import UserCard from './UserCard.vue';
import TasksReport from './TasksReport.vue';
import UserService from '../services/UserService';
import TaskService from '../services/TaskService';

let usersList = ref([]);
let userName = ref("");
let isShowTasksReportModal = ref(false)
let tasksReportList = ref([]);

onMounted(async () => {
    try {
        const response = await UserService.getAllUsers();
        usersList.value = response.data.sort((a, b) => a.name.localeCompare(b.name));
    }
    catch (error) {
        console.error(error);
    }
})

const onSubmitUser = async () => {
    try {
        const response = await UserService.createUser(userName.value);
        usersList.value.push(response.data);
        userName.value = "";
    }
    catch (error) {
        console.error(error);
    }
}

const onCreateTaskReportClicked = async () => {
    try {
        const response = await TaskService.createTaskReport();
        tasksReportList.value = response.data;
        isShowTasksReportModal.value = true;
    } catch (error) {
        console.error(error);
    }
}

</script>

