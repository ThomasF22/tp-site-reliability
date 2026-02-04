<template>
  <div class="card mb-4">
    <div class="card-body">
      <h5 class="card-title">
        <i class="bi bi-pencil-square text-primary"></i>
        Quoi de neuf ?
      </h5>
      
      <form @submit.prevent="handleSubmit">
        <!-- Zone de texte -->
        <div class="mb-3">
          <textarea
            class="form-control"
            rows="3"
            placeholder="Partagez vos pensées..."
            v-model="postContent"
            :class="{ 'is-invalid': errors.content }"
            maxlength="500"
          ></textarea>
          <div v-if="errors.content" class="invalid-feedback">
            {{ errors.content }}
          </div>
          <div class="form-text d-flex justify-content-between">
            <span>{{ postContent.length }}/500 caractères</span>
            <span v-if="postContent.length > 400" :class="getCharacterCountClass()">
              {{ 500 - postContent.length }} caractères restants
            </span>
          </div>
        </div>

        <!-- URL d'image (optionnel) -->
        <div class="mb-3">
          <label for="imageUrl" class="form-label">
            <i class="bi bi-image"></i>
            Image (optionnel)
          </label>
          <input
            type="url"
            class="form-control"
            id="imageUrl"
            v-model="imageUrl"
            placeholder="https://exemple.com/image.jpg"
            :class="{ 'is-invalid': errors.imageUrl }"
          >
          <div v-if="errors.imageUrl" class="invalid-feedback">
            {{ errors.imageUrl }}
          </div>
        </div>

        <!-- Prévisualisation de l'image -->
        <div v-if="imageUrl && isValidImageUrl" class="mb-3">
          <div class="text-muted small mb-2">Aperçu :</div>
          <img 
            :src="imageUrl" 
            class="img-fluid rounded"
            style="max-height: 200px; width: auto;"
            alt="Aperçu"
            @error="imageError = true"
            @load="imageError = false"
          >
        </div>

        <!-- Message d'erreur -->
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
          <i class="bi bi-exclamation-triangle"></i>
          {{ errorMessage }}
        </div>

        <!-- Message de succès -->
        <div v-if="successMessage" class="alert alert-success" role="alert">
          <i class="bi bi-check-circle"></i>
          {{ successMessage }}
        </div>

        <!-- Actions -->
        <div class="d-flex justify-content-between align-items-center">
          <div class="text-muted small">
            <i class="bi bi-globe"></i>
            Visible par tous
          </div>
          
          <div class="d-flex gap-2">
            <button 
              type="button"
              class="btn btn-outline-secondary btn-sm"
              @click="clearForm"
              :disabled="isLoading"
            >
              <i class="bi bi-x-circle"></i>
              Effacer
            </button>
            
            <button 
              type="submit"
              class="btn btn-primary"
              :disabled="!canSubmit || isLoading"
            >
              <span 
                v-if="isLoading" 
                class="spinner-border spinner-border-sm me-2" 
                role="status"
              ></span>
              <i v-else class="bi bi-send me-1"></i>
              {{ isLoading ? 'Publication...' : 'Publier' }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js'

export default {
  name: 'CreatePost',
  emits: ['postCreated'],
  data() {
    return {
      postContent: '',
      imageUrl: '',
      errors: {},
      errorMessage: '',
      successMessage: '',
      isLoading: false,
      imageError: false
    }
  },
  computed: {
    canSubmit() {
      return this.postContent.trim().length > 0 && 
             this.postContent.length <= 500 &&
             !this.imageError
    },
    
    isValidImageUrl() {
      if (!this.imageUrl) return false
      try {
        const url = new URL(this.imageUrl)
        return ['http:', 'https:'].includes(url.protocol)
      } catch {
        return false
      }
    }
  },
  methods: {
    async handleSubmit() {
      this.isLoading = true
      this.errors = {}
      this.errorMessage = ''
      this.successMessage = ''

      try {
        // Validation
        if (!this.validateForm()) {
          this.isLoading = false
          return
        }

        // Création du post
        const newPost = await api.createPost(
          this.postContent.trim(),
          this.imageUrl || null
        )

        this.successMessage = 'Post publié avec succès !'
        this.$emit('postCreated', newPost)
        
        // Effacer le formulaire après un court délai
        setTimeout(() => {
          this.clearForm()
        }, 1000)

      } catch (error) {
        console.error('Erreur lors de la création du post:', error)
        
        if (error.response?.status === 401) {
          this.errorMessage = 'Vous devez être connecté pour publier'
          // Rediriger vers la page de connexion
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        } else if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'Erreur lors de la publication. Veuillez réessayer.'
        }
      } finally {
        this.isLoading = false
      }
    },

    validateForm() {
      let isValid = true

      // Validation du contenu
      if (!this.postContent.trim()) {
        this.errors.content = 'Le contenu ne peut pas être vide'
        isValid = false
      } else if (this.postContent.length > 500) {
        this.errors.content = 'Le contenu ne peut pas dépasser 500 caractères'
        isValid = false
      }

      // Validation de l'URL d'image
      if (this.imageUrl && !this.isValidImageUrl) {
        this.errors.imageUrl = 'URL d\'image invalide'
        isValid = false
      }

      return isValid
    },

    clearForm() {
      this.postContent = ''
      this.imageUrl = ''
      this.errors = {}
      this.errorMessage = ''
      this.successMessage = ''
      this.imageError = false
    },

    getCharacterCountClass() {
      const remaining = 500 - this.postContent.length
      if (remaining < 20) return 'text-danger'
      if (remaining < 50) return 'text-warning'
      return 'text-muted'
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-title i {
  margin-right: 0.5rem;
}

.form-control:focus {
  border-color: #1da1f2;
  box-shadow: 0 0 0 0.2rem rgba(29, 161, 242, 0.25);
}

.btn-primary {
  font-weight: 500;
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}
</style>