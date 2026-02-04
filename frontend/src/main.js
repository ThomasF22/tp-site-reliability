import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Import Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
// Import Bootstrap Icons
import 'bootstrap-icons/font/bootstrap-icons.css'

// Import des vues
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Profile from './views/Profile.vue'
import PostDetail from './views/PostDetail.vue'

// Configuration du routeur
const routes = [
  { 
    path: '/', 
    name: 'Home', 
    component: Home,
    meta: { requiresAuth: false }
  },
  { 
    path: '/login', 
    name: 'Login', 
    component: Login,
    meta: { requiresAuth: false }
  },
  { 
    path: '/register', 
    name: 'Register', 
    component: Register,
    meta: { requiresAuth: false }
  },
  { 
    path: '/profile/:username', 
    name: 'Profile', 
    component: Profile,
    meta: { requiresAuth: false }
  },
  { 
    path: '/posts/:id', 
    name: 'PostDetail', 
    component: PostDetail,
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard pour l'authentification
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user') !== null
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

const app = createApp(App)
app.use(router)
app.mount('#app')