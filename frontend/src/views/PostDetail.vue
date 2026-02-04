<template>
  <div class="container py-4">
    <!-- Loading -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
    </div>

    <!-- Post non trouvé -->
    <div v-else-if="!post" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-warning" style="font-size: 3rem;"></i>
      <h3 class="mt-3">Post non trouvé</h3>
      <p class="text-muted">Ce post n'existe pas ou a été supprimé</p>
      <router-link to="/" class="btn btn-primary">
        <i class="bi bi-house"></i>
        Retour à l'accueil
      </router-link>
    </div>

    <!-- Post détaillé -->
    <div v-else>
      <!-- Bouton retour -->
      <button @click="goBack" class="btn btn-outline-secondary mb-4">
        <i class="bi bi-arrow-left"></i>
        Retour
      </button>

      <!-- Post principal -->
      <div class="card mb-4">
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
          </div>

          <!-- Contenu du post -->
          <div class="mb-3">
            <p class="mb-2 fs-5">{{ post.content }}</p>
            <img 
              v-if="post.image_url" 
              :src="post.image_url" 
              class="img-fluid rounded"
              style="max-height: 400px; width: auto;"
              alt="Image du post"
            >
          </div>

          <!-- Statistiques -->
          <div class="row text-center border-top border-bottom py-2 mb-3">
            <div class="col">
              <div class="fw-bold">{{ post.like_count || 0 }}</div>
              <small class="text-muted">Likes</small>
            </div>
            <div class="col">
              <div class="fw-bold">{{ comments.length }}</div>
              <small class="text-muted">Commentaires</small>
            </div>
          </div>

          <!-- Actions -->
          <div class="d-flex justify-content-around border-bottom pb-3 mb-3">
            <button 
              class="btn btn-sm like-btn d-flex align-items-center"
              :class="{ 'liked': post.is_liked }"
              @click="toggleLike"
              :disabled="!isLoggedIn || isLiking"
            >
              <i class="bi" :class="post.is_liked ? 'bi-heart-fill' : 'bi-heart'"></i>
              <span class="ms-1">Like</span>
            </button>
            
            <button class="btn btn-sm btn-outline-secondary d-flex align-items-center">
              <i class="bi bi-chat"></i>
              <span class="ms-1">Commenter</span>
            </button>
          </div>

          <!-- Zone de commentaire (si connecté) -->
          <div v-if="isLoggedIn" class="mb-4">
            <form @submit.prevent="submitComment">
              <div class="mb-3">
                <textarea 
                  v-model="newComment"
                  class="form-control"
                  rows="3"
                  placeholder="Écrivez votre commentaire..."
                  required
                ></textarea>
              </div>
              <button 
                type="submit" 
                class="btn btn-primary"
                :disabled="!newComment.trim() || isSubmittingComment"
              >
                <span v-if="isSubmittingComment" class="spinner-border spinner-border-sm me-2"></span>
                Commenter
              </button>
            </form>
          </div>

          <!-- Message si pas connecté -->
          <div v-else class="text-center py-3 bg-light rounded mb-4">
            <p class="mb-2">Connectez-vous pour commenter</p>
            <router-link to="/login" class="btn btn-primary btn-sm">
              Se connecter
            </router-link>
          </div>
        </div>
      </div>

      <!-- Commentaires -->
      <div class="comments-section">
        <h5 class="mb-3">
          <i class="bi bi-chat-square-text"></i>
          Commentaires ({{ comments.length }})
        </h5>

        <!-- Liste des commentaires -->
        <div v-if="comments.length > 0">
          <div 
            v-for="comment in comments"
            :key="comment.id"
            class="card mb-3"
          >
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div class="d-flex align-items-center">
                  <router-link 
                    :to="`/profile/${comment.author.username}`"
                    class="text-decoration-none fw-bold me-2"
                  >
                    {{ comment.author.display_name }}
                  </router-link>
                  <span class="text-muted small">@{{ comment.author.username }}</span>
                  <span class="text-muted mx-2">•</span>
                  <span class="text-muted small">{{ formatDate(comment.created_at) }}</span>
                </div>
              </div>
              <p class="mb-2">{{ comment.content }}</p>
              
              <!-- Actions commentaire -->
              <div class="d-flex align-items-center gap-2">
                <button 
                  class="btn btn-sm like-btn d-flex align-items-center"
                  :class="{ 'liked': comment.is_liked }"
                  @click="toggleCommentLike(comment)"
                  :disabled="!isLoggedIn"
                >
                  <i class="bi" :class="comment.is_liked ? 'bi-heart-fill' : 'bi-heart'"></i>
                  <span class="ms-1">{{ comment.like_count || 0 }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Message si pas de commentaires -->
        <div v-else class="text-center py-4">
          <i class="bi bi-chat-square text-muted" style="font-size: 2rem;"></i>
          <p class="text-muted mt-2">Aucun commentaire pour le moment</p>
          <p class="text-muted small">Soyez le premier à commenter !</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js'

export default {
  name: 'PostDetail',
  data() {
    return {
      post: null,
      comments: [],
      newComment: '',
      isLoading: true,
      isLiking: false,
      isSubmittingComment: false,
      currentUser: null
    }
  },
  computed: {
    isLoggedIn() {
      return this.currentUser !== null
    }
  },
  created() {
    this.loadUserInfo()
    this.loadPost()
    this.loadComments()
  },
  methods: {
    loadUserInfo() {
      const userData = localStorage.getItem('user')
      if (userData) {
        this.currentUser = JSON.parse(userData)
      }
    },

    async loadPost() {
      try {
        const postId = this.$route.params.id
        this.post = await api.getPost(postId)
      } catch (error) {
        console.error('Erreur lors du chargement du post:', error)
      } finally {
        this.isLoading = false
      }
    },

    async loadComments() {
      try {
        const postId = this.$route.params.id
        this.comments = await api.getPostComments(postId)
      } catch (error) {
        console.error('Erreur lors du chargement des commentaires:', error)
      }
    },

    async toggleLike() {
      if (!this.isLoggedIn || this.isLiking) return

      this.isLiking = true
      try {
        const response = await api.togglePostLike(this.post.id)
        this.post.is_liked = response.is_liked
        this.post.like_count = response.like_count
      } catch (error) {
        console.error('Erreur lors du like:', error)
      } finally {
        this.isLiking = false
      }
    },

    async toggleCommentLike(comment) {
      if (!this.isLoggedIn) return

      try {
        const response = await api.toggleCommentLike(comment.id)
        comment.is_liked = response.is_liked
        comment.like_count = response.like_count
      } catch (error) {
        console.error('Erreur lors du like de commentaire:', error)
      }
    },

    async submitComment() {
      if (!this.newComment.trim() || this.isSubmittingComment) return

      this.isSubmittingComment = true
      try {
        const newComment = await api.createComment(this.post.id, this.newComment)
        this.comments.push(newComment)
        this.newComment = ''
      } catch (error) {
        console.error('Erreur lors de la création du commentaire:', error)
        alert('Erreur lors de la création du commentaire')
      } finally {
        this.isSubmittingComment = false
      }
    },

    goBack() {
      this.$router.go(-1)
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('fr-FR', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.like-btn {
  background: none;
  border: none;
  color: #6c757d;
  transition: color 0.2s ease;
}

.like-btn:hover {
  color: #dc3545;
}

.like-btn.liked {
  color: #dc3545;
}

.post-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>