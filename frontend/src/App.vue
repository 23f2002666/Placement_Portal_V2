<script setup>
import { RouterView, useRouter, useRoute } from 'vue-router';
import { ref, watchEffect, computed } from 'vue';

const router = useRouter();
const route = useRoute(); 


const role = ref(localStorage.getItem('user_role'));
const isAuthenticated = ref(!!localStorage.getItem('auth_token'));


watchEffect(() => {
  role.value = localStorage.getItem('user_role');
  isAuthenticated.value = !!localStorage.getItem('auth_token');
});


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
  <div :class="isCustomPage ? 'full-page-wrapper' : 'container mt-4'">
    <RouterView />
  </div>
</template>

<style>

html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  height: 100%;
  background-color: #1a1a1a;
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