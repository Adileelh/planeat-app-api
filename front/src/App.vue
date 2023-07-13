
<template>
  <div>
    <Navbar />
    <router-view />
  </div>
</template>

<script>
// import Login from './components/Login.vue'
import Navbar from './components/Navbar.vue'


  export default {
    name: 'App',
    components: {
      // Login,
      Navbar,

    }
  }
</script>

<style scoped>

</style>
