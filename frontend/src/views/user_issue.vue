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
    <h2>User Issues</h2>
    <div v-if="userIssues.length > 0">
      <div v-for="issue in userIssues" :key="issue.id" class="issue-card">
        <h3>Issue ID: {{ issue.id }}</h3>
        <p>User ID: {{ issue.user_id }}</p>
        <p>Book ID: {{ issue.book_id }}</p>
        <p>Issue Date: {{ issue.issue_date }}</p>
        <p>Due Date: {{ issue.due_date }}</p>
        <p>Status: {{ issue.status }}</p>
        <!-- Display book content if available and status is active -->
<p v-if="issue.book_content && issue.status === 'active'">Book Content: {{ issue.book_content }}</p>
        <button v-if="issue.status === 'returned'" @click="addFeedback(issue.id)">Add Feedback</button>
<button v-if="issue.status === 'active'" @click="returnBook(issue.id)">Return Book</button>

      </div>
    </div>
    <p v-else>No issues available.</p>
  </div>
  <div class="modal" v-show="isOpen">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h3>Existing Feedback:</h3>
      <ul v-if="existingFeedback.length > 0">
        <li v-for="fb in existingFeedback" :key="fb.id">{{ fb.feedback }}</li>
      </ul>
      <h3>Add New Feedback:</h3>
      <textarea v-model="feedbackText" placeholder="Enter your feedback"></textarea>
      <button @click="submitFeedback">Submit</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
    props: {
    existingFeedback: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      userIssues: [],
      isOpen: false,
      feedbackText: ''
    };
  },
  mounted() {
    this.fetchUserIssues();
  },
  methods: {
    addFeedback(issueId) {
  const authToken = localStorage.getItem('authToken');
  const feedbackText = prompt('Enter your feedback:');
  if (!feedbackText) return; // If the user cancels the prompt
  axios
    .post(`${API_BASE_URL}/feedback`, { issue_id: issueId, feedback: feedbackText }, {
      headers: { 'authToken': authToken }
    })
    .then(response => {
      console.log('Feedback added successfully:', response.data.message);
      // Refresh user issues after adding feedback
      this.fetchUserIssues();
    })
    .catch(error => {
      console.error('Error adding feedback:', error);
    });
},
openModal() {
      this.isOpen = true;
    },
    closeModal() {
      this.isOpen = false;
    },
    submitFeedback() {
      this.$emit('submit', this.feedbackText);
      this.isOpen = false;
    },
        isAuthenticated() {
      // Check if the user is authenticated based on the presence of authToken
      return !!localStorage.getItem('authToken');
    },
    fetchUserIssues() {
      // Get the authentication token from localStorage
      const authToken = localStorage.getItem('authToken');

      // Make the GET request with the authentication token in the headers
      axios
        .get(`${API_BASE_URL}/userissues`, {
          headers: { 'authToken': authToken }
        })
        .then((response) => {
          this.userIssues = response.data;
        })
        .catch((error) => {
          console.error('Error fetching user issues:', error);
        });
    },
    returnBook(issueId) {
      // Get the authentication token from localStorage
      const authToken = localStorage.getItem('authToken');

      // Make the PATCH request to mark the issue as returned
      axios
        .patch(`${API_BASE_URL}/issues/${issueId}`, { status: 'returned' }, {
          headers: { 'authToken': authToken }
        })
        .then((response) => {
          console.log('Book returned successfully:', response.data.message);
          // Refresh user issues after returning the book
          this.fetchUserIssues();
        })
        .catch((error) => {
          console.error('Error returning book:', error);
        });
    },
  },
};
</script>

<style scoped>
.issue-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

button {
  padding: 5px 10px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
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
