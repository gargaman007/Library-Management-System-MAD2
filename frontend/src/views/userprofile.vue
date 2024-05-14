<template>
  <div>
    <nav>
      <h1>Library Management System</h1>
      <router-link to="/index">Home</router-link> |
      <router-link to="/section">Sections</router-link> |
      <router-link to="/userprofile">User Profile</router-link> |
      <router-link to="/userissues">User Issues</router-link> |
      <router-link to="/search">Search</router-link> |
      <button v-if="!isAuthenticated()" @click="loginClicked">Login</button>
      <button v-if="!isAuthenticated()" @click="registerClicked">Register</button>
      <router-link v-if="isAuthenticated()" to="/logout">Logout</router-link> |

    </nav>
    <h2>User Profile</h2>
    <div v-if="userProfile" class="profile-card">
      <h3>{{ userProfile.username }}</h3>
      <p>Email: {{ userProfile.email }}</p>
      <p>Last Login At: {{ userProfile.last_login_at }}</p>
      <p>Current Login At: {{ userProfile.current_login_at }}</p>
      <p>Last Login IP: {{ userProfile.last_login_ip }}</p>
      <p>Current Login IP: {{ userProfile.current_login_ip }}</p>
      <p>Login Count: {{ userProfile.login_count }}</p>
      <p>Active: {{ userProfile.active }}</p>
      <p>Confirmed At: {{ userProfile.confirmed_at }}</p>
    </div>
    <p v-else>No user profile available.</p>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  data() {
    return {
      userProfile: null, // Initialize as an object
    };
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
        isAuthenticated() {
      // Check if the user is authenticated based on the presence of authToken
      return !!localStorage.getItem('authToken');
    },
    fetchUserProfile() {
      // Get the authentication token from localStorage
      const authToken = localStorage.getItem('authToken');

      // Make the GET request with the authentication token in the headers
      axios
        .get(`${API_BASE_URL}/profile`, {
          headers: { 'authToken': authToken }
        })
        .then((response) => {
          this.userProfile = response.data; // Assign the response directly to userProfile
        })
        .catch((error) => {
          console.error('Error fetching user profile:', error);
        });
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-card {
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
/* Adding new styles for the current component */
nav {
  background-color: #007bff;
  padding: 10px;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav h1 {
  margin: 0;
}

nav a {
  color: #fff;
  text-decoration: none;
  margin-right: 10px;
}

.search-container {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-right: 10px; /* Adjust margin as needed */
}

input[type="text"] {
  padding: 5px;
  margin-right: 5px; /* Adjust margin as needed */
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

li {
  display: inline;
  margin-right: 10px;
}


.error-message {
  color: #FF0000;
  margin-top: 10px;
}

.book-container {
  max-width: 800px;
  margin: 20px auto;
}

.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.book-card {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}
/* User profile component styles */
.profile-card {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}

/* Login component styles */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-card {
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* Book component styles */
.book-container {
  max-width: 800px;
  margin: 20px auto;
}

.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.book-card {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}
</style>
