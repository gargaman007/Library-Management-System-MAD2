<template>
  <div>
    <!-- Navigation bar -->
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

    <!-- Display sections -->
    <div>
      <h2>Sections</h2>
      <div v-if="sections.length > 0" class="category-container">
        <button v-for="section in sections" :key="section.id" @click="navigateToSection(section.id)">
          <div class="section-info">
            <p class="section-name">{{ section.name }}</p>
            <p class="section-description">{{ section.description }}</p>
          </div>
        </button>
      </div>
      <p v-else>No Sections available at the moment.</p>
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
      searchQuery: '',
    };
  },
  mounted() {
    
    // Fetch sections when the component is mounted
    this.fetchSections();
  },
  methods: {
        isAuthenticated() {
      // Check if the user is authenticated based on the presence of authToken
      return !!localStorage.getItem('authToken');
    },
    fetchSections() {
      const authToken = localStorage.getItem('authToken');
      axios
        .get(`${API_BASE_URL}/section`, { headers: { 'authToken': authToken } })
        .then((response) => {
          this.sections = response.data;
        })
        .catch((error) => {
          console.error('Error fetching Sections:', error);
        });
    },
    navigateToSection(sectionId) {
      // Navigate to the section page for the selected section
      this.$router.push({ path: `/section/${sectionId}` });
    },
  },
};
</script>

<style scoped>
.category-container {
  display: flex;
  flex-wrap: wrap;
}

button {
  padding: 8px;
  margin: 8px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
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
