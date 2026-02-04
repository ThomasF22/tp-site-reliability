<template>
  <div id="app">
    <!-- Navbar -->
    <NavBar />
    
    <!-- Contenu principal -->
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>

<style>
/* Styles globaux */
body {
  background-color: #f8f9fa;
}

.navbar-brand {
  font-weight: bold;
  color: #1da1f2 !important;
}

.btn-primary {
  background-color: #1da1f2;
  border-color: #1da1f2;
}

.btn-primary:hover {
  background-color: #0d8bd9;
  border-color: #0d8bd9;
}

.card {
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-card {
  margin-bottom: 1rem;
  transition: transform 0.2s ease-in-out;
}

.post-card:hover {
  transform: translateY(-2px);
}

.text-muted {
  color: #657786 !important;
}

.like-btn {
  border: none;
  background: none;
  color: #657786;
  transition: color 0.2s ease;
}

.like-btn:hover {
  color: #e1306c;
}

.like-btn.liked {
  color: #e1306c;
}
</style>