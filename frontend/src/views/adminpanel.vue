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
  <div class="admin-panel">
    <h1>Librarian Panel</h1>

    <!-- Total Issue Quantity -->
    <div class="card">
      <h2>Total Issue Quantity</h2>
      <p>{{ issueQuantity || 'Loading...' }}</p>
    </div>

    <!-- Number of Available Books -->
    <div class="card">
      <h2>Available Books</h2>
      <p>{{ availableBooks || 'Loading...' }}</p>
    </div>

    <!-- Total Number of Books -->
    <div class="card">
      <h2>Total Books</h2>
      <p>{{ totalBooks || 'Loading...' }}</p>
    </div>

    <!-- Total Categories -->
    <div class="card">
      <h2>Total Categories</h2>
      <p>{{ totalCategories || 'Loading...' }}</p>
    </div>

    <!-- CSV Export Buttons -->
    <div class="csv-export">
      <button @click="exportCSV('export-issues-csv')">Export Issues CSV</button>
      <button @click="exportCSV('export-feedbacks-csv')">Export Feedbacks CSV</button>
      <button @click="exportCSV('export-user-activities-csv')">Export User Activities CSV</button>
      <button @click="exportCSV('export-books-csv')">Export Books CSV</button>
      <button @click="exportCSV('export-sections-csv')">Export Sections CSV</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export default {
  data() {
    return {
      issueQuantity: null,
      availableBooks: null,
      totalBooks: null,
      totalCategories: null,
    };
  },
  methods: {
    async fetchData() {
      try {
        const authToken = localStorage.getItem('authToken');
        const response = await axios.get(`${API_BASE_URL}/admin-dashboard`, { headers: { 'authToken': authToken } });
        const { issueQuantity, availableBooks, totalBooks, totalCategories } = response.data;
        this.issueQuantity = issueQuantity;
        this.availableBooks = availableBooks;
        this.totalBooks = totalBooks;
        this.totalCategories = totalCategories;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    async exportCSV(exportType) {
    try {
        const authToken = localStorage.getItem('authToken');
        const response = await axios.get(`${API_BASE_URL}/export/${exportType}`, { headers: { 'authToken': authToken } });

        // Assuming the response data is a string of CSV content
        const csvContent = response.data;

        // Perform the async download
        this.downloadCSV(csvContent, `${exportType}.csv`);
    } catch (error) {
        console.error('Error exporting CSV:', error);
    }
    },



    downloadCSV(data, filename) {
    // Convert JSON data to CSV format
    const csvContent = this.convertJSONToCSV(data);

    // Create a Blob with the CSV content
    const blob = new Blob([csvContent], { type: 'text/csv' });

    // Create a link element to trigger the download
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;

    // Append the link to the DOM, trigger the download, and remove the link
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    },

convertJSONToCSV(jsonData) {
  // Extract keys from the first row of the JSON data
  const keys = Object.keys(jsonData[0]);

  // Create an array to hold CSV rows
  const rows = [];

  // Add the header row
  rows.push(keys.map(key => `"${key}"`).join(','));

  // Add data rows
  jsonData.forEach((row) => {
    const values = keys.map((key) => `"${row[key]}"`);
    rows.push(values.join(','));
  });

  // Join rows with newline characters to form the complete CSV content
  return rows.join('\n');
}



  },
  mounted() {
    this.fetchData();
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
