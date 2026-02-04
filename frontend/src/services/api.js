import axios from 'axios'

// Configuration de base d'axios
const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important pour les cookies de session
  headers: {
    'Content-Type': 'application/json'
  }
})

// Intercepteur pour gérer les erreurs globalement
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Déconnexion automatique si non autorisé
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // Authentification
  async login(username, password) {
    const response = await api.post('/auth/login', {
      username,
      password
    })
    return response.data
  },

  async register(userData) {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  async logout() {
    const response = await api.post('/auth/logout')
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },

  // Posts
  async getPosts(skip = 0, limit = 20) {
    const response = await api.get(`/posts/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  async getPost(postId) {
    const response = await api.get(`/posts/${postId}`)
    return response.data
  },

  async createPost(content, imageUrl = null) {
    const response = await api.post('/posts/', {
      content,
      image_url: imageUrl
    })
    return response.data
  },

  async updatePost(postId, content, imageUrl = null) {
    const response = await api.put(`/posts/${postId}`, {
      content,
      image_url: imageUrl
    })
    return response.data
  },

  async deletePost(postId) {
    const response = await api.delete(`/posts/${postId}`)
    return response.data
  },

  async togglePostLike(postId) {
    const response = await api.post(`/posts/${postId}/like`)
    return response.data
  },

  // Commentaires
  async createComment(postId, content) {
    const response = await api.post('/comments/', {
      post_id: postId,
      content
    })
    return response.data
  },

  async getPostComments(postId) {
    const response = await api.get(`/comments/post/${postId}`)
    return response.data
  },

  async updateComment(commentId, content) {
    const response = await api.put(`/comments/${commentId}`, {
      content
    })
    return response.data
  },

  async deleteComment(commentId) {
    const response = await api.delete(`/comments/${commentId}`)
    return response.data
  },

  async toggleCommentLike(commentId) {
    const response = await api.post(`/comments/${commentId}/like`)
    return response.data
  },

  // Utilisateurs
  async getUsers(skip = 0, limit = 20) {
    const response = await api.get(`/users/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  async getUserProfile(username) {
    const response = await api.get(`/users/${username}`)
    return response.data
  },

  async updateProfile(userData) {
    const response = await api.put('/users/me', userData)
    return response.data
  },

  async getMyPosts() {
    const response = await api.get('/users/me/posts')
    return response.data
  }
}