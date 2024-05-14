<template>
  <div>
    <!-- Navigation Bar -->
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

    <!-- Product Container -->
    <div class="index-container">
      <h2>Books in Section: {{ sectionName }}</h2>
      <div v-if="sectionBooks.length > 0" class="product-container">
        <div v-for="book in sectionBooks" :key="book.id" class="product-card">
          <h3>{{ book.name }}</h3>
          <p>Author: {{ book.author }}</p>
          <p>Description: {{ book.description }}</p>
          <p>Section: {{ book.section_name }}</p>
          <p>Status: {{ book.status }}</p>
          <!-- Request button -->
          <button
            @click="requestBook(book.id)"
            :disabled="book.status !== 'available'"
          >
            Request
          </button>
        </div>
      </div>
      <p v-else>No Books available in this Section at the moment.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  data() {
    return {
      sectionBooks: [],
      sectionName: '', // To store the selected category name
      searchQuery: '',
    };
  },
  computed: {
    isLoggedIn() {
      // Check if the auth token is present to determine if the user is logged in
      return !!localStorage.getItem('authToken');
    },
  },
  mounted() {
    // Fetch section books when the component is mounted
    this.fetchSectionBooks();
  },
  methods: {
        isAuthenticated() {
      // Check if the user is authenticated based on the presence of authToken
      return !!localStorage.getItem('authToken');
    },
    fetchSectionBooks() {
      // Get the sectionId from the route params
      const sectionId = this.$route.params.sectionId;

      // Fetch books based on the selected section using the provided API
      axios
        .get(`${API_BASE_URL}/section/${sectionId}/books`)
        .then((response) => {
          this.sectionBooks = response.data;
          // Assuming the response format is similar to the one in your API
          // Update the section name as needed
          this.sectionName = response.data.length > 0 ? response.data[0].section_name : 'Unknown Section';
        })
        .catch((error) => {
          console.error('Error fetching section books:', error);
        });
    },
    requestBook(bookId) {
      // Logic for requesting a book goes here
    },
  },
};
</script>

<style scoped>
/* Your component styles go here */

/* Reusing styles from the previous component */
.index-container {
  max-width: 800px;
  margin: 0 auto;
}

.product-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.product-card {
  width: calc(33.33% - 10px);
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  padding: 8px;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
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
