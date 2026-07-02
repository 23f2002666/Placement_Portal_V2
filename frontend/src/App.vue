<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <div class="container">
    <nav class="navbar bg-body-tertiary">
  <div class="container-fluid">
    <RouterLink to="/" class="navbar-brand">
      Placement
    </RouterLink>

    <form class="d-flex" role="search">
      <input
        class="form-control me-2"
        type="search"
        placeholder="Search"
      />
      <button class="btn btn-outline-success" type="submit">
        Search
      </button>
    </form>

    <RouterLink to="/login" class="btn btn-primary ms-3">
      Login
    </RouterLink>
  </div>
</nav>

    

  <RouterView/>
  </div>

  

</template>

