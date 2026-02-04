<template>
  <div class="row">
    <!-- Colonne principale -->
    <div class="col-lg-8">
      <!-- Zone de création de post (si connecté) -->
      <CreatePost v-if="isLoggedIn" @postCreated="handlePostCreated" />

      <!-- Titre -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3>
          <i class="bi bi-house-fill text-primary"></i>
          Fil d'actualité
        </h3>
        <button 
          class="btn btn-outline-secondary btn-sm"
          @click="refreshPosts"
          :disabled="isLoadingPosts"
        >
          <i class="bi bi-arrow-clockwise"></i>
          Actualiser
        </button>
      </div>

      <!-- Loading des posts -->
      <div v-if="isLoadingPosts && posts.length === 0" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Chargement...</span>
        </div>
        <p class="mt-2 text-muted">Chargement des posts...</p>
      </div>

      <!-- Message si aucun post -->
      <div v-else-if="posts.length === 0 && !isLoadingPosts" class="text-center py-5">
        <i class="bi bi-chat-square-text-fill text-muted" style="font-size: 3rem;"></i>
        <h5 class="mt-3 text-muted">Aucun post pour le moment</h5>
        <p class="text-muted">Soyez le premier à partager quelque chose !</p>
        <router-link v-if="!isLoggedIn" to="/register" class="btn btn-primary">
          Rejoindre la communauté
        </router-link>
      </div>

      <!-- Liste des posts -->
      <div v-else>
        <PostCard
          v-for="post in posts"
          :key="post.id"
          :post="post"
          @postLiked="handlePostLiked"
          @postDeleted="handlePostDeleted"
        />

        <!-- Bouton charger plus -->
        <div v-if="hasMorePosts" class="text-center mt-4">
          <button 
            class="btn btn-outline-primary"
            @click="loadMorePosts"
            :disabled="isLoadingMore"
          >
            <span 
              v-if="isLoadingMore" 
              class="spinner-border spinner-border-sm me-2" 
              role="status"
            ></span>
            {{ isLoadingMore ? 'Chargement...' : 'Charger plus' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Sidebar droite -->
    <div class="col-lg-4">
      <!-- Widget de bienvenue -->
      <div class="card mb-3" v-if="!isLoggedIn">
        <div class="card-body">
          <h5 class="card-title">
            <i class="bi bi-heart-fill text-danger"></i>
            Bienvenue sur Forum !
          </h5>
          <p class="card-text text-muted">
            Rejoignez notre communauté et partagez vos idées avec le monde entier.
          </p>
          <div class="d-grid gap-2">
            <router-link to="/register" class="btn btn-primary">
              Créer un compte
            </router-link>
            <router-link to="/login" class="btn btn-outline-primary">
              Se connecter
            </router-link>
          </div>
        </div>
      </div>

      <!-- Statistiques du forum -->
      <div class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">
            <i class="bi bi-graph-up text-success"></i>
            Statistiques
          </h5>
          <div class="row text-center">
            <div class="col-6">
              <div class="h4 mb-0 text-primary">{{ totalPosts }}</div>
              <small class="text-muted">Posts</small>
            </div>
            <div class="col-6">
              <div class="h4 mb-0 text-success">{{ totalUsers }}</div>
              <small class="text-muted">Membres</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Utilisateurs suggérés -->
      <div class="card" v-if="suggestedUsers.length > 0">
        <div class="card-body">
          <h5 class="card-title">
            <i class="bi bi-people text-info"></i>
            Utilisateurs à découvrir
          </h5>
          <div 
            v-for="user in suggestedUsers" 
            :key="user.id"
            class="d-flex align-items-center mb-2"
          >
            <div class="flex-grow-1">
              <router-link 
                :to="`/profile/${user.username}`"
                class="text-decoration-none fw-bold"
              >
                {{ user.display_name }}
              </router-link>
              <div class="small text-muted">@{{ user.username }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js'
import PostCard from '../components/PostCard.vue'
import CreatePost from '../components/CreatePost.vue'

export default {
  name: 'Home',
  components: {
    PostCard,
    CreatePost
  },
  data() {
    return {
      posts: [],
      suggestedUsers: [],
      isLoadingPosts: false,
      isLoadingMore: false,
      hasMorePosts: true,
      currentSkip: 0,
      postsPerPage: 10,
      totalPosts: 0,
      totalUsers: 0,
      currentUser: null
    }
  },
  computed: {
    isLoggedIn() {
      return this.currentUser !== null
    }
  },
  async created() {
    this.loadUserInfo()
    await this.loadPosts()
    await this.loadStats()
    await this.loadSuggestedUsers()
  },
  methods: {
    loadUserInfo() {
      const userData = localStorage.getItem('user')
      if (userData) {
        this.currentUser = JSON.parse(userData)
      }
    },

    async loadPosts(append = false) {
      try {
        if (!append) {
          this.isLoadingPosts = true
          this.currentSkip = 0
        } else {
          this.isLoadingMore = true
        }

        const posts = await api.getPosts(this.currentSkip, this.postsPerPage)
        
        if (append) {
          this.posts = [...this.posts, ...posts]
        } else {
          this.posts = posts
        }

        this.hasMorePosts = posts.length === this.postsPerPage
        this.currentSkip += posts.length

      } catch (error) {
        console.error('Erreur lors du chargement des posts:', error)
      } finally {
        this.isLoadingPosts = false
        this.isLoadingMore = false
      }
    },

    async loadMorePosts() {
      await this.loadPosts(true)
    },

    async refreshPosts() {
      await this.loadPosts()
    },

    async loadStats() {
      try {
        // Estimer les stats depuis les posts chargés
        this.totalPosts = this.posts.length > 0 ? this.posts.length : 0
        
        // Charger quelques utilisateurs pour avoir une estimation
        const users = await api.getUsers(0, 5)
        this.totalUsers = users.length
      } catch (error) {
        console.error('Erreur lors du chargement des stats:', error)
      }
    },

    async loadSuggestedUsers() {
      try {
        const users = await api.getUsers(0, 3)
        this.suggestedUsers = users.slice(0, 3)
      } catch (error) {
        console.error('Erreur lors du chargement des utilisateurs suggérés:', error)
      }
    },

    handlePostCreated(newPost) {
      // Ajouter le nouveau post en haut de la liste
      this.posts.unshift(newPost)
      this.totalPosts++
    },

    handlePostLiked(postId, likeData) {
      // Mettre à jour le post dans la liste
      const postIndex = this.posts.findIndex(p => p.id === postId)
      if (postIndex !== -1) {
        this.posts[postIndex].like_count = likeData.like_count
        this.posts[postIndex].is_liked = likeData.is_liked
      }
    },

    handlePostDeleted(postId) {
      // Retirer le post de la liste
      this.posts = this.posts.filter(p => p.id !== postId)
      this.totalPosts = Math.max(0, this.totalPosts - 1)
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
</style>