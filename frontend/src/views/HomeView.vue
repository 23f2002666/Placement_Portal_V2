<template>
  <div class="landing-page bg-dark min-vh-100 text-white">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-secondary px-4">
      <div class="container-fluid">
        <a class="navbar-brand d-flex align-items-center" href="#">
          <span class="fw-bold text-white">Placement Portal</span>
        </a>
        <div class="ms-auto">
          <router-link to="/login" class="btn btn-outline-success btn-sm me-2 px-3">Login</router-link>
          <router-link to="/register" class="btn btn-success btn-sm px-3">Register</router-link>
        </div>
      </div>
    </nav>

    <div class="container py-5">
      <div class="row mb-4 justify-content-center">
        <div class="col-lg-10">
          <div class="card border-0 shadow-lg p-5 text-center rounded-4 bg-white">
            <div class="card-body py-5">
              <h1 class="display-4 fw-bold text-primary mb-3">Campus Recruitment Portal</h1>
              <p class="lead text-muted mx-auto mb-4" style="max-width: 700px;">
                Connecting brilliant minds with world-class opportunities. Manage placement drives, applications, and recruitment all in one place.
              </p>
              <div class="d-flex justify-content-center gap-3">
                <router-link to="/login" class="btn btn-primary btn-lg px-4 fw-bold">Login to Dashboard</router-link>
                <router-link to="/register" class="btn btn-outline-secondary btn-lg px-4">Create New Account</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row justify-content-center g-4">
        <div class="col-lg-5 col-md-6">
          <div class="card h-100 bg-dark text-white border-secondary p-4">
            <div class="card-body d-flex flex-column">
              <h3 class="fw-bold mb-3">For Students</h3>
              <p class="text-secondary mb-4">
                Build your professional profile, explore job openings from top companies, and track your applications in real-time.
              </p>
              <router-link to="/register" class="btn btn-outline-light mt-auto" style="width: fit-content;">Register as Student</router-link>
            </div>
          </div>
        </div>

        <div class="col-lg-5 col-md-6">
          <div class="card h-100 bg-white text-dark border-0 p-4">
            <div class="card-body d-flex flex-column">
              <h3 class="fw-bold mb-3">For Companies</h3>
              <p class="text-muted mb-4">
                Hire the best talent from our institute. Post placement drives, manage candidates, and streamline your recruitment process.
              </p>
              <router-link to="/register" class="btn btn-outline-primary mt-auto" style="width: fit-content;">Register as Company</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer class="text-center py-4 text-secondary border-top border-secondary mt-5">
      <small>© 2026 Placement Portal · Institute Recruitment Cell</small>
    </footer>
  </div>
</template>

<script setup>
</script>

<style scoped>
.landing-page {
  background: linear-gradient(180deg, #48494a 0%, #1a1d20 100%);
}
</style>