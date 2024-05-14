<template>
  <div>
  <H1> Library Management System </H1>
    <h2>Logout</h2>
    <p>Logging out...</p>
  </div>
</template>

<script>
export default {
  mounted() {
    // Clear all items from local storage
    localStorage.clear();

    // Redirect to the login page
    this.$router.push('/login');
  },
};
</script>

<style scoped>
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
