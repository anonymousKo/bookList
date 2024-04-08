<template>
  <div id="app">
    <header>
      <!-- Header content -->
      <h1>My Bookstore</h1>
    </header>

    <main>
      <!-- Main content -->
      <BookList />
    </main>

    <footer>
      <!-- Footer content -->
      <p>&copy; 2024 My Bookstore</p>
    </footer>
  </div>
</template>

<script>
import BookList from './components/BookList.vue';

export default {
  components: {
    BookList
  }
};
</script>

<style>
/* Add global styles here if needed */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}
header {
  background-color: #333;
  color: #fff;
  padding: 20px;
  text-align: center;
}
footer {
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  text-align: center;
}
</style>

