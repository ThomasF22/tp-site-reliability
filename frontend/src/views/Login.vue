<template>
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
      <div class="card">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">
            <i class="bi bi-box-arrow-in-right text-primary"></i>
            Connexion
          </h2>

          <!-- Formulaire de connexion -->
          <form @submit.prevent="handleLogin">
            <!-- Champ username -->
            <div class="mb-3">
              <label for="username" class="form-label">Nom d'utilisateur</label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="loginForm.username"
                :class="{ 'is-invalid': errors.username }"
                required
                autofocus
              >
              <div v-if="errors.username" class="invalid-feedback">
                {{ errors.username }}
              </div>
            </div>

            <!-- Champ password -->
            <div class="mb-3">
              <label for="password" class="form-label">Mot de passe</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="loginForm.password"
                :class="{ 'is-invalid': errors.password }"
                required
              >
              <div v-if="errors.password" class="invalid-feedback">
                {{ errors.password }}
              </div>
            </div>

            <!-- Message d'erreur global -->
            <div v-if="errorMessage" class="alert alert-danger" role="alert">
              <i class="bi bi-exclamation-triangle"></i>
              {{ errorMessage }}
            </div>

            <!-- Message de succès -->
            <div v-if="successMessage" class="alert alert-success" role="alert">
              <i class="bi bi-check-circle"></i>
              {{ successMessage }}
            </div>

            <!-- Bouton de soumission -->
            <div class="d-grid">
              <button 
                type="submit" 
                class="btn btn-primary"
                :disabled="isLoading"
              >
                <span 
                  v-if="isLoading" 
                  class="spinner-border spinner-border-sm me-2" 
                  role="status"
                ></span>
                {{ isLoading ? 'Connexion...' : 'Se connecter' }}
              </button>
            </div>
          </form>

          <!-- Lien vers l'inscription -->
          <div class="text-center mt-3">
            <p class="mb-0 text-muted">
              Pas encore de compte ?
              <router-link to="/register" class="text-decoration-none">
                Créer un compte
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      errors: {},
      errorMessage: '',
      successMessage: '',
      isLoading: false
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true
      this.errors = {}
      this.errorMessage = ''
      this.successMessage = ''

      try {
        // Validation côté client
        if (!this.validateForm()) {
          this.isLoading = false
          return
        }

        // Appel API pour la connexion
        const response = await api.login(
          this.loginForm.username,
          this.loginForm.password
        )

        // Sauvegarder les infos utilisateur
        localStorage.setItem('user', JSON.stringify(response.user))
        
        this.successMessage = response.message || 'Connexion réussie !'
        
        // Redirection après un court délai
        setTimeout(() => {
          this.$router.push('/')
        }, 1000)

      } catch (error) {
        console.error('Erreur de connexion:', error)
        
        if (error.response?.status === 401) {
          this.errorMessage = 'Nom d\'utilisateur ou mot de passe incorrect'
        } else if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'Erreur de connexion. Veuillez réessayer.'
        }
      } finally {
        this.isLoading = false
      }
    },

    validateForm() {
      let isValid = true

      // Validation du username
      if (!this.loginForm.username.trim()) {
        this.errors.username = 'Le nom d\'utilisateur est requis'
        isValid = false
      } else if (this.loginForm.username.length < 3) {
        this.errors.username = 'Le nom d\'utilisateur doit faire au moins 3 caractères'
        isValid = false
      }

      // Validation du password
      if (!this.loginForm.password) {
        this.errors.password = 'Le mot de passe est requis'
        isValid = false
      } else if (this.loginForm.password.length < 6) {
        this.errors.password = 'Le mot de passe doit faire au moins 6 caractères'
        isValid = false
      }

      return isValid
    }
  },
  
  // Rediriger si déjà connecté
  created() {
    if (localStorage.getItem('user')) {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-title i {
  margin-right: 0.5rem;
}

.btn-primary {
  font-weight: 500;
}
</style>