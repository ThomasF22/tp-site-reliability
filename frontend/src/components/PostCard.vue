<template>
  <div class="card post-card">
    <div class="card-body">
      <!-- En-tête du post -->
      <div class="d-flex align-items-start mb-3">
        <div class="flex-grow-1">
          <div class="d-flex align-items-center mb-1">
            <router-link 
              :to="`/profile/${post.author.username}`"
              class="text-decoration-none fw-bold me-2"
            >
              {{ post.author.display_name }}
            </router-link>
            <span class="text-muted small">@{{ post.author.username }}</span>
            <span class="text-muted mx-2">•</span>
            <span class="text-muted small">{{ formatDate(post.created_at) }}</span>
          </div>
        </div>
        
        <!-- Menu dropdown pour le propriétaire du post -->
        <div class="dropdown" v-if="isOwner">
          <button 
            class="btn btn-sm btn-outline-secondary dropdown-toggle"
            data-bs-toggle="dropdown"
          >
            <i class="bi bi-three-dots"></i>
          </button>
          <ul class="dropdown-menu">
            <li>
              <button class="dropdown-item text-danger" @click="deletePost">
                <i class="bi bi-trash"></i>
                Supprimer
              </button>
            </li>
          </ul>
        </div>
      </div>

      <!-- Contenu du post -->
      <div class="mb-3">
        <p class="mb-2">{{ post.content }}</p>
        <img 
          v-if="post.image_url" 
          :src="post.image_url" 
          class="img-fluid rounded"
          style="max-height: 300px; width: auto;"
          alt="Image du post"
        >
      </div>

      <!-- Actions (like, comment) -->
      <div class="d-flex align-items-center justify-content-between">
        <div class="d-flex align-items-center gap-3">
          <!-- Bouton like -->
          <button 
            class="btn btn-sm like-btn d-flex align-items-center"
            :class="{ 'liked': post.is_liked }"
            @click="toggleLike"
            :disabled="!isLoggedIn || isLiking"
          >
            <i class="bi" :class="post.is_liked ? 'bi-heart-fill' : 'bi-heart'"></i>
            <span class="ms-1">{{ post.like_count || 0 }}</span>
          </button>

          <!-- Bouton commentaire -->
          <router-link 
            :to="`/posts/${post.id}`"
            class="btn btn-sm btn-outline-secondary d-flex align-items-center text-decoration-none"
          >
            <i class="bi bi-chat"></i>
            <span class="ms-1">{{ post.comment_count || 0 }}</span>
          </router-link>
        </div>

        <!-- Timestamp détaillé -->
        <small class="text-muted">
          {{ formatDetailedDate(post.created_at) }}
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js'

export default {
  name: 'PostCard',
  props: {
    post: {
      type: Object,
      required: true
    }
  },
  emits: ['postLiked', 'postDeleted'],
  data() {
    return {
      isLiking: false,
      currentUser: null
    }
  },
  computed: {
    isLoggedIn() {
      return this.currentUser !== null
    },
    isOwner() {
      return this.isLoggedIn && this.currentUser.id === this.post.author.id
    }
  },
  created() {
    this.loadUserInfo()
  },
  methods: {
    loadUserInfo() {
      const userData = localStorage.getItem('user')
      if (userData) {
        this.currentUser = JSON.parse(userData)
      }
    },

    async toggleLike() {
      if (!this.isLoggedIn || this.isLiking) return

      this.isLiking = true
      try {
        const response = await api.togglePostLike(this.post.id)
        this.$emit('postLiked', this.post.id, response)
      } catch (error) {
        console.error('Erreur lors du like:', error)
      } finally {
        this.isLiking = false
      }
    },

    async deletePost() {
      if (!confirm('Êtes-vous sûr de vouloir supprimer ce post ?')) {
        return
      }

      try {
        await api.deletePost(this.post.id)
        this.$emit('postDeleted', this.post.id)
      } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        alert('Erreur lors de la suppression du post')
      }
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date

      // Moins d'une minute
      if (diff < 60000) {
        return 'à l\'instant'
      }
      
      // Moins d'une heure
      if (diff < 3600000) {
        return `${Math.floor(diff / 60000)}m`
      }
      
      // Moins de 24h
      if (diff < 86400000) {
        return `${Math.floor(diff / 3600000)}h`
      }
      
      // Moins d'une semaine
      if (diff < 604800000) {
        return `${Math.floor(diff / 86400000)}j`
      }
      
      // Plus d'une semaine
      return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short'
      })
    },

    formatDetailedDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.post-card {
  margin-bottom: 1rem;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.like-btn {
  border: none;
  background: none;
  color: #657786;
  transition: color 0.2s ease;
  padding: 0.25rem 0.5rem;
}

.like-btn:hover {
  color: #e1306c;
  background-color: rgba(225, 48, 108, 0.1);
}

.like-btn.liked {
  color: #e1306c;
}

.like-btn.liked:hover {
  color: #c42d5c;
}

.btn-outline-secondary:hover {
  background-color: rgba(108, 117, 125, 0.1);
  border-color: transparent;
  color: #6c757d;
}
</style>