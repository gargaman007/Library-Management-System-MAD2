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
    <div>
      <!-- Show all issues -->
      <h2>All Issues</h2>
      <div v-for="issue in issues" :key="issue.id" class="issue-card">
        <p>User ID: {{ issue.user_id }}</p>
        <p>Book ID: {{ issue.book_id }}</p>
        <p>Issue Date: {{ issue.issue_date }}</p>
        <p>Due Date: {{ issue.due_date }}</p>
        <p>Status: {{ issue.status }}</p>
        <!-- Allow returning the book -->
        <button v-if="issue.status !== 'returned'" @click="returnBook(issue.id)">Return Book</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  data() {
    return {
      issues: [],
    };
  },
  mounted() {
    this.fetchIssues();
  },
  methods: {
    fetchIssues() {
      const authToken = localStorage.getItem('authToken');
      axios.get(`${API_BASE_URL}/issues`, { headers: { 'authToken': authToken } })
        .then(response => {
          this.issues = response.data;
        })
        .catch(error => {
          console.error('Error fetching issues:', error);
        });
    },
    returnBook(issueId) {
      const authToken = localStorage.getItem('authToken');
      axios.patch(
        `${API_BASE_URL}/issues/${issueId}`,
        { status: 'returned' },  // Set status to 'returned'
        { headers: { 'authToken': authToken } }
      )
        .then(response => {
          console.log('Book returned:', response.data.message);
          // Refresh the list of issues
          this.fetchIssues();
        })
        .catch(error => {
          console.error('Error returning book:', error);
        });
    },
  },
};
</script>

<style scoped>
/* Your component styles go here */
.issue-card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
}

.issue-card:hover {
  transform: translateY(-5px);
}

.issue-card p {
  margin-bottom: 15px;
  color: #555;
}

button {
  padding: 10px;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #218838;
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
