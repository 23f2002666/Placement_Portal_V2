<template>
  <div class="dashboard-wrapper">

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 border-bottom border-secondary">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold fs-4">Placement Portal</span>
        <div class="ms-auto">
          <button @click="logout" class="btn btn-danger btn-sm px-3 rounded-pill">Logout</button>
        </div>
      </div>
    </nav>

    <div class="sub-header bg-primary text-white py-2 px-4 shadow-sm">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <span class="fs-6 fw-semibold">🏢 Company Dashboard</span>
        <div class="d-flex align-items-center gap-4">
          <div @click="openPostModal" class="nav-action-item"><span class="fs-5">+</span> Post Drive</div>
          <div @click="openProfileModal" class="nav-action-item">
            <i class="bi bi-gear"></i> Edit Profile
          </div>
        </div>
      </div>
    </div>

    <div class="container-fluid px-5 py-4">
      <div class="row g-4">
        <div class="col-lg-4 col-md-5">
          <div class="card profile-card border-0 shadow-lg rounded-3 h-100">
            <div class="card-header bg-dark text-white text-center py-2 fw-semibold">
              🏢 Company Profile
            </div>
            <div class="card-body p-4 bg-white text-dark">
              <div class="profile-info">
                <p><strong>Name:</strong> {{ profile.company_name }}</p>
                <p><strong>Email:</strong> {{ profile.email }}</p>
                <p><strong>HR Name:</strong> {{ profile.hr_name}}</p>
                <p><strong>Mobile No:</strong> {{ profile.mobile || 'N/A' }}</p>
                <p><strong>Address:</strong> {{ profile.address || 'N/A' }}</p>
                <p><strong>Status:</strong> <span class="badge bg-success rounded-pill">Approved</span></p>
              </div>
              <button @click="openProfileModal" class="btn btn-outline-primary w-100 btn-sm mt-3 rounded-pill">
                Edit Profile
              </button>
            </div>
          </div>
        </div>

        <div class="col-lg-8 col-md-7">
          <div class="row g-4 h-100">
            <div class="col-md-6">
              <div class="card stat-card bg-primary text-white border-0 shadow rounded-3">
                <div class="card-body p-4">
                  <h5 class="fw-bold mb-3">Jobs Posted</h5>
                  <h1 class="display-3 fw-bold">{{ myDrives.length }}</h1>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card stat-card bg-warning text-dark border-0 shadow rounded-3">
                <div class="card-body p-4">
                  <h5 class="fw-bold mb-3 text-uppercase small">Active Portals</h5>
                  <h1 class="display-3 fw-bold">{{ activeDrivesCount }}</h1>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mt-5">
        <div class="col-12 text-center text-white mb-3"><h3>My Posted Jobs</h3></div>
        <div class="col-12">
          <div class="card border-0 shadow-lg overflow-hidden rounded-3">
            <table class="table table-hover mb-0 align-middle text-center">
              <thead class="table-dark">
                <tr>
                  <th class="ps-4 text-start">Job Title</th><th>Deadline</th><th>Status</th><th>Applicants</th><th>Action</th>
                </tr>
              </thead>
              <tbody class="bg-white text-dark">
                <tr v-for="drive in myDrives" :key="drive.id">
                  <td class="ps-4 fw-bold text-start">{{ drive.title }}</td>
                  <td>{{ drive.deadline_date }}</td>
                  <td>
                    <span :class="drive.status === 'Closed' ? 'badge bg-danger' : 'badge bg-success'">
                      {{ drive.status }}
                    </span>
                  </td>
                  <td>
                    <button @click="viewApplicants(drive.id)" class="btn btn-info btn-sm text-white px-3">
                      View Applicants ({{ drive.applicant_count || 0 }})
                    </button>
                  </td>
                  <td>
                    <div class="btn-group gap-1">
                      <button v-if="drive.status !== 'Closed'" @click="toggleStatus(drive, 'Closed')" class="btn btn-secondary btn-sm">Close</button>
                      <button v-else @click="toggleStatus(drive, 'Approved')" class="btn btn-success btn-sm">Open</button>
                      <button @click="openEditModal(drive)" class="btn btn-warning btn-sm text-white">Edit</button>
                      <button @click="deleteDrive(drive.id)" class="btn btn-danger btn-sm">Delete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.7);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content text-dark border-0">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">{{ isEditing ? 'Edit Drive' : 'Post New Drive' }}</h5>
            <button type="button" class="btn-close btn-close-white" @click="showModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <div class="mb-3">
                <label class="form-label small fw-bold">Job Title</label>
                <input v-model="currentDrive.title" class="form-control" placeholder="Job Title">
            </div>
            <div class="mb-3">
                <label class="form-label small fw-bold">Description</label>
                <textarea v-model="currentDrive.description" class="form-control" rows="3"></textarea>
            </div>
            <div class="row">
              <div class="col-6">
                <label class="form-label small fw-bold">Min CGPA</label>
                <input v-model="currentDrive.min_cgpa_required" type="number" step="0.1" class="form-control">
              </div>
              <div class="col-6">
                <label class="form-label small fw-bold">Package</label>
                <input v-model="currentDrive.package_details" class="form-control" placeholder="e.g. 12 LPA">
              </div>
            </div>
            <div class="mt-3">
                <label class="form-label small fw-bold">Deadline</label>
                <input v-model="currentDrive.deadline_date" type="date" class="form-control">
            </div>
            <button @click="saveDrive" class="btn btn-primary w-100 fw-bold mt-4">{{ isEditing ? 'Update' : 'Post' }} Drive</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showApplicantModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.7); z-index: 1050;">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content text-dark border-0">
          <div class="modal-header bg-info text-white">
            <h5 class="modal-title">Applicants List</h5>
            <button type="button" class="btn-close" @click="showApplicantModal = false"></button>
          </div>
          <div class="modal-body p-0">
            <table class="table table-striped mb-0 align-middle">
              <thead class="table-light">
                <tr>
                  <th class="ps-3">Student</th>
                  <th>CGPA</th>
                  <th class="text-center">Full Profile</th>
                  <th class="text-center">Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in applicants" :key="app.application_id">
                  <td class="ps-3">
                    <div class="fw-bold">{{ app.student_name }}</div>
                    <small class="text-muted">{{ app.email }}</small>
                  </td>
                  <td>{{ app.cgpa }}</td>
                  <td class="text-center">
                    <button @click="viewStudentProfile(app)" class="btn btn-outline-primary btn-sm rounded-pill">
                      👁️ Details
                    </button>
                  </td>
                  <td class="text-center">
                    <span :class="getStatusBadge(app.status)">{{ app.status }}</span>
                  </td>
                  <td>
                    <select @change="updateAppStatus(app.application_id, $event.target.value)" class="form-select form-select-sm">
                      <option value="" disabled selected>Change Status</option>
                      <option value="Shortlisted">Shortlist</option>
                      <option value="Selected">Select</option>
                      <option value="Rejected">Reject</option>
                    </select>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="applicants.length === 0" class="p-4 text-center text-muted">No applicants yet.</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showProfileModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.7);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content text-dark border-0">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Edit Company Profile</h5>
            <button type="button" class="btn-close btn-close-white" @click="showProfileModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <div class="mb-3">
              <label class="form-label small fw-bold">Company Name</label>
              <input v-model="editProfileData.company_name" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">HR Name</label>
              <input v-model="editProfileData.hr_name" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Mobile Number</label>
              <input v-model="editProfileData.mobile" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Address / Description</label>
              <textarea v-model="editProfileData.address" class="form-control" rows="3"></textarea>
            </div>
            <button @click="updateProfile" class="btn btn-primary w-100 fw-bold mt-3">Save Changes</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showStudentDetailModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.8); z-index: 1100;">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content text-dark border-0 rounded-4">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">Student Full Profile</h5>
            <button type="button" class="btn-close btn-close-white" @click="showStudentDetailModal = false"></button>
          </div>
          <div class="modal-body p-4 text-center">
            <div class="avatar-circle mx-auto bg-light text-primary mb-2">
              {{ selectedStudent.student_name ? selectedStudent.student_name.charAt(0).toUpperCase() : 'S' }}
            </div>
            <h4 class="fw-bold mb-0">{{ selectedStudent.student_name }}</h4>
            <p class="text-primary">{{ selectedStudent.email }}</p>

            <div class="row g-3 mt-3 text-start">
              <div class="col-6 border-end">
                <label class="small text-muted fw-bold text-uppercase">Roll Number</label>
                <p class="mb-0">{{ selectedStudent.roll_number || 'N/A' }}</p>
              </div>
              <div class="col-6">
                <label class="small text-muted fw-bold text-uppercase">Branch</label>
                <p class="mb-0">{{ selectedStudent.branch || 'N/A' }}</p>
              </div>
              <div class="col-6 border-end">
                <label class="small text-muted fw-bold text-uppercase">Current CGPA</label>
                <p class="mb-0 fw-bold text-success">{{ selectedStudent.cgpa }}</p>
              </div>
              <div class="col-12">
                <label class="small text-muted fw-bold text-uppercase">Skills</label>
                <p class="mb-0 p-2 bg-light rounded text-dark">{{ selectedStudent.skills || 'No skills listed' }}</p>
              </div>
            </div>
          </div>
          <div class="modal-footer border-0">
            <button @click="showStudentDetailModal = false" class="btn btn-secondary w-100 rounded-pill">Close Profile</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = localStorage.getItem('auth_token');
