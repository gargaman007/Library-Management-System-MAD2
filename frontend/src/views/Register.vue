<template>
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
  <div class="register-container">
    <div class="register-card">
      <h2>Register</h2>
      <form @submit.prevent="registerUser">
        <div class="form-group">
          <label>Email:</label>
          <input type="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label>Password:</label>
          <input type="password" v-model="password" required />
        </div>
        <button type="submit">Register</button>
      </form>
      <p v-if="message" class="error-message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  data() {
    return {
      email: '',
      password: '',
      message: ''
    };
  },
  methods: {
        isAuthenticated() {
      // Check if the user is authenticated based on the presence of authToken
      return !!localStorage.getItem('authToken');
    },
    registerUser() {
      axios.post(`${API_BASE_URL}/register`, {
        email: this.email,
        password: this.password,
      })
        .then(response => {
          this.message = response.data.message;
          this.email = '';
          this.password = '';
          // redirect to the login page or show a success message
          this.$router.push('/login');
        })
        .catch(error => {
          if (error.response && error.response.data.message) {
            this.message = error.response.data.message;
          } else {
            this.message = error.message;
          }
        });
    },
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.register-card {
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

.error-message {
  color: #FF0000;
  margin-top: 10px;
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
</style>
