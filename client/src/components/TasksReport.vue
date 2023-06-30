<template>
    <div class="section">
      <div class="container">
        <div class="is-multiline">
          <div v-for="(tasks, user) in taskReportList" :key="user">
            <div class="card mb-4 has-background-info-light">
              <header class="card-header">
                <p class="card-header-title">{{ user }}</p>
              </header>
              <div class="card-content is-contained">
                <div class="content">
                  <div class="columns is-multiline">
                    <div v-for="(time, task) in tasks" :key="task" class="column">
                      <div class="card has-background-success-light">
                        <div class="card-content">
                          <p class="title is-5">{{ task }}</p>
                          <p><strong>Hours:</strong> {{ time.hours }}</p>
                          <p><strong>Minutes:</strong> {{ time.minutes }}</p>
                          <p><strong>Seconds:</strong> {{ time.seconds }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script setup>

defineProps({
    taskReportList: {
        type: [],
        required: true,
    },
})

</script>
