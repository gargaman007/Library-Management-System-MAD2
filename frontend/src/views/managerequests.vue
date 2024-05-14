<template>
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
    <!-- Show all book requests for admin and librarian -->
    <div>
      <h2>All Book Requests</h2>
      <div v-for="request in requests" :key="request.id" class="book-request-card">
        <p>User ID: {{ request.user_id }}</p>
        <p>Book ID: {{ request.book_id }}</p>
        <p>Status: {{ request.status }}</p>
        <!-- Admin and librarian actions -->
        <div>
          <!-- Conditionally render buttons based on the status -->
          <button v-if="request.status === 'pending'" @click="acceptRequest(request.id)">Accept</button>
          <button v-if="request.status === 'pending'" @click="rejectRequest(request.id)">Reject</button>
        </div>
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
      requests: [],
    };
  },
  computed: {
    isAuthorized() {
      // Check if the user has librarian or admin role
      const userRole = localStorage.getItem('userRole');
      return userRole === 'librarian' || userRole === 'admin';
    },
  },
  mounted() {
    if (this.isAuthorized) {
      this.fetchRequests();
    }
  },
  methods: {
    fetchRequests() {
      const authToken = localStorage.getItem('authToken');

      axios.get(`${API_BASE_URL}/all-book-requests`, { headers: { 'authToken': authToken } })
        .then(response => {
          this.requests = response.data;
        })
        .catch(error => {
          console.error('Error fetching book requests:', error);
        });
    },
    acceptRequest(requestId) {
      const authToken = localStorage.getItem('authToken');

      axios.patch(
        `${API_BASE_URL}/update-book-request/${requestId}`,
        { status: 'accepted' },
        { headers: { 'authToken': authToken } }
      )
        .then(response => {
          console.log('Book request accepted:', response.data.message);
          // Refresh the list of book requests
          this.fetchRequests();
        })
        .catch(error => {
          console.error('Error accepting book request:', error);
        });
    },
    rejectRequest(requestId) {
      const authToken = localStorage.getItem('authToken');

      axios.patch(
        `${API_BASE_URL}/update-book-request/${requestId}`,
        { status: 'rejected' },
        { headers: { 'authToken': authToken } }
      )
        .then(response => {
          console.log('Book request rejected:', response.data.message);
          // Refresh the list of book requests
          this.fetchRequests();
        })
        .catch(error => {
          console.error('Error rejecting book request:', error);
        });
    },
  },
};
</script>

<style scoped>
/* Your component styles go here */
.book-request-card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
}

.book-request-card:hover {
  transform: translateY(-5px);
}

.book-request-card p {
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
