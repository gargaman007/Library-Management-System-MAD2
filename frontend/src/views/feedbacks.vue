<template>
  <div>
    <nav>
      <h1>Library Management System</h1>
      <router-link to="/admin">Home</router-link> |
      <router-link to="/manage-sections">Manage Sections</router-link> |
      <router-link to="/manage-books">Manage Books</router-link> |
      <router-link to="/manage-requests">Manage Requests</router-link> |
      <router-link to="/view-issued-books">View Issued Books</router-link> |
      <router-link to="/feedback">Feedback</router-link> | <!-- New link for Feedback -->
      <router-link to="/logout">Logout</router-link> |
      <router-link to="/register">Register</router-link> |
      <router-link to="/login">Login</router-link> |
    </nav>
    <div class="admin-panel">
      <h1>Librarian Panel</h1>
      <!-- Feedback list -->
      <div v-if="feedbackList.length > 0">
        <h2>Feedback List</h2>
        <ul>
          <li v-for="feedback in feedbackList" :key="feedback.id">
            <p><strong>Issue ID:</strong> {{ feedback.issue_id }}</p>
            <p><strong>User ID:</strong> {{ feedback.user_id }}</p>
            <p><strong>Feedback:</strong> {{ feedback.feedback }}</p>
          </li>
        </ul>
      </div>
      <p v-else>No feedback available.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  data() {
    return {
      feedbackList: [], // Store feedback data
      searchQuery: ''
    };
  },
  methods: {
    async fetchFeedback() {
      try {
        const authToken = localStorage.getItem('authToken');
        const response = await axios.get(`${API_BASE_URL}/all-feedback`, { headers: { 'authToken': authToken } });
        this.feedbackList = response.data;
      } catch (error) {
        console.error('Error fetching feedback:', error);
      }
    }
  },
  mounted() {
    this.fetchFeedback();
  }
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
</style>

