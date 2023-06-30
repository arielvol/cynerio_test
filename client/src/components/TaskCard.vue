<template>
    <div class="card mt-4 has-background-info-light">
        <div class="card-content">
            <div class="columns is-vcentered">
                <div class="column">
                    <p class="title is-4">{{ currentTask.name }}</p>
                </div>
                <div class="column">
                    <button class="button is-primary" @click="toggleCheckIn">{{ currentTask.status === 'checkout' ?
                        'Checkin' : 'Checkout' }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, onMounted } from 'vue'
import TaskService from '../services/TaskService';

const props = defineProps({
    task: {
        type: Object,
        required: true,
    },
})

onMounted(() => {
    currentTask.value = {...props.task}
})

let currentTask = ref({})

const toggleCheckIn = async () => {
    try {
        let response = null;
        if (currentTask.value.status === 'checkout') {
            response = await TaskService.checkInTask(currentTask.value.id)
        } else {
            response = await TaskService.checkOutTask(currentTask.value.id)
        }
        const task = response.data.task;
        currentTask.value.status = task.status;
    } catch (error) {
        console.error(error);
    }
}
</script>