<template>
  <div class="admin-wrapper">

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 border-bottom border-secondary shadow sticky-top">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold fs-4">Admin Console</span>
        <div class="ms-auto d-flex align-items-center gap-3">
          <div class="input-group input-group-sm" style="width: 380px;">
            <input 
              type="text" 
              v-model="searchQuery" 
              @keyup.enter="handleSearch"
              class="form-control" 
              :placeholder="'Search ' + tabTitle + '...'"
            >
            <button @click="handleSearch" class="btn btn-primary px-3" type="button">Search</button>
            <button v-if="searchQuery" @click="clearSearch" class="btn btn-outline-light" type="button">✕</button>
          </div>
          <button @click="openReport" class="btn btn-info btn-sm px-3 fw-bold me-2">📊 Weekly Report</button>
          <button @click="logout" class="btn btn-danger btn-sm px-3 fw-bold ms-2">Logout</button>
        </div>
      </div>
    </nav>

    <div class="container py-4">
      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="card stat-card bg-primary text-white border-0 shadow-sm h-100 p-3">
            <div class="d-flex justify-content-between">
              <h5 class="fw-normal">Total Drives</h5>
              <span class="fs-3">📢</span>
            </div>
            <h1 class="display-4 fw-bold">{{ stats.total_drives }}</h1>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card stat-card bg-success text-white border-0 shadow-sm h-100 p-3">
            <div class="d-flex justify-content-between">
              <h5 class="fw-normal">Students</h5>
              <span class="fs-3">👨‍🎓</span>
            </div>
            <h1 class="display-4 fw-bold">{{ stats.total_students }}</h1>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card stat-card bg-warning text-dark border-0 shadow-sm h-100 p-3">
            <div class="d-flex justify-content-between">
              <h5 class="fw-normal">Companies</h5>
              <span class="fs-3">🏢</span>
            </div>
            <h1 class="display-4 fw-bold">{{ stats.total_companies }}</h1>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-lg rounded-4 overflow-hidden mb-5">
        <div class="bg-white border-bottom px-2 pt-2">
          <ul class="nav nav-tabs border-0 custom-tabs">
            <li class="nav-item" v-for="tab in tabs" :key="tab.id">
              <button 
                class="nav-link border-0" 
                :class="{ active: currentTab === tab.id }" 
                @click="changeTab(tab.id)"
              >
                {{ tab.icon }} {{ tab.label }}
              </button>
            </li>
          </ul>
        </div>

        <div class="card-body bg-white p-4">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="fw-bold m-0">{{ tabTitle }} Management</h4>
            <span v-if="searchQuery" class="badge bg-info p-2">Results for: "{{ searchQuery }}"</span>
          </div>
          
          <div class="table-responsive">
            <table class="table align-middle table-hover">
              <thead class="table-light">
                <tr v-if="['pending', 'approved'].includes(currentTab)">
                  <th>#</th><th>Company Name</th><th>Email</th><th class="text-center">Drives</th> <th class="text-center">Selected</th> <th>Status</th><th class="text-end">Actions</th>
                </tr>
                <tr v-else-if="currentTab === 'students'">
                  <th>#</th><th>Full Name</th><th>Roll Number</th><th>Email</th><th>Status</th><th class="text-end">Actions</th>
                </tr>
                <tr v-else>
                  <th>#</th><th>Company</th><th>Job Title</th><th>Deadline</th><th>Status</th><th class="text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in filteredData" :key="item.id">
                  <td>{{ index + 1 }}</td>
                  
                  <!-- COMPANY VIEW -->
                  <template v-if="['pending', 'approved'].includes(currentTab)">
                    <td class="fw-bold">{{ item.name || item.company_name }}</td>
                    <td>{{ item.email }}</td>
                      <td class="text-center">
                          <span class="badge bg-secondary rounded-pill">{{ item.drive_count || 0 }}</span>
                      </td>
                      <td class="text-center text-success fw-bold">
                              {{ item.selected_count || 0 }}
                      </td>
                    <td><span :class="getStatusBadge(item.status)">{{ item.status }}</span></td>
                    <td class="text-end">
                      <button v-if="item.status === 'Pending'" @click="updateCompanyStatus(item.id, 'Approved')" class="btn btn-success btn-sm me-1">Approve</button>
                      <button v-if="item.status === 'Pending'" @click="updateCompanyStatus(item.id, 'Rejected')" class="btn btn-danger btn-sm">Reject</button>
                      <button v-if="item.status === 'Approved'" @click="updateCompanyStatus(item.id, 'Rejected')" class="btn btn-dark btn-sm me-1">Blacklist</button>
                      <button v-if="item.status === 'Rejected'" @click="updateCompanyStatus(item.id, 'Approved')" class="btn btn-info btn-sm me-1">Whitelist</button>
                      <button @click="deleteEntity('company', item.id)" class="btn btn-outline-danger btn-sm ms-1">Delete</button>
                    </td>
                  </template>

                  <template v-else-if="currentTab === 'students'">
                    <td class="fw-bold">{{ item.name || item.full_name }}</td>
                    <td>{{ item.roll || item.roll_number }}</td>
                    <td>{{ item.email }}</td>
                    <td>
                      <span :class="(item.status === 'Active' || item.is_active) ? 'badge bg-success' : 'badge bg-danger'">
                        {{ (item.status === 'Active' || item.is_active) ? 'Active' : 'Blacklisted' }}
                      </span>
                    </td>
                    <td class="text-end">
                      <button @click="toggleStudentStatus(item.id)" class="btn btn-sm" :class="(item.status === 'Active' || item.is_active) ? 'btn-dark' : 'btn-success'">
                        {{ (item.status === 'Active' || item.is_active) ? 'Blacklist' : 'Approve' }}
                      </button>
                      <button @click="deleteEntity('student', item.id)" class="btn btn-outline-danger btn-sm ms-1">Delete</button>
                    </td>
                  </template>

                  <template v-else>
                    <td>{{ item.company || item.company_name }}</td>
                    <td class="fw-bold">{{ item.title }}</td>
                    <td>{{ item.deadline || item.deadline_date }}</td>
                    <td><span :class="getStatusBadge(item.status)">{{ item.status }}</span></td>
                    <td class="text-end">
                      <button v-if="item.status === 'Pending'" @click="updateDriveStatus(item.id)" class="btn btn-success btn-sm">Approve</button>
                      <button @click="deleteEntity('drive', item.id)" class="btn btn-outline-danger btn-sm ms-1">Delete</button>
                    </td>
                  </template>
                </tr>

                <tr v-if="filteredData.length === 0">
                  <td colspan="6" class="text-center py-5 text-muted">No records found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

