<template>
  <div class="dashboard-wrapper">

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 border-bottom border-secondary">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold fs-4">Placement Portal</span>
        <div class="ms-auto d-flex gap-2">
          <button @click="exportMyHistory" class="btn btn-outline-info btn-sm px-3">
            📥 Export History (CSV)
          </button>
          <button @click="logout" class="btn btn-danger btn-sm px-3">Logout</button>
        </div>
      </div>
    </nav>

    <div v-if="upcomingDeadlines.length > 0 && showReminders" class="container mt-3">
      <div class="alert alert-warning border-warning shadow-sm d-flex align-items-center" role="alert">
        <span class="fs-4 me-3">🔔</span>
        <div>
          <h6 class="alert-heading fw-bold mb-1">Urgent Reminders</h6>
          <p class="mb-0 small" v-for="drive in upcomingDeadlines" :key="drive.id">
            The deadline for <strong>{{ drive.title }}</strong> ({{ drive.company_name }}) is tomorrow! Apply before it's too late.
          </p>
        </div>
      </div>
    </div>

    <div class="sub-header bg-primary text-white py-2 px-4 d-flex justify-content-between align-items-center shadow-sm mt-2">
      <span class="fs-6 fw-semibold">🎓 Student Dashboard</span>
      <div class="d-flex gap-3">
        <a href="#" @click.prevent="showStatusModal = true" class="text-white text-decoration-none small">Status</a>
        <router-link to="/student/profile" class="text-white text-decoration-none small">Edit Profile</router-link>
      </div>
    </div>

    <div class="container py-4">
      <div class="row mb-4">
        <div class="col-12 text-center">
          <div class="card border-0 shadow-sm py-3 rounded-3">
            <h2 class="fw-normal mb-0">Welcome, <span class="fw-bold">{{ profile.name || 'Student' }}</span>!</h2>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm h-100 rounded-3 overflow-hidden">
            <div class="card-header bg-secondary text-white text-center py-2 fw-semibold">MY PROFILE</div>
            <div class="card-body">
              <div class="profile-details">
                <p><strong>Name:</strong> {{ profile.name }}</p>
                <p><strong>Roll No:</strong> {{ profile.roll }}</p>
                <p><strong>Dept:</strong> {{ profile.dept }}</p>
                <p><strong>CGPA:</strong> {{ profile.cgpa }}</p>
              </div>
              <hr>
              <button class="btn btn-outline-primary btn-sm w-100 rounded-pill">Upload Resume</button>
            </div>
          </div>
        </div>

        <div class="col-lg-8">
          <div class="card border-0 shadow-sm h-100 rounded-3 overflow-hidden">
            <div class="card-header bg-success text-white py-2 px-3 d-flex justify-content-between align-items-center">
              <span class="fw-semibold">ACTIVE PLACEMENT DRIVES</span>
              <div class="input-group input-group-sm w-50">
                <input 
                  v-model="searchQuery" 
                  @input="handleSearch"
                  type="text" 
                  class="form-control border-0" 
                  placeholder="Search Company or Role..."
                />
                <button v-if="searchQuery" @click="clearSearch" class="btn btn-light btn-sm">✕</button>
              </div>
            </div>

            <div class="card-body bg-white text-center">
              <div v-if="drives.length === 0" class="py-5">
                <p class="text-muted">No active drives found.</p>
              </div>

              <div v-else v-for="drive in drives" :key="drive.id" class="card mb-3 text-start border-light shadow-sm">
                <div class="card-body d-flex justify-content-between align-items-center">
                  
                  <div style="flex: 1;">
                    <h5 class="fw-bold mb-0 text-dark">{{ drive.title }}</h5>
                    <small class="text-muted">{{ drive.company_name }} | Min CGPA: {{ drive.min_cgpa }}</small>
                    <a href="#" @click.prevent="viewJobDetails(drive)" class="small text-primary text-decoration-none">
                      ℹ️ View Full Details
                    </a>
                  </div>
                  <div v-if="isApplied(drive.id)" class="mx-3 text-center" style="min-width: 130px;">
                      <span :class="getStatusBadge(getApplicationStatus(drive.id))" style="font-size: 0.7rem; padding: 4px 10px; border-radius: 50px; display: inline-block;">
                        {{ getApplicationStatus(drive.id) }}
                      </span>
                  </div>
                  <div style="min-width: 100px; text-align: right;">
                    <button v-if="!isApplied(drive.id)" @click="apply(drive.id)" class="btn btn-primary btn-sm px-4 rounded-pill">Apply</button>
                    <button v-else class="btn btn-outline-secondary btn-sm px-4 rounded-pill" disabled>Applied</button>
                  </div>

                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <transition name="fade">
      <div v-if="showDetailModal" class="modal-overlay" @click.self="showDetailModal = false">
        <div class="modal-card shadow-lg" style="max-width: 500px;">
          <div class="modal-header-custom bg-light">
            <h5 class="mb-0 fw-bold">{{ selectedDrive.title }}</h5>
            <button type="button" class="btn-close" @click="showDetailModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <p class="text-muted mb-4">{{ selectedDrive.company_name }}</p>
            
            <div class="row g-3">
              <div class="col-6">
                <label class="small text-uppercase text-muted fw-bold">Package</label>
                <p class="text-success fw-bold">₹ {{ selectedDrive.package }} LPA</p>
              </div>
              <div class="col-6">
                <label class="small text-uppercase text-muted fw-bold">Min CGPA</label>
                <p>{{ selectedDrive.min_cgpa }}</p>
              </div>
              <div class="col-6">
                <label class="small text-uppercase text-muted fw-bold">Deadline</label>
                <p class="text-danger">{{ selectedDrive.deadline_date }}</p>
              </div>
            </div>

            <hr>
            <label class="small text-uppercase text-muted fw-bold">Job Description</label>
            <p class="mt-2" style="white-space: pre-line;">{{ selectedDrive.description }}</p>
          </div>
          <div class="modal-footer p-3">
            <button v-if="!isApplied(selectedDrive.id)" @click="apply(selectedDrive.id); showDetailModal = false" class="btn btn-primary w-100 rounded-pill">Apply Now</button>
            <button v-else class="btn btn-secondary w-100 rounded-pill" disabled>Already Applied</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showStatusModal" class="modal-overlay" @click.self="showStatusModal = false">
        <div class="modal-card shadow-lg">
          <div class="modal-header-custom">
            <div class="d-flex align-items-center">
              <div class="icon-circle me-3">💼</div>
              <div>
                <h5 class="mb-0 fw-bold text-dark">Application Tracking</h5>
                <small class="text-muted">Your recruitment progress</small>
              </div>
            </div>
            <button type="button" class="btn-close-custom" @click="showStatusModal = false">&times;</button>
          </div>

          <div class="modal-body-custom">
            <div class="table-responsive">
              <table class="table table-borderless align-middle mb-0">
                <thead>
                  <tr>
                    <th class="ps-3 small fw-bold text-muted">Company & Job</th>
                    <th class="small fw-bold text-muted">Applied On</th>
                    <th class="small fw-bold text-muted text-center">Status</th>
                    <th class="small fw-bold text-muted text-center">Action</th> 
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="app in history" :key="app.application_id" class="status-row">
                    <td class="ps-3 py-3">
                      <div>
                        <div class="fw-bold text-dark">{{ app.company_name }}</div>
                        <div class="small text-muted">{{ app.drive_title }}</div>
                      </div>
                    </td>
                    <td class="text-dark small">{{ app.date }}</td>
                    <td class="text-center">
                      <span :class="getStatusBadge(app.status)" class="badge-pill">
                        {{ app.status }}
                      </span>
                    </td>
                    <td class="text-center">
                      <button v-if="app.status === 'Selected'" @click="downloadOffer(app)" class="btn btn-sm btn-success rounded-pill px-3">
                        📥 Offer Letter
                      </button>
                      <span v-else class="text-muted small">-</span>
                    </td>
                  </tr>
                  <tr v-if="history.length === 0">
                    <td colspan="4" class="text-center py-5">No applications yet.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="modal-footer-custom">
            <button class="btn btn-dark rounded-pill px-4" @click="showStatusModal = false">Close</button>
          </div>
        </div>
      </div>
    </transition>  
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();


