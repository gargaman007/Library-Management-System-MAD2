<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" v-if="showNavbarBrand" to="/">Grocery Store</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsUser" to="/home">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsUser" to="/products">Products</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsUser" to="/category">Category</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsUser" to="/cart">Cart</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsUser" to="/orders">Orders</router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsManager" to="/home">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsManager" to="/manage-category">Manage Category</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsManager" to="/manage-product">Manage Product</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsManager" to="/view-orders">View All Orders</router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsAdmin" to="/home">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsAdmin" to="/manage-category">Manage Category</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsAdmin" to="/manage-product">Manage Product</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsAdmin" to="/manage-orders">Manage Orders</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsAdmin" to="/managers-requests">Managers Requests</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsAdmin" to="/all-customers">All Customers</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="showNavbarItemsAdmin" to="/all-managers">All Managers</router-link>
          </li>
        </ul>
      </div>
      <div class="d-flex">
        <form class="form-inline" role="search" v-if="showSearchForm">
          <div class="input-group">
            <input type="search" class="form-control" placeholder="Search..." aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </div>
        </form>
        <div class="dropdown ml-2" v-if="showDropdown">
          <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown"
            aria-haspopup="true" aria-expanded="false">
            {{ userName }}
          </button>
          <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <router-link class="dropdown-item" v-if="showLogin" to="/login">Login</router-link>
            <button class="dropdown-item" v-if="showLogout" @click="logoutUser">Logout</button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  name: 'Navbar',
  computed: {
    showNavbarBrand() {
      return this.$route.name === 'login' || this.$route.name === 'register';
    },
    showNavbarItemsUser() {
      return this.userRole === 'user' && (this.$route.name === 'home' || this.$route.name === 'products' || this.$route.name === 'category' || this.$route.name === 'cart' || this.$route.name === 'orders');
    },
    showNavbarItemsManager() {
      return this.userRole === 'manager' && (this.$route.name === 'home' || this.$route.name === 'manage-category' || this.$route.name === 'manage-product' || this.$route.name === 'view-orders');
    },
    showNavbarItemsAdmin() {
      return this.userRole === 'admin' && (this.$route.name === 'home' || this.$route.name === 'manage-category' || this.$route.name === 'manage-product' || this.$route.name === 'manage-orders' || this.$route.name === 'managers-requests' || this.$route.name === 'all-customers' || this.$route.name === 'all-managers');
    },
    showSearchForm() {
      return this.userRole === 'user' || this.$route.name === 'search';
    },
    showDropdown() {
      return this.showLogin || this.showLogout;
    },
    showLogin() {
      return this.$route.name === 'login';
    },
    showLogout() {
      return this.$route.name !== 'login' && this.$route.name !== 'register' && this.userRole;
    },
    userName() {
      // Implement logic to get the user's name or username
      return 'User Name';
    },
    userRole() {
      return localStorage.getItem('userRole');
    },
  },
  methods: {
    logoutUser() {
      axios.post(`${API_BASE_URL}/logout`, {
        uid: localStorage.getItem('userId'),
        role: localStorage.getItem('userRole'),
      })
        .then(response => {
          localStorage.removeItem('userRole');
          localStorage.removeItem('authToken');
          localStorage.removeItem('userId');
          this.$router.push('/');
        })
        .catch(error => {
          console.error('Logout error:', error);
        });
    },
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