<transition name="fade">
  <div v-if="showReport" class="report-overlay">
    <div class="report-container shadow-lg">
      <div class="report-header bg-dark text-white p-4 d-flex justify-content-between align-items-center">
        <h2 class="m-0">Placement Portal - Weekly Summary Report</h2>
        <button @click="showReport = false" class="btn btn-outline-light">Close Report</button>
      </div>

      <div class="report-content p-5">
        <section class="mb-5">
          <h3 class="border-bottom pb-2 text-primary">Part 1: Student Placement Tracking</h3>
          <table class="table table-striped table-hover mt-3">
            <thead class="table-primary">
              <tr>
                <th>Full Name</th><th>Roll Number</th><th>Dept</th><th>CGPA</th><th>Selected At</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in report.students" :key="s.roll">
                <td>{{ s.name }}</td>
                <td>{{ s.roll }}</td>
                <td>{{ s.dept }}</td>
                <td>{{ s.cgpa }}</td>
                <td :class="s.placed_at !== 'Pending' ? 'fw-bold text-success' : 'text-muted'">
                  {{ s.placed_at }}
                </td>
              </tr>
            </tbody>
          </table>
        </section>

        <section>
          <h3 class="border-bottom pb-2 text-primary">Part 2: Recruiter Performance Breakdown</h3>
          <div class="row mt-4">
            <div v-for="c in report.companies" :key="c.company_name" class="col-md-6 mb-4">
              <div class="card h-100 border-secondary">
                <div class="card-header bg-light fw-bold fs-5">{{ c.company_name }}</div>
                <div class="card-body">
                  <p><strong>Total Drives Conducted:</strong> {{ c.total_drives }}</p>
                  <p class="mb-1 text-muted small">Job Post Wise Selections:</p>
                  <ul class="list-group list-group-flush mb-3">
                    <li v-for="post in c.drive_breakdown" :key="post.job_title" class="list-group-item d-flex justify-content-between align-items-center py-1 small">
                      {{ post.job_title }}
                      <span class="badge bg-primary rounded-pill">{{ post.hired }}</span>
                    </li>
                  </ul>
                  <div class="d-flex justify-content-between align-items-center border-top pt-2">
                    <span class="fw-bold">Total Students Hired:</span>
                    <span class="fs-4 fw-bold text-success">{{ c.total_hired }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</transition>


</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = localStorage.getItem('auth_token');
const showReport = ref(false);
const report = ref({ students: [], companies: [] });

const openReport = async () => {
  const res = await fetch('http://127.0.0.1:5000/api/admin/analytics-report', {
    headers: { 'Authentication-Token': token }
  });
  if (res.ok) {
    report.value = await res.json();
    showReport.value = true;
  }
};
const stats = ref({ total_students: 0, total_companies: 0, total_drives: 0 });
const companies = ref([]);
const students = ref([]);
const drives = ref([]);
const currentTab = ref('pending');
const searchQuery = ref('');

const tabs = [
  { id: 'pending', label: 'Pending Companies', icon: '🔔' },
  { id: 'approved', label: 'Partner Companies', icon: '✅' },
  { id: 'pending_drivers', label: 'Review Drives', icon: '📢' },
  { id: 'all_drives', label: 'All Job Posts', icon: '🏢' },
  { id: 'students', label: 'Student Management', icon: '👨‍🎓' },
];

const handleSearch = async () => {
  if (!searchQuery.value.trim()) { fetchData(); return; }
  let type = 'company';
  if (currentTab.value === 'students') type = 'student';
  else if (['pending_drivers', 'all_drives'].includes(currentTab.value)) type = 'drive';
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/admin/search?type=${type}&q=${searchQuery.value}`, {
      headers: { 'Authentication-Token': token }
    });
    if (res.ok) {
      const results = await res.json();
      if (type === 'student') students.value = results;
      else if (type === 'company') companies.value = results;
      else if (type === 'drive') drives.value = results;
    }
  } catch (err) { console.error("Search failed:", err); }
};

const clearSearch = () => { searchQuery.value = ''; fetchData(); };

const changeTab = (tabId) => {
  currentTab.value = tabId;
  if (searchQuery.value) handleSearch(); 
};

const fetchData = async () => {
  if (!token) { router.push('/login'); return; }
  const headers = { 'Authentication-Token': token };
  
  try {
    const [sRes, cRes, dRes, stRes] = await Promise.all([
      fetch('http://127.0.0.1:5000/api/admin/stats', { headers }),
      fetch('http://127.0.0.1:5000/api/admin/companies', { headers }),
      fetch('http://127.0.0.1:5000/api/admin/drives', { headers }),
      fetch('http://127.0.0.1:5000/api/admin/students', { headers })
    ]);

    if (sRes.ok) stats.value = await sRes.json();
    if (cRes.ok) companies.value = await cRes.json();
    if (stRes.ok) students.value = await stRes.json();
    if (dRes.ok) drives.value = await dRes.json();
  } catch (err) { console.error("Refresh failed:", err); }
};

const updateCompanyStatus = async (id, status) => {
  await fetch(`http://127.0.0.1:5000/api/admin/company/${id}`, {
    method: 'PUT',
    headers: { 'Authentication-Token': token, 'Content-Type': 'application/json' },
    body: JSON.stringify({ status })
  });
  fetchData();
};

