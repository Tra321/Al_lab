import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue')
    },
    {
      path: '/book/:id',
      name: 'bookDetail',
      component: () => import('../views/BookDetail.vue')
    },
    {
      path: '/publish',
      name: 'publish',
      component: () => import('../views/Publish.vue')
    },
    {
      path: '/category/:type',
      name: 'category',
      component: () => import('../views/Category.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/Search.vue')
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../views/Orders.vue')
    },
    {
      path: '/order/:id',
      name: 'orderDetail',
      component: () => import('../views/OrderDetail.vue')
    },
    {
      path: '/address',
      name: 'address',
      component: () => import('../views/Address.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue')
    }
  ]
})

export default router