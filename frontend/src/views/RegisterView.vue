<template>
  <div class="register-page">
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 border-bottom border-secondary">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand d-flex align-items-center">
          <span class="fw-bold fs-4 text-white">Placement Portal</span>
        </router-link>
        <div class="ms-auto d-flex gap-2">
          <router-link to="/" class="btn btn-success btn-sm px-3">Home</router-link>
          <router-link to="/login" class="btn btn-success btn-sm px-3">Login</router-link>
        </div>
      </div>
    </nav>

    <div class="register-container d-flex align-items-center justify-content-center py-5">
      <div class="card shadow-lg border-0 p-4" style="width: 480px; border-radius: 15px;">
        <div class="card-body">
          <h2 class="text-center mb-4 fw-normal">📝 Register</h2>

          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label class="form-label text-secondary small fw-bold">REGISTER AS</label>
              <select v-model="form.role" class="form-select form-select-lg fs-6" required>
                <option value="student">Student</option>
                <option value="company">Company / Recruiter</option>
              </select>
            </div>

            <div class="mb-3">
              <label class="form-label text-secondary small mb-1">Email address</label>
              <input type="email" v-model="form.email" class="form-control" placeholder="name@example.com" required>
            </div>

            <div class="mb-3">
              <label class="form-label text-secondary small mb-1">Password</label>
              <input type="password" v-model="form.password" class="form-control" placeholder="Min 8 characters" required>
            </div>

            <hr class="my-4 text-secondary opacity-25">

            <div v-if="form.role === 'student'" class="animate-fade-in">
              <div class="mb-3">
                <label class="form-label text-secondary small mb-1">Full Name</label>
                <input type="text" v-model="form.full_name" class="form-control" placeholder="John Doe" required>
              </div>
              <div class="mb-3">
                <label class="form-label text-secondary small mb-1">Roll Number</label>
                <input type="text" v-model="form.roll_number" class="form-control" placeholder="e.g. 2024CS01" required>
              </div>
            </div>

            <div v-if="form.role === 'company'" class="animate-fade-in">
              <div class="mb-3">
                <label class="form-label text-secondary small mb-1">Company Name</label>
                <input type="text" v-model="form.company_name" class="form-control" placeholder="Google / Microsoft" required>
              </div>
              <div class="mb-3">
                <label class="form-label text-secondary small mb-1">HR Mobile Number</label>
                <input type="text" v-model="form.hr_mobile" class="form-control" placeholder="Email or Phone" required>
              </div>
            </div>

            <div class="d-grid mt-4">
              <button class="btn btn-primary btn-lg fs-6 fw-bold" type="submit" :disabled="loading">
                {{ loading ? 'Creating Account...' : 'Register' }}
              </button>
            </div>
          </form>

          <div class="text-center mt-4">
            <span class="text-muted small">Already have an account? </span>
            <router-link to="/login" class="text-primary fw-bold text-decoration-none small">
              Login
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(false);

const form = reactive({
    role: 'student',
    email: '',
    password: '',
    full_name: '',
    roll_number: '',
    company_name: '',
    hr_contact: ''
});

async function handleRegister() {
    if (form.password.length < 8) {
        alert("Password must be at least 8 characters");
        return;
    }

    loading.value = true;
    try {
        const response = await fetch('http://127.0.0.1:5000/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form)
        });

        const data = await response.json();

        if (response.ok) {
            alert("Registration successful! Please login.");
            router.push('/login');
        } else {
            alert("Error: " + data.message);
        }
    } catch (error) {
        alert("Could not connect to server");
    } finally {
        loading.value = false;
    }
}
</script>

<style scoped>
.register-page {
  background: radial-gradient(circle, #4d4d4d 0%, #1a1a1a 100%);
  min-height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
}

.register-container {
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

.form-control, .form-select {
    border-radius: 8px;
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>