const drives = ref([]);          
const history = ref([]);         
const searchQuery = ref('');     
const showStatusModal = ref(false); 
const profile = ref({ name: '', roll: '', dept: '', cgpa: '', resume: null });


const showReminders = ref(true); 

const handleSearch = async () => {
  const token = localStorage.getItem('auth_token');
  if (!searchQuery.value.trim()) {
    fetchAllDrives();
    return;
  }
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/student/search?q=${searchQuery.value}`, {
      headers: { 'Authentication-Token': token }
    });
    if (res.ok) {
      drives.value = await res.json();
    }
  } catch (error) {
    console.error("Search failed:", error);
  }
};

const clearSearch = () => {
  searchQuery.value = '';
  fetchAllDrives();
};

const fetchData = async () => {
  const token = localStorage.getItem('auth_token');
  if (!token) { router.push('/login'); return; }

  try {
    const res = await fetch('http://127.0.0.1:5000/api/student/profile', {
      headers: { 'Authentication-Token': token }
    });
    if (res.ok) {
      const data = await res.json();
      profile.value = data.profile;
      history.value = data.applications; 
    }

  
    await fetchAllDrives();


    if (upcomingDeadlines.value.length > 0) {
      showReminders.value = true;
      setTimeout(() => {
        showReminders.value = false;
      }, 10000); 
    }

  } catch (error) { 
    console.error("Data fetch error:", error); 
  }
};

const getApplicationStatus = (driveId) => {
  const found = history.value.find(app => app.drive_id === driveId);
  return found ? found.status : 'Applied';
};

const fetchAllDrives = async () => {
  const token = localStorage.getItem('auth_token');
  const dRes = await fetch('http://127.0.0.1:5000/api/all-drives', {
    headers: { 'Authentication-Token': token }
  });
  if (dRes.ok) {
    drives.value = await dRes.json();
  }
};

const showDetailModal = ref(false);
const selectedDrive = ref({});

const viewJobDetails = (drive) => {
  selectedDrive.value = drive;
  showDetailModal.value = true;
};

const apply = async (id) => {
  const token = localStorage.getItem('auth_token');
  const res = await fetch(`http://127.0.0.1:5000/api/apply/${id}`, {
    method: 'POST',
    headers: { 'Authentication-Token': token }
  });
  const data = await res.json();
  alert(data.message);
  fetchData(); 
};

