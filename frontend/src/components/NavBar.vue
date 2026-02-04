<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
    <div class="container">
      <!-- Logo/Brand -->
      <router-link class="navbar-brand" to="/">
        <i class="bi bi-twitter"></i>
        Forum
      </router-link>

      <!-- Toggle button pour mobile -->
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation items -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">
              <i class="bi bi-house"></i>
              Accueil
            </router-link>
          </li>
        </ul>

        <!-- User menu -->
        <ul class="navbar-nav">
          <li v-if="!isLoggedIn" class="nav-item">
            <router-link class="nav-link" to="/login">
              <i class="bi bi-box-arrow-in-right"></i>
              Connexion
            </router-link>
          </li>
          <li v-if="!isLoggedIn" class="nav-item">
            <router-link class="nav-link" to="/register">
              <i class="bi bi-person-plus"></i>
              Inscription
            </router-link>
          </li>
          
          <!-- Menu utilisateur connecté -->
          <li v-if="isLoggedIn" class="nav-item dropdown">
            <a 
              class="nav-link dropdown-toggle" 
              href="#" 
              id="navbarDropdown" 
              role="button" 
              data-bs-toggle="dropdown"
            >
              <i class="bi bi-person-circle"></i>
              {{ currentUser?.display_name || currentUser?.username }}
            </a>
            <ul class="dropdown-menu">
              <li>
                <router-link 
                  class="dropdown-item" 
                  :to="`/profile/${currentUser?.username}`"
                >
                  <i class="bi bi-person"></i>
                  Mon profil
                </router-link>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <button class="dropdown-item" @click="handleLogout">
                  <i class="bi bi-box-arrow-right"></i>
                  Déconnexion
                </button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import api from '../services/api.js'

export default {
  name: 'NavBar',
  data() {
    return {
      currentUser: null
    }
  },
  computed: {
    isLoggedIn() {
      return this.currentUser !== null
    }
  },
  async created() {
    await this.checkAuthStatus()
  },
  methods: {
    async checkAuthStatus() {
      try {
        const userData = localStorage.getItem('user')
        if (userData) {
          this.currentUser = JSON.parse(userData)
          // Vérifier que la session est encore valide
          await api.getCurrentUser()
        }
      } catch (error) {
        console.log('Pas de session active')
        this.currentUser = null
        localStorage.removeItem('user')
      }
    },
    async handleLogout() {
      try {
        await api.logout()
        this.currentUser = null
        localStorage.removeItem('user')
        this.$router.push('/')
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error)
        // Même en cas d'erreur, on déconnecte côté client
        this.currentUser = null
        localStorage.removeItem('user')
        this.$router.push('/')
      }
    }
  },
  watch: {
    // Écouter les changements de route pour mettre à jour le statut auth
    '$route'() {
      this.checkAuthStatus()
    }
  }
}
</script>

<style scoped>
.navbar-brand {
  font-size: 1.5rem;
}

.navbar-brand i {
  margin-right: 0.5rem;
}

.nav-link i {
  margin-right: 0.25rem;
}

.dropdown-item i {
  margin-right: 0.5rem;
  width: 1rem;
}
</style>