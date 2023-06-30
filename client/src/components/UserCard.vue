<template>
  <div class="card mt-4 has-background-success-light">
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <p class="title is-4">{{ user.name }}</p>
          <button class="button is-info" @click="isModalActive = true">Add Task</button>
        </div>
      </div>
    </div>
    <div v-if="tasksList && tasksList.length > 0" class="mt-4">
      <h2 class="title is-5 ml-5">Tasks:</h2>
      <TaskCard v-for="task in tasksList" :key="task.id" :task="task" />
    </div>
    <div class="modal" :class="{ 'is-active': isModalActive }">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">New Task</p>
          <button class="delete" aria-label="close" @click="isModalActive = false"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Task</label>
            <div class="control">
              <input class="input" type="text" placeholder="Enter task" v-model="newTask" required>
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="addTask">Add Task</button>
          <button class="button" @click="isModalActive = false">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TaskService from '../services/TaskService';
import TaskCard from './TaskCard.vue'

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
})

let newTask = ref('')
let isModalActive = ref(false)
let tasksList = ref([])

onMounted(async () => {
  try {
    const response = await TaskService.getUserTasks(props.user.id);
    tasksList.value = response.data.tasks;
  }
  catch (error) {
    console.error(error);
  }
})

const addTask = async () => {
  try {
    const response = await TaskService.createTask(newTask.value, props.user.id);
    const returnedTask = response.data;
    tasksList.value.push(returnedTask);

    isModalActive.value = false
    newTask.value = ''
  } catch (error) {
    console.error(error);
  }
}
</script>
