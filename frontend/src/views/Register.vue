<template>
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-5">
      <div class="card">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">
            <i class="bi bi-person-plus text-primary"></i>
            Inscription
          </h2>

          <!-- Formulaire d'inscription -->
          <form @submit.prevent="handleRegister">
            <!-- Nom d'utilisateur -->
            <div class="mb-3">
              <label for="username" class="form-label">Nom d'utilisateur</label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="registerForm.username"
                :class="{ 'is-invalid': errors.username }"
                required
                autofocus
                placeholder="Ex: john_doe"
              >
              <div v-if="errors.username" class="invalid-feedback">
                {{ errors.username }}
              </div>
            </div>

            <!-- Email -->
            <div class="mb-3">
              <label for="email" class="form-label">Adresse email</label>
              <input
                type="email"
                class="form-control"
                id="email"
                v-model="registerForm.email"
                :class="{ 'is-invalid': errors.email }"
                required
                placeholder="john@example.com"
              >
              <div v-if="errors.email" class="invalid-feedback">
                {{ errors.email }}
              </div>
            </div>

            <!-- Nom d'affichage -->
            <div class="mb-3">
              <label for="display_name" class="form-label">Nom d'affichage</label>
              <input
                type="text"
                class="form-control"
                id="display_name"
                v-model="registerForm.display_name"
                :class="{ 'is-invalid': errors.display_name }"
                required
                placeholder="John Doe"
              >
              <div v-if="errors.display_name" class="invalid-feedback">
                {{ errors.display_name }}
              </div>
            </div>

            <!-- Bio (optionnel) -->
            <div class="mb-3">
              <label for="bio" class="form-label">Bio <span class="text-muted">(optionnel)</span></label>
              <textarea
                class="form-control"
                id="bio"
                v-model="registerForm.bio"
                rows="3"
                placeholder="Parlez-nous de vous..."
              ></textarea>
            </div>

            <!-- Mot de passe -->
            <div class="mb-3">
              <label for="password" class="form-label">Mot de passe</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="registerForm.password"
                :class="{ 'is-invalid': errors.password }"
                required
              >
              <div v-if="errors.password" class="invalid-feedback">
                {{ errors.password }}
              </div>
              <div class="form-text">Au moins 6 caractères</div>
            </div>

            <!-- Confirmation mot de passe -->
            <div class="mb-3">
              <label for="confirmPassword" class="form-label">Confirmer le mot de passe</label>
              <input
                type="password"
                class="form-control"
                id="confirmPassword"
                v-model="confirmPassword"
                :class="{ 'is-invalid': errors.confirmPassword }"
                required
              >
              <div v-if="errors.confirmPassword" class="invalid-feedback">
                {{ errors.confirmPassword }}
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
                {{ isLoading ? 'Création...' : 'Créer mon compte' }}
              </button>
            </div>
          </form>

          <!-- Lien vers la connexion -->
          <div class="text-center mt-3">
            <p class="mb-0 text-muted">
              Déjà un compte ?
              <router-link to="/login" class="text-decoration-none">
                Se connecter
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
  name: 'Register',
  data() {
    return {
      registerForm: {
        username: '',
        email: '',
        display_name: '',
        bio: '',
        password: ''
      },
      confirmPassword: '',
      errors: {},
      errorMessage: '',
      successMessage: '',
      isLoading: false
    }
  },
  methods: {
    async handleRegister() {
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

        // Appel API pour l'inscription
        const response = await api.register(this.registerForm)

        // Sauvegarder les infos utilisateur
        localStorage.setItem('user', JSON.stringify(response.user))
        
        this.successMessage = response.message || 'Compte créé avec succès !'
        
        // Redirection après un court délai
        setTimeout(() => {
          this.$router.push('/')
        }, 1500)

      } catch (error) {
        console.error('Erreur d\'inscription:', error)
        
        if (error.response?.status === 400) {
          const detail = error.response.data.detail
          if (detail.includes('Username already taken')) {
            this.errors.username = 'Ce nom d\'utilisateur est déjà pris'
          } else if (detail.includes('Email already registered')) {
            this.errors.email = 'Cette adresse email est déjà utilisée'
          } else {
            this.errorMessage = detail
          }
        } else {
          this.errorMessage = 'Erreur lors de la création du compte. Veuillez réessayer.'
        }
      } finally {
        this.isLoading = false
      }
    },

    validateForm() {
      let isValid = true

      // Validation du username
      if (!this.registerForm.username.trim()) {
        this.errors.username = 'Le nom d\'utilisateur est requis'
        isValid = false
      } else if (this.registerForm.username.length < 3) {
        this.errors.username = 'Le nom d\'utilisateur doit faire au moins 3 caractères'
        isValid = false
      } else if (!/^[a-zA-Z0-9_]+$/.test(this.registerForm.username)) {
        this.errors.username = 'Le nom d\'utilisateur ne peut contenir que des lettres, chiffres et _'
        isValid = false
      }

      // Validation de l'email
      if (!this.registerForm.email.trim()) {
        this.errors.email = 'L\'adresse email est requise'
        isValid = false
      } else if (!this.isValidEmail(this.registerForm.email)) {
        this.errors.email = 'Adresse email invalide'
        isValid = false
      }

      // Validation du nom d'affichage
      if (!this.registerForm.display_name.trim()) {
        this.errors.display_name = 'Le nom d\'affichage est requis'
        isValid = false
      } else if (this.registerForm.display_name.length < 2) {
        this.errors.display_name = 'Le nom d\'affichage doit faire au moins 2 caractères'
        isValid = false
      }

      // Validation du password
      if (!this.registerForm.password) {
        this.errors.password = 'Le mot de passe est requis'
        isValid = false
      } else if (this.registerForm.password.length < 6) {
        this.errors.password = 'Le mot de passe doit faire au moins 6 caractères'
        isValid = false
      }

      // Validation de la confirmation du password
      if (!this.confirmPassword) {
        this.errors.confirmPassword = 'Veuillez confirmer le mot de passe'
        isValid = false
      } else if (this.registerForm.password !== this.confirmPassword) {
        this.errors.confirmPassword = 'Les mots de passe ne correspondent pas'
        isValid = false
      }

      return isValid
    },

    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(email)
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