const myDrives = ref([]);
const profile = ref({ company_name: '', hr_name: '', email: '', mobile: '', address: '' });
const applicants = ref([]);


const showModal = ref(false);          
const showApplicantModal = ref(false); 
const showProfileModal = ref(false);   
const showStudentDetailModal = ref(false); 

const isEditing = ref(false);
const currentDrive = ref({ title: '', description: '', min_cgpa_required: 0, package_details: '', deadline_date: '' });
const editProfileData = ref({});
const selectedStudent = ref({}); 


const activeDrivesCount = computed(() => {
  return myDrives.value.filter(d => d.status === 'Approved').length;
});

const fetchData = async () => {
  if (!token) { router.push('/login'); return; }
  try {
    const profRes = await fetch('http://127.0.0.1:5000/api/company/profile', { 
        headers: { 'Authentication-Token': token } 
    });
    if (profRes.ok) profile.value = await profRes.json();
    const res = await fetch('http://127.0.0.1:5000/api/drives', { 
        headers: { 'Authentication-Token': token } 
    });
    if (res.ok) myDrives.value = await res.json();
  } catch (err) { console.error(err); }
};

const viewApplicants = async (id) => {
  const res = await fetch(`http://127.0.0.1:5000/api/company/applications/${id}`, { 
      headers: { 'Authentication-Token': token } 
  });
  
  if (res.ok) {
    const data = await res.json();
    applicants.value = data.map(app => ({
        application_id: app.application_id,
        status: app.status,
        student_name: app.student_info.name,
        email: app.student_info.email,
        roll_number: app.student_info.roll,
        branch: app.student_info.branch,
        cgpa: app.student_info.cgpa,
        skills: app.student_info.skills
    }));
    showApplicantModal.value = true;
  } else {
    alert("Could not load applicants.");
  }
};

