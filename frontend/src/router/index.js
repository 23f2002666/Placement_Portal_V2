import { createRouter, createWebHistory } from 'vue-router'

// 1. Import all the components you created
import Login from '../views/LoginView.vue'
import Register from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import AllDrives from '../views/AllDrives.vue'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'; 

const routes = [
    {
    path: '/',
    name: 'home',
    component: HomeView 
  },
  {
    path: '/student/profile',
    name: 'StudentProfile',
    component: ProfileView
  },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { 
    path: '/admin', 
    component: AdminDashboard,
    beforeEnter: (to, from, next) => {
      
      localStorage.getItem('user_role') === 'admin' ? next() : next('/login')
    }
  },
  { 
    path: '/company', 
    component: CompanyDashboard,
    beforeEnter: (to, from, next) => {
      localStorage.getItem('user_role') === 'company' ? next() : next('/login')
    }
  },
  { 
    path: '/student', 
    component: StudentDashboard,
    beforeEnter: (to, from, next) => {
      localStorage.getItem('user_role') === 'student' ? next() : next('/login')
    }
  },
  { path: '/search', component: AllDrives },
  { path: '/', redirect: '/login' } 
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router