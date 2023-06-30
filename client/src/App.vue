<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="has-background-grey-dark">
    <section className="hero is-primary has-text-centered">
      <div className="hero-body">
        <p className="title">Cynerio Project</p>
      </div>
    </section>
    <RouterView />
  </div>
</template>