const isApplied = (driveId) => {
  return history.value.some(app => app.drive_id === driveId);
};

const upcomingDeadlines = computed(() => {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const tomorrowStr = tomorrow.toISOString().split('T')[0];
  return drives.value.filter(drive => drive.deadline_date && drive.deadline_date.includes(tomorrowStr));
});

const getStatusBadge = (status) => {
  if (status === 'Selected') return 'badge bg-success px-3 rounded-pill';
  if (status === 'Rejected') return 'badge bg-danger px-3 rounded-pill';
  if (status === 'Shortlisted') return 'badge bg-info px-3 rounded-pill';
  return 'badge bg-warning text-dark px-3 rounded-pill';
};

const exportMyHistory = async () => {
  const token = localStorage.getItem('auth_token');
  const res = await fetch('http://127.0.0.1:5000/api/test-export', { 
    headers: { 'Authentication-Token': token } 
  });
  const data = await res.json();
  alert(data.message);
};

const logout = () => { 
  localStorage.clear(); 
  router.push('/login'); 
};

onMounted(fetchData);
</script>

<style scoped>
.dashboard-wrapper {
  background: radial-gradient(circle, #4d4d4d 0%, #1a1a1a 100%);
  min-height: 100vh;
  width: 100%;
}
.sub-header { background-color: #0d6efd !important; }
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex; align-items: center; justify-content: center;
  z-index: 1050;
}
.profile-details p { margin-bottom: 12px; font-size: 0.95rem; }
.profile-details strong { display: inline-block; width: 80px; color: #444; }
.badge { font-size: 0.8rem; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-card {
  background: white;
  width: 100%;
  max-width: 800px;
  border-radius: 20px;
  overflow: hidden;
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-header-custom {
  padding: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
}

.icon-circle {
  width: 45px; height: 45px;
  background: #eef4ff;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem;
}

.btn-close-custom {
  background: none; border: none; font-size: 2rem;
  color: #ccc; line-height: 1; cursor: pointer;
  transition: color 0.2s;
}
.btn-close-custom:hover { color: #333; }

.modal-body-custom {
  max-height: 60vh;
  overflow-y: auto;
  padding: 10px;
}

.status-row {
  border-bottom: 1px solid #f9f9f9;
  transition: background 0.2s;
}
.status-row:hover { background-color: #fcfcfc; }

.avatar-sm { width: 40px; height: 40px; font-size: 1.1rem; }


.badge-pill {
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  display: inline-block;
  min-width: 100px;
}

.bg-success { background-color: #d1fae5 !important; color: #065f46 !important; }
.bg-danger { background-color: #fee2e2 !important; color: #991b1b !important; }
.bg-info { background-color: #e0f2fe !important; color: #075985 !important; }
.bg-warning { background-color: #fef3c7 !important; color: #92400e !important; }

.modal-footer-custom {
  padding: 20px;
  border-top: 1px solid #f0f0f0;
  text-align: right;
}
</style>