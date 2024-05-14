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
    <!-- Show all books -->
    <div>
      <h2>All Books</h2>
      <div v-if="books.length > 0">
        <table class="book-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Section</th>
              <th>Author</th>
              <th>Description</th>
              <th>Content</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books" :key="book.id">
              <td>{{ book.name }}</td>
              <td>{{ book.section_name }}</td>
              <td>{{ book.author }}</td>
              <td>{{ book.description }}</td>
              <td>{{ book.content }}</td>
              <td>{{ book.status }}</td>
              <td>
                <button @click="editBook(book.id)">Edit</button>
                <button @click="deleteBook(book.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>No books available.</p>
    </div>

    <!-- Add new book form -->
    <div>
      <h2>Add New Book</h2>
      <form @submit.prevent="addBook">
        <div class="form-group">
          <label>Name:</label>
          <input type="text" v-model="newBook.name" required />
        </div>
        <div class="form-group">
          <label>Category:</label>
          <select v-model="newBook.section_id" required>
            <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Author:</label>
          <input type="text" v-model="newBook.author" required />
        </div>
        <div class="form-group">
          <label>Description:</label>
          <textarea v-model="newBook.description" required></textarea>
        </div>
                <div class="form-group">
          <label>Content:</label>
          <textarea v-model="newBook.content" required></textarea>
        </div>
        <div class="form-group">
          <label>Status:</label>
          <select v-model="newBook.status" required>
            <option value="available">Available</option>
            <option value="not_available">Not Available</option>
          </select>
        </div>
        <button type="submit">Add Book</button>
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
      books: [],
      sections: [],
      newBook: {
        name: '',
        section_id: null,
        author: '',
        description: '',
        content:'',
        status: 'available',
      },
    };
  },
  mounted() {
    this.fetchAllBooks();
    this.fetchAllSections();
  },
  methods: {
    fetchAllBooks() {
      const authToken = localStorage.getItem('authToken');
      axios.get(`${API_BASE_URL}/books`, { headers: { 'authToken': authToken } })
        .then(response => {
          this.books = response.data;
        })
        .catch(error => {
          console.error('Error fetching books:', error);
        });
    },
    fetchAllSections() {
      const authToken = localStorage.getItem('authToken');
      axios.get(`${API_BASE_URL}/section`, { headers: { 'authToken': authToken } })
        .then(response => {
          this.sections = response.data;
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
    editBook(bookId) {
      this.$router.push({ name: 'editbook', params: { id: bookId } });
    },
    deleteBook(bookId) {
      const authToken = localStorage.getItem('authToken');
      axios.delete(`${API_BASE_URL}/book/${bookId}`, { headers: { 'authToken': authToken } })
        .then(response => {
          console.log('Book deleted:', response.data.message);
          this.fetchAllBooks();
        })
        .catch(error => {
          console.error('Error deleting book:', error);
        });
    },
addBook() {
  const authToken = localStorage.getItem('authToken');
  const formData = new FormData();
  formData.append('name', this.newBook.name);
  formData.append('author', this.newBook.author);
  formData.append('description', this.newBook.description);
  formData.append('content', this.newBook.content);  // Change to content_url

  axios.post(`${API_BASE_URL}/book/${this.newBook.section_id}`, formData, { headers: { 'authToken': authToken } })
    .then(response => {
      console.log('Book added:', response.data.message);
      this.fetchAllBooks();
      this.newBook = {
        name: '',
        section_id: null,
        author: '',
        description: '',
        content: '',  // Clear the content field after adding the book
        status: 'available',
      };
    })
    .catch(error => {
      console.error('Error adding book:', error);
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

