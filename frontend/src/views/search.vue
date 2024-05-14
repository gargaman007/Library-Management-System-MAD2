<template>
  <div>
    <!-- Navigation bar -->
    <nav>
      <h1>Library Management System</h1>
      <router-link to="/index">Home</router-link> |
      <router-link to="/section">Sections</router-link> |
      <router-link to="/userprofile">User Profile</router-link> |
      <router-link to="/userissues">User Issues</router-link> |
      <button v-if="!isAuthenticated()" @click="loginClicked">Login</button>
      <button v-if="!isAuthenticated()" @click="registerClicked">Register</button>
      <router-link v-if="isAuthenticated()" to="/logout">Logout</router-link> |
      

      

    </nav>
        <div class="search-container">
      <input v-model="searchQuery" type="text" placeholder="Search" />
      <button @click="searchBooks">Search</button>
    </div>
      <h2>Search Results</h2>
    <!-- Display search results -->
    <div class="search-container">
      <div v-if="searchResults.length > 0" class="book-container">
        <div v-for="result in searchResults" :key="result.book_id" class="book-card">
          <h3>{{ result.book_name }}</h3>
          <p>Author: {{ result.author }}</p>
          <p>Description: {{ result.description }}</p>
          <p>Section: {{ result.section_name }}</p>
                    <button
            @click="requestBook(result.book_id)"
            :disabled="result.status !== 'available'"
          >
            Request
          </button>
        </div>
      </div>
      <p v-else>No results found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      searchResults: [],
      searchQuery: '',
    };
  },
  methods: {
    searchBooks() {
      axios
        .get('http://localhost:5000/api/books/search', {
          params: { query: this.searchQuery },
        })
        .then(response => {
          this.searchResults = response.data;
        })
        .catch(error => {
          console.error('Error fetching search results:', error);
        });
    },        isAuthenticated() {
      // Check if the user is authenticated based on the presence of authToken
      return !!localStorage.getItem('authToken');
    },
    requestBook(bookId) {
  if (!this.isLoggedIn) {
    console.log('User not logged in. Redirect to login page.');
    this.$router.push('/login');
    return;
  }
  else {
  const authToken = localStorage.getItem('authToken');
  const userId = localStorage.getItem('userId');

  // Send request to backend to request the book with bookId
  axios
    .post(`${API_BASE_URL}/bookrequest`, { user_id: userId, book_id: bookId }, {
      headers: { 'authToken': authToken }
    })
    .then((response) => {
      console.log('Book request sent successfully:', response.data.message);
      // Optionally, update UI or show success message
    })
    .catch((error) => {
      console.error('Error requesting book:', error);
      // Handle error (e.g., show error message)
    });
  }
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
  justify-content: center;
  margin-top: 20px; /* Optional: Add margin for spacing */
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
