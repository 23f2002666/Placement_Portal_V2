<template>
  <div class="login-page">
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 border-bottom border-secondary">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand fw-bold fs-4">
          Placement Portal
        </router-link>
        <div class="ms-auto d-flex gap-2">
          <router-link to="/" class="btn btn-success btn-sm px-3">Home</router-link>
          <router-link to="/register" class="btn btn-success btn-sm px-3">Register</router-link>
        </div>
      </div>
    </nav>

    <div class="login-container d-flex align-items-center justify-content-center">
      <div class="card shadow-lg border-0 p-4" style="width: 400px; border-radius: 15px;">
        <div class="card-body">
          <h2 class="text-center mb-4 fw-normal">🔐 Login</h2>
          <form @submit.prevent="login">
            <div class="mb-3 text-start">
              <label class="form-label text-secondary small mb-1">Username</label>
              <input 
                type="email" 
                class="form-control form-control-lg fs-6" 
                placeholder="Enter username"
                v-model="email" 
                required
              >
            </div>

            <div class="mb-4 text-start">
              <label class="form-label text-secondary small mb-1">Password</label>
              <input 
                type="password" 
                class="form-control form-control-lg fs-6" 
                placeholder="Enter password"
                v-model="password" 
                @input="validatePassword" 
                required
              >
              <div v-if="passwordError" class="form-text text-danger tiny">
                {{ passwordError }}
              </div>
            </div>

            <div class="d-grid">
              <button class="btn btn-primary btn-lg fs-6 fw-bold" type="submit">
                Login
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const email = ref('');
const password = ref('');
const passwordError = ref('');

const validatePassword = () => {
    if (password.value.length < 8) {
        passwordError.value = 'Minimum 8 characters required.';
        return false;
    } else {
        passwordError.value = '';
        return true; 
    }
};

async function login() {
    if (!validatePassword()) return;
    
    try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email.value, password: password.value })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('auth_token', data.user.auth_token);
            const userRole = data.user.roles[0];
            localStorage.setItem('user_role', userRole);

            if (userRole === 'admin') router.push('/admin');
            else if (userRole === 'company') router.push('/company');
            else if (userRole === 'student') router.push('/student');
            
            alert("Success!");
        } else {
            alert('Login failed: ' + data.message);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Could not connect to the server.");
    }
}
</script>

<style scoped>
.login-page {
  background: radial-gradient(circle, #4d4d4d 0%, #1a1a1a 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.login-container {
  flex-grow: 1;
}

.btn-primary {
  background-color: #007bff;
  border: none;
  padding: 12px;
}

.btn-success {
  background-color: #198754;
  border: none;
}

.tiny {
  font-size: 0.75rem;
}
</style>