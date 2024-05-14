import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import register from '../views/Register.vue'

import adminpanel from '../views/adminpanel.vue'
import Editbooks from '../views/editbooks.vue'
import EditSection from '../views/editsection.vue'
import index from '../views/index.vue'
import Logout from '../views/logout.vue'
import Managebooks from '../views/managebooks.vue'


import manageissues from '../views/manageissues.vue'
import managerequests from '../views/managerequests.vue'

import feedback from '../views/feedbacks.vue'
import ManageSections from '../views/managesection.vue'

import Search from '../views/search.vue'
import section from '../views/section.vue'
import SectionBooks from '../views/sectionbooks.vue'
import UserIssue from '../views/user_issue.vue'
import UserProfile from '../views/userprofile.vue'

const routes = [
  {
    path: '/feedback',
    name: 'feedback',
    component: feedback,
  },
  {
    path: '/view-issued-books',
    name: 'manageissues',
    component: manageissues,
  },
  {
    path: '/manage-requests',
    name: 'managerequests',
    component: managerequests,
  },
  {
    path: '/section/:sectionId',
    name: 'SectionBooks',
    component: SectionBooks,
  },
  {
    path: '/userissues',
    name: 'UserIssue',
    component: UserIssue,
  },
  {
    path: '/userprofile',
    name: 'UserProfile',
    component: UserProfile,
  },
  {
    path: '/section',
    name: 'section',
    component: section,
  },
  {
    path:'/manage-books',
    name: 'manage-books',
    component: Managebooks
  },

  {
    path: '/manage-sections',
    name: 'ManageSections',
    component: ManageSections,
  },

  {
    path: '/admin',
    name: 'admin',
    component: adminpanel
  },
  {
    path: '/logout',
    name: 'logout',
    component: Logout
  },


  {
    path: '/search',
    name: 'Search',
    component: Search,
    props: (route) => ({ query: route.query.q }), // Pass the query parameter as a prop
  },
  {
    path: '/editbook/:id',
    name: 'editbook',
    component: Editbooks,
  },


  {
    path: '/edit-section/:id',
    name: 'editsection',
    component: EditSection,
  }
,
  {
    path: '/register',
    name: 'register',
    component: register
  },
  {
    path:'/login',
    name:'login',
    component: Login
  },
  {
    path:'/index',
    name: 'index',
    component: index
  },
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
