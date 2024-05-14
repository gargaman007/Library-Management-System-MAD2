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
  <div class="edit-category-container">
    <h2>Edit Section</h2>

    <div v-if="section">
      <form @submit.prevent="saveChanges">
        <div class="form-group">
          <label>Name:</label>
          <input type="text" v-model="editedSection.name" required />
        </div>
        <div class="form-group">
          <label>Description:</label>
          <textarea v-model="editedSection.description" required></textarea>
        </div>
        <button type="submit">Save Changes</button>
      </form>
    </div>

    <p v-else>No section details available.</p>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  data() {
    return {
      section: null,
      editedSection: {
        name: '',
        description: '',
      },
    };
  },
  mounted() {
    const sectionId = this.$route.params.id;
    this.fetchSection(sectionId);
  },
  methods: {
    fetchSection(sectionId) {
      const authToken = localStorage.getItem('authToken');

      axios.get(`${API_BASE_URL}/section/${sectionId}`, { headers: { 'authToken': authToken } })
        .then(response => {
          this.section = response.data;
          this.editedSection = { ...this.section };
        })
        .catch(error => {
          console.error('Error fetching section details:', error);
        });
    },
    saveChanges() {
      const sectionId = this.$route.params.id;
      const authToken = localStorage.getItem('authToken');

      axios.patch(
        `${API_BASE_URL}/section/${sectionId}`,
        { ...this.editedSection },
        { headers: { 'authToken': authToken } }
      )
        .then(response => {
          console.log('Section updated:', response.data.message);
          this.$router.push('/manage-sections');
        })
        .catch(error => {
          console.error('Error updating section:', error);
        });
    },
  },
};
</script>

<style scoped>
/* Your component styles go here */
.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.section-card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
}

.section-card:hover {
  transform: translateY(-5px);
}

.section-card p {
  margin-bottom: 15px;
  color: #555;
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
