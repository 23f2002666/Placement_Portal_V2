<template>
  <div class="profile-page-wrapper">

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 border-bottom border-secondary shadow">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold fs-4">Placement Portal</span>
        <div class="ms-auto">
          <router-link to="/student" class="btn btn-outline-light btn-sm px-3">
            <i class="bi bi-arrow-left me-1"></i> Back to Dashboard
          </router-link>
        </div>
      </div>
    </nav>

    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-6 col-md-8">
          <div class="card border-0 shadow-lg rounded-4 overflow-hidden">
            <div class="card-header bg-primary text-white text-center py-3">
              <h4 class="mb-0 fw-bold">📝 Edit My Profile</h4>
              <small class="opacity-75">Update your academic and personal details</small>
            </div>
            <div class="card-body p-4 bg-white">
              <form @submit.prevent="handleUpdate">
                
                <div class="mb-3">
                  <label class="form-label fw-bold text-secondary">Full Name</label>
                  <input type="text" v-model="form.name" class="form-control form-control-lg fs-6" required>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-bold text-secondary">Roll Number</label>
                    <input type="text" v-model="form.roll" class="form-control" required>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-bold text-secondary">Current CGPA</label>
                    <input type="number" step="0.01" v-model="form.cgpa" class="form-control" required>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-bold text-secondary">Department / Branch</label>
                  <select v-model="form.dept" class="form-select" required>
                    <option value="" disabled>Select Branch</option>
                    <option value="CS">Computer Science</option>
                    <option value="IT">Information Technology</option>
                    <option value="ECE">Electronics & Communication</option>
                    <option value="ME">Mechanical Engineering</option>
                    <option value="CE">Civil Engineering</option>
                  </select>
                </div>

                <div class="mb-4">
                  <label class="form-label fw-bold text-secondary">Key Skills</label>
                  <textarea 
                    v-model="form.skills" 
                    class="form-control" 
                    rows="3" 
                    placeholder="e.g. Java, Python, Web Development..."
                  ></textarea>
                  <div class="form-text">Separate skills with commas.</div>
                </div>

                <div class="d-grid gap-2">
                  <button type="submit" class="btn btn-primary btn-lg fw-bold" :disabled="loading">
                    {{ loading ? 'Saving Changes...' : 'Save Profile' }}
                  </button>
                  <router-link to="/student" class="btn btn-link text-decoration-none text-muted">Cancel</router-link>
                </div>

              </form>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(false);
const token = localStorage.getItem('auth_token');


const form = ref({
  name: '',
  roll: '',
  dept: '',
  cgpa: 0,
  skills: ''
});


const loadProfile = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/student/profile', {
      headers: { 'Authentication-Token': token }
    });
    if (res.ok) {
      const data = await res.json();
      form.value = { ...data.profile };
    }
  } catch (err) {
    console.error("Error loading profile:", err);
  }
};

const handleUpdate = async () => {
  loading.value = true;
  try {
    const res = await fetch('http://127.0.0.1:5000/api/student/profile', {
      method: 'PUT',
      headers: { 
        'Authentication-Token': token,
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify(form.value)
    });

    if (res.ok) {
      alert("Profile updated successfully! ✅");
      router.push('/student'); 
    } else {
      alert("Failed to update profile.");
    }
  } catch (err) {
    alert("Network error. Please try again.");
  } finally {
    loading.value = false;
  }
};

onMounted(loadProfile);
</script>

<style scoped>
.profile-page-wrapper {
  background: radial-gradient(circle, #4d4d4d 0%, #1a1a1a 100%);
  min-height: 100vh;
  width: 100%;
}

.card {
  border-radius: 15px;
}

.form-label {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>