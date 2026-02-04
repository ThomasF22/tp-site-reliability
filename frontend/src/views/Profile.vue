<template>
  <div>
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
      <p class="mt-2 text-muted">Chargement du profil...</p>
    </div>

    <div v-else-if="user" class="row">
      <!-- Informations du profil -->
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-body text-center">
            <div class="mb-3">
              <i class="bi bi-person-circle text-muted" style="font-size: 4rem;"></i>
            </div>
            <h3>{{ user.display_name }}</h3>
            <p class="text-muted mb-2">@{{ user.username }}</p>
            <p v-if="user.bio" class="mb-3">{{ user.bio }}</p>
            
            <div class="row text-center mt-3">
              <div class="col-6">
                <div class="h5 mb-0 text-primary">{{ user.post_count || 0 }}</div>
                <small class="text-muted">Posts</small>
              </div>
              <div class="col-6">
                <div class="h5 mb-0 text-success">{{ user.follower_count || 0 }}</div>
                <small class="text-muted">Abonnés</small>
              </div>
            </div>

            <div v-if="user.created_at" class="mt-3">
              <small class="text-muted">
                <i class="bi bi-calendar"></i>
                Inscrit en {{ formatJoinDate(user.created_at) }}
              </small>
            </div>
          </div>
        </div>

        <!-- Posts de l'utilisateur -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4>
            <i class="bi bi-chat-square-text"></i>
            Posts de {{ user.display_name }}
          </h4>
        </div>

        <!-- Liste des posts -->
        <div v-if="user.posts && user.posts.length > 0">
          <PostCard
            v-for="post in user.posts"
            :key="post.id"
            :post="post"
            @postLiked="handlePostLiked"
            @postDeleted="handlePostDeleted"
          />
        </div>
        
        <!-- Aucun post -->
        <div v-else class="text-center py-5">
          <i class="bi bi-chat-square-text text-muted" style="font-size: 3rem;"></i>
          <h5 class="mt-3 text-muted">Aucun post</h5>
          <p class="text-muted">{{ user.display_name }} n'a pas encore publié de contenu.</p>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5">
      <i class="bi bi-person-x text-muted" style="font-size: 4rem;"></i>
      <h4 class="mt-3 text-muted">Utilisateur introuvable</h4>
      <p class="text-muted">Cet utilisateur n'existe pas ou a supprimé son compte.</p>
      <router-link to="/" class="btn btn-primary">
        Retour à l'accueil
      </router-link>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js'
import PostCard from '../components/PostCard.vue'

export default {
  name: 'Profile',
  components: {
    PostCard
  },
  data() {
    return {
      user: null,
      isLoading: false,
      errorMessage: ''
    }
  },
  async created() {
    await this.loadUserProfile()
  },
  watch: {
    // Recharger si le paramètre username change
    '$route.params.username'() {
      this.loadUserProfile()
    }
  },
  methods: {
    async loadUserProfile() {
      this.isLoading = true
      this.errorMessage = ''

      try {
        const username = this.$route.params.username
        this.user = await api.getUserProfile(username)
      } catch (error) {
        console.error('Erreur lors du chargement du profil:', error)
        if (error.response?.status === 404) {
          this.user = null
        } else {
          this.errorMessage = 'Erreur lors du chargement du profil'
        }
      } finally {
        this.isLoading = false
      }
    },

    handlePostLiked(postId, likeData) {
      // Mettre à jour le post dans la liste
      if (this.user?.posts) {
        const postIndex = this.user.posts.findIndex(p => p.id === postId)
        if (postIndex !== -1) {
          this.user.posts[postIndex].like_count = likeData.like_count
          this.user.posts[postIndex].is_liked = likeData.is_liked
        }
      }
    },

    handlePostDeleted(postId) {
      // Retirer le post de la liste
      if (this.user?.posts) {
        this.user.posts = this.user.posts.filter(p => p.id !== postId)
        this.user.post_count = Math.max(0, this.user.post_count - 1)
      }
    },

    formatJoinDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long'
      })
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.bi-person-circle {
  color: #6c757d;
}

h3 {
  margin-bottom: 0.5rem;
}
</style>