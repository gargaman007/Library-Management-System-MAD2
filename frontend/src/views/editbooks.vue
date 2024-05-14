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
  <div class="complete-product-container">
    <h2>Edit Book</h2>

    <div class="edit-product-form">
   <form @submit.prevent="editBook">
    <div class="form-group">
      <label>Name:</label>
      <input type="text" v-model="editedBook.name" required />
    </div>
    <div class="form-group">
      <label>Section:</label>
      <select v-model="editedBook.section_id" required>
        <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
      </select>
    </div>
    <div class="form-group">
      <label>Author:</label>
      <input type="text" v-model="editedBook.author" required />
    </div>
    <div class="form-group">
      <label>Description:</label>
      <textarea v-model="editedBook.description" required></textarea>
    </div>
    <div class="form-group">
      <label>Content:</label>
      <textarea v-model="editedBook.content" required></textarea>
    </div>
    <div class="form-group">
      <label>Status:</label>
      <select v-model="editedBook.status" required>
        <option value="available">Available</option>
        <option value="not_available">Not Available</option>
      </select>
    </div>
    <button type="submit">Save Changes</button>
    <button @click="deleteBook">Delete Book</button>
  </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export default {
  data() {
    return {
      editedBook: {
        name: '',
        section_id: null,
        author: '',
        description: '',
        content: '',
        status: 'available',
      },
      sections: [],
    };
  },
  mounted() {
    // Fetch book details and sections when the component is mounted
    this.fetchBookDetails();
    this.fetchAllSections();
  },
  methods: {
    fetchBookDetails() {
      const authToken = localStorage.getItem('authToken');
      const bookId = this.$route.params.id;

      axios.get(`${API_BASE_URL}/api/book/${bookId}`, { headers: { 'authToken': authToken } })
        .then(response => {
          this.editedBook = response.data;
        })
        .catch(error => {
          console.error('Error fetching book details:', error);
        });
    },
    fetchAllSections() {
      const authToken = localStorage.getItem('authToken');

      axios.get(`${API_BASE_URL}/api/section`, { headers: { 'authToken': authToken } })
        .then(response => {
          this.sections = response.data;
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
    editBook() {
  const authToken = localStorage.getItem('authToken');
  const formData = new FormData();

  // Append each field of the edited book to the FormData object
  formData.append('name', this.editedBook.name);
  formData.append('section_id', this.editedBook.section_id);
  formData.append('author', this.editedBook.author);
  formData.append('description', this.editedBook.description);
  formData.append('content', this.editedBook.content);
  formData.append('status', this.editedBook.status);

  const bookId = this.$route.params.id;

  axios.patch(
    `${API_BASE_URL}/api/book/${bookId}`,
    formData, // Send FormData instead of spread operator
    {
      headers: {
        'authToken': authToken,
        'Content-Type': 'multipart/form-data',
      },
    }
  )
    .then(response => {
      console.log('Book updated:', response.data.message);
      this.$router.push({ name: 'manage-books' });
    })
    .catch(error => {
      console.error('Error updating book:', error);
    });
},



    deleteBook() {
      const authToken = localStorage.getItem('authToken');
      const bookId = this.$route.params.id;

      axios.delete(`${API_BASE_URL}/api/book/${bookId}`, { headers: { 'authToken': authToken } })
        .then(response => {
          console.log('Book deleted:', response.data.message);
          // Redirect to the book listing page after deletion
          this.$router.push({ name: 'manage-books' });
        })
        .catch(error => {
          console.error('Error deleting book:', error);
        });
    },
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

button {
  padding: 5px 10px;
  margin-right: 5px;
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
input {
  width: 100%;
  padding: 5px;
  margin-bottom: 5px; /* Add margin-bottom to textarea */
}
form {
  margin-bottom: 20px; /* Add margin to separate the form from other elements */
}

.form-group {
  margin-bottom: 10px; /* Add margin between form groups */
}

textarea {
  width: 100%;
  padding: 5px;
  margin-bottom: 5px; /* Add margin-bottom to textarea */
}

button[type="submit"] {
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}
</style>

