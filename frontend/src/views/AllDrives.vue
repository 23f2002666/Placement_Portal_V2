<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Search Placement Drives</h2>
      <div class="d-flex w-50">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="form-control me-2" 
          placeholder="Search by title or company..."
        >
        <button @click="filterDrives" class="btn btn-primary">Search</button>
      </div>
    </div>

    <div v-if="filteredDrives.length === 0" class="text-center py-5">
      <p class="text-muted">No drives found matching your search.</p>
    </div>

    <div class="row">
      <div v-for="drive in filteredDrives" :key="drive.id" class="col-md-6 mb-3">
        <div class="card h-100 shadow-sm border-start border-primary border-4">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <h5 class="card-title">{{ drive.title }}</h5>
              <span class="badge bg-info text-dark">{{ drive.package_details || 'N/A' }}</span>
            </div>
            <h6 class="card-subtitle mb-2 text-muted">{{ drive.company }}</h6>
            <p class="card-text text-truncate">{{ drive.description }}</p>
            <div class="d-flex justify-content-between align-items-center">
              <small class="text-danger fw-bold">Deadline: {{ drive.deadline }}</small>
              <router-link :to="`/student`" class="btn btn-sm btn-outline-primary">View & Apply</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const allDrives = ref([]);
const filteredDrives = ref([]);
const searchQuery = ref('');
const token = localStorage.getItem('auth_token');

const fetchDrives = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/drives', {
      headers: { 'Authentication-Token': token }
    });
    const data = await res.json();
    allDrives.value = data;
    filteredDrives.value = data;
  } catch (e) {
    console.error("Fetch error", e);
  }
};

const filterDrives = () => {
  const query = searchQuery.value.toLowerCase();
  filteredDrives.value = allDrives.value.filter(d => 
    d.title.toLowerCase().includes(query) || 
    d.company.toLowerCase().includes(query)
  );
};

onMounted(fetchDrives);
</script>