const viewStudentProfile = (appData) => {
  selectedStudent.value = appData;
  showStudentDetailModal.value = true;
};

const openStudentDetail = (appData) => {
  selectedStudent.value = appData;
  showStudentDetailModal.value = true;
};

const updateAppStatus = async (appId, status) => {
  const res = await fetch(`http://127.0.0.1:5000/api/company/application/update/${appId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', 'Authentication-Token': token },
    body: JSON.stringify({ status })
  });
  if (res.ok) {
      alert("Status Updated!");
  }
};

const getStatusBadge = (status) => {
  if (status === 'Selected') return 'badge bg-success';
  if (status === 'Shortlisted') return 'badge bg-info';
  if (status === 'Rejected') return 'badge bg-danger';
  return 'badge bg-secondary';
};


const saveDrive = async () => {
  const method = isEditing.value ? 'PUT' : 'POST';
  const url = isEditing.value ? `http://127.0.0.1:5000/api/drives?id=${currentDrive.value.id}` : `http://127.0.0.1:5000/api/drives`;
  
  const res = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json', 'Authentication-Token': token },
    body: JSON.stringify(currentDrive.value)
  });

  if (res.ok) {
    showModal.value = false;
    fetchData();
  } else {
    const errorData = await res.json();
    alert("Error: " + (errorData.message || "Could not save"));
  }
};

const toggleStatus = async (drive, newStatus) => {
  await fetch(`http://127.0.0.1:5000/api/drives?id=${drive.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', 'Authentication-Token': token },
    body: JSON.stringify({ ...drive, status: newStatus })
  });
  fetchData();
};

const deleteDrive = async (id) => {
  if (confirm("Delete this drive?")) {
    await fetch(`http://127.0.0.1:5000/api/drives?id=${id}`, {
      method: 'DELETE',
      headers: { 'Authentication-Token': token }
    });
    fetchData();
  }
};

const openProfileModal = () => {
  editProfileData.value = { ...profile.value };
  showProfileModal.value = true;
};

const updateProfile = async () => {
  const res = await fetch('http://127.0.0.1:5000/api/company/profile', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', 'Authentication-Token': token },
    body: JSON.stringify(editProfileData.value)
  });
  if (res.ok) {
    alert("Profile Updated!");
    showProfileModal.value = false;
    fetchData();
  }
};

const openPostModal = () => { 
  isEditing.value = false; 
  currentDrive.value = { title: '', description: '', min_cgpa_required: 0, package_details: '', deadline_date: '' }; 
  showModal.value = true; 
};

const openEditModal = (drive) => { 
  isEditing.value = true; 
  currentDrive.value = { ...drive }; 
  showModal.value = true; 
};

const logout = () => { localStorage.clear(); router.push('/login'); };

onMounted(fetchData);
</script>


<style scoped>
.dashboard-wrapper {
  background: radial-gradient(circle, #4d4d4d 0%, #1a1a1a 100%);
  min-height: 100vh;
  width: 100%;
  color: white;
}
.sub-header { background-color: #0d6efd !important; }
.nav-action-item { cursor: pointer; transition: opacity 0.2s; }
.nav-action-item:hover { opacity: 0.8; }
.profile-card strong { display: inline-block; width: 100px; color: #555; }
.stat-card { min-height: 160px; }
.badge { font-size: 0.75rem; }


.avatar-circle {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  border: 3px solid #0d6efd;
}
.modal-content {
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
</style>