const toggleStudentStatus = async (id) => {
  await fetch(`http://127.0.0.1:5000/api/admin/student/${id}`, {
    method: 'PUT',
    headers: { 'Authentication-Token': token }
  });
  fetchData();
};

const updateDriveStatus = async (id) => {
  await fetch(`http://127.0.0.1:5000/api/admin/drive/${id}`, {
    method: 'PUT',
    headers: { 'Authentication-Token': token }
  });
  fetchData();
};

const deleteEntity = async (type, id) => {
  if (!confirm(`Delete this ${type} permanently?`)) return;
  await fetch(`http://127.0.0.1:5000/api/admin/${type}/${id}`, {
    method: 'DELETE',
    headers: { 'Authentication-Token': token }
  });
  fetchData();
};

const filteredData = computed(() => {
  if (currentTab.value === 'pending') return companies.value.filter(c => c.status === 'Pending');
  if (currentTab.value === 'approved') return companies.value.filter(c => c.status !== 'Pending');
  if (currentTab.value === 'students') return students.value;
  if (currentTab.value === 'pending_drivers') return drives.value.filter(d => d.status === 'Pending');
  return drives.value;
});

const tabTitle = computed(() => tabs.find(t => t.id === currentTab.value).label);

const getStatusBadge = (s) => {
  if (s === 'Approved' || s === 'Active') return 'badge bg-success';
  if (s === 'Pending') return 'badge bg-warning text-dark';
  return 'badge bg-danger';
};

const logout = () => { localStorage.clear(); router.push('/login'); };

onMounted(fetchData);
</script>

<style scoped>
.admin-wrapper { background: #f0f2f5; min-height: 100vh; }
.nav-tabs .nav-link { color: #555; border: none; padding: 15px 25px; transition: 0.3s; }
.nav-tabs .nav-link.active { color: #0d6efd; border-bottom: 3px solid #0d6efd !important; background: none; }
.stat-card { border-radius: 12px; transition: 0.3s; }
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }

.report-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.8);
  z-index: 3000;
  display: flex; justify-content: center; align-items: center;
}
.report-container {
  width: 95%; height: 90%;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  display: flex; flex-direction: column;
}
.report-content {
  flex-grow: 1;
  overflow-y: auto;
}
.text-primary { color: #0d6efd !important; }
.card-header { border-bottom: 2px solid #0d6efd; }

</style>