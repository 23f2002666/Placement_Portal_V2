<script setup>
import { RouterView, useRouter, useRoute } from 'vue-router';
import { ref, watchEffect, computed } from 'vue';

const router = useRouter();
const route = useRoute(); 

// Global state - helpful if you want to use these later
const role = ref(localStorage.getItem('user_role'));
const isAuthenticated = ref(!!localStorage.getItem('auth_token'));

// Sync state whenever the route changes or user logs in/out
watchEffect(() => {
  role.value = localStorage.getItem('user_role');
  isAuthenticated.value = !!localStorage.getItem('auth_token');
});

// We keep this computed property to ensure we don't accidentally 
// add padding to your professional dark pages.
const isCustomPage = computed(() => {
  const customPages = ['/', '/login', '/register', '/student', '/admin', '/company'];
  return customPages.includes(route.path);
});

const logout = () => {
  localStorage.clear();
  router.push('/login');
};
</script>

<template>
  <!-- 
    We do NOT put a <nav> here anymore because you have built 
    special dark navbars inside Home, Login, and StudentView.
  -->
  <div :class="isCustomPage ? 'full-page-wrapper' : 'container mt-4'">
    <RouterView />
  </div>
</template>

<style>
/* 
  This CSS is what fixed your "Full Page" problem. 
  It removes the white gaps at the edges.
*/
html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  height: 100%;
  background-color: #1a1a1a; /* Matches the dark background */
  overflow-x: hidden;
}

#app {
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}

.full-page-wrapper {
  width: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}
</style>