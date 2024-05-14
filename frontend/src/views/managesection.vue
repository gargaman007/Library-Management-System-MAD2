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
    <!-- Show all sections -->
    <div>
      <h2>All Sections</h2>
      <div v-for="section in sections" :key="section.id" class="section-card">
        <p>Name: {{ section.name }}</p>
        <p>Description: {{ section.description }}</p>
        <p>Date Created: {{ section.date_created }}</p>
                <div>
          <button @click="editSection(section.id)">Edit</button>
          <button @click="deleteSection(section.id)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Add new section form -->
    <div>
      <h2>Add New Section</h2>
      <form @submit.prevent="addSection">
        <div class="form-group">
          <label>Section Name:</label>
          <input type="text" v-model="newSection.name" required />
        </div>
        <div class="form-group">
          <label>Section Description:</label>
          <textarea v-model="newSection.description" required></textarea>
        </div>
        <button type="submit">Add Section</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  data() {
    return {
      sections: [],
      newSection: {
        name: '',
        description: '',
      },
    };
  },
  mounted() {
    this.fetchSections();
  },
  methods: {
        editSection(sectionId) {
      // Redirect to the edit section page with the sectionId
      this.$router.push(`/edit-section/${sectionId}`);
    },

    // Method to Delete a Section
    deleteSection(sectionId) {
      // Confirm before deleting the section
      if (confirm('Are you sure you want to delete this section?')) {
        const authToken = localStorage.getItem('authToken');
        axios.delete(`${API_BASE_URL}/section/${sectionId}`, { headers: { 'authToken': authToken } })
          .then(response => {
            console.log('Section deleted:', response.data.message);
            // Fetch sections again after deletion
            this.fetchSections();
          })
          .catch(error => {
            console.error('Error deleting section:', error);
          });
      }
    },
    fetchSections() {
      const authToken = localStorage.getItem('authToken');
      axios.get(`${API_BASE_URL}/section`, { headers: { 'authToken': authToken } })
        .then(response => {
          this.sections = response.data;
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
addSection() {
  const authToken = localStorage.getItem('authToken');
  
  axios.post(
    `${API_BASE_URL}/section`,
    { ...this.newSection },
    { headers: { 'authToken': authToken } }
  )
    .then(response => {
      console.log('Section added:', response.data.message);
      this.fetchSections();
      this.newSection = { name: '', description: '' };
    })
    .catch(error => {
      console.error('Error adding section:', error);
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
