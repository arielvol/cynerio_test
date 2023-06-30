<template>
    <div class="container is-fluid">
        <form @submit.prevent="onSubmitUser" class="box mt-5">
            <div class="field">
                <label class="label">Create User Form:</label>
                <div class="control">
                    <input class="input" type="text" placeholder="Enter user name" v-model="userName" required>
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
                    <TasksReport :task-report="tasksReport" />
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
import { createErrorMessage } from '../utils/utils';

import toastr from 'toastr';
import 'toastr/toastr.scss';

let usersList = ref([]);
let userName = ref("");
let isShowTasksReportModal = ref(false)
let tasksReport = ref({});

onMounted(async () => {
    try {
        const response = await UserService.getAllUsers();
        usersList.value = response.data.sort((a, b) => a.name.localeCompare(b.name));
    }
    catch (error) {
        const msg = createErrorMessage(error);
        toastr.error(msg, 'Error fetching users');
    }
})

const onSubmitUser = async () => {
    try {
        const response = await UserService.createUser(userName.value);
        usersList.value.push(response.data);
        userName.value = "";
    }
    catch (error) {
        const msg = createErrorMessage(error);
        toastr.error(msg, 'Error Creating User');
    }
}

const onCreateTaskReportClicked = async () => {
    try {
        const response = await TaskService.createTaskReport();
        tasksReport.value = response.data;
        isShowTasksReportModal.value = true;
    } catch (error) {
        const msg = createErrorMessage(error);
        toastr.error(msg, 'Error creating Task Report');
    }
}

</script>

