<template>
 <div class="container">
    <h1 class="mt-4">Book List</h1>

    <!-- Menu for Discover New Book -->
    <div class="dropdown" @mouseover="showDropdown = true" @mouseleave="hideDropdown">
      <button class="btn btn-secondary" type="button" id="discoverMenu" :aria-expanded="showDropdown" aria-haspopup="true">
        Discover New Book
      </button>
      <div class="dropdown-menu" :class="{ 'show': showDropdown }" aria-labelledby="discoverMenu" @mouseover="showDropdown = true" @mouseleave="hideDropdown">
        <a class="dropdown-item" href="https://www.nytimes.com/section/books/review" target="_blank">New York Times</a>
        <a class="dropdown-item" href="https://book.douban.com/" target="_blank">Douban</a>
        <a class="dropdown-item" href="https://www.goodreads.com/" target="_blank">Goodreads</a>
      </div>
    </div>


    <!-- Form to add a new book -->
    <form @submit.prevent="addBook" class="mb-4">
      <div class="form-group">
        <label for="title">Title:</label>
        <input type="text" id="title" class="form-control" v-model="newBook.title" required>
      </div>
      <div class="form-group">
        <label for="author">Author:</label>
        <input type="text" id="author" class="form-control" v-model="newBook.author">
      </div>
  <div class="form-group">
    <label for="year">Year:</label>
    <input type="text" id="year" class="form-control" ref="yearPicker">
  </div>
      <button type="submit" class="btn btn-primary">Add Book</button>
    </form>

    <hr>

    <!-- List of books -->
     <ul class="list-group">
      <li v-for="book in books" :key="book.id" class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <span class="font-weight-bold text-lg">{{ book.title }}</span>
          <span v-if="book.author" class="author-text"> by {{ book.author }}</span>
          <span v-else class="author-text"></span>
          <div>
            <button @click="updateStatus(book.id, !book.read_status)" class="btn btn-sm btn-info mr-2">
              {{ book.read_status ? 'Mark as Unread' : 'Mark as Read' }}
            </button>
            <button @click="deleteBook(book.id)" class="btn btn-sm btn-danger">Delete</button>
          </div>
        </div>
      </li>
    </ul>
</div>
</template>

<script>
import backendConfig from '@/config';
import $ from 'jquery'; // Import jQuery
import 'bootstrap-datepicker'; // Import Bootstrap Datepicker
import 'bootstrap-datepicker/dist/css/bootstrap-datepicker.min.css'; // Import Bootstrap Datepicker CSS


export default {
  data() {
    return {
      showDropdown: false,
      books: [],
      newBook: { title: '', author: '' }
    };
  },
  mounted() {
    // Fetch initial list of books
    this.getBooks();
    $(this.$refs.yearPicker).datepicker({
      format: 'yyyy',
      viewMode: 'years',
      minViewMode: 'years',
      autoclose: true
    });
  },
  methods: {
    hideDropdown() {
      this.showDropdown = false;
    },
    // Fetch all books from backend
    getBooks() {
      fetch(`${backendConfig.baseUrl}/api/books/get`)
        .then(response => response.json())
        .then(data => {
          this.books = data;
        })
        .catch(error => {
          console.error('Error fetching books:', error);
        });
    },
    // Add a new book
    addBook() {
      fetch(`${backendConfig.baseUrl}/api/books/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.newBook)
      })
      .then(response => response.json())
      .then(data => {
        console.log('Book added:', data);
        this.books.push(data);
        // Reset the form fields
        this.newBook = { title: '', author: '' };
      })
      .catch(error => {
        console.error('Error adding book:', error);
      });
    },
    // Update the read status of a book
    updateStatus(bookId, newStatus) {
      fetch(`${backendConfig.baseUrl}/api/books/update`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ book_id: bookId, status: newStatus })
      })
      .then(response => response.json())
      .then(data => {
        console.log('Book status updated:', data);
        // Find the index of the book in this.books array
        const index = this.books.findIndex(book => book.id === bookId);
        // Update the read status of the book in this.books array
        if (index !== -1) {
          this.books[index].read = newStatus;
        }
      })
      .catch(error => {
        console.error('Error updating book status:', error);
      });
    },

    deleteBook(bookId) {
      fetch(`${backendConfig.baseUrl}/api/books/delete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ book_id: bookId })
      })
      .then(response => {
        if (response.ok) {
          console.log('Book deleted successfully');
          // Remove the deleted book from this.books array
          this.books = this.books.filter(book => book.id !== bookId);
        } else {
          console.error('Error deleting book:', response.statusText);
        }
      })
      .catch(error => {
        console.error('Error deleting book:', error);
      });
    }
  }
};
</script>

<style>
.text-lg {
  font-size: 1.25rem; /* Adjust the font size as needed */
}

.author-text {
  font-style: italic; /* Apply italic style to the "by" text */
}
.bootstrap-datepicker {
  font-size: 14px; /* Adjust font size as needed */
}

.bootstrap-datepicker-dropdown {
  border: none; /* Remove border */
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1); /* Add shadow */
}

.bootstrap-datepicker-dropdown.datepicker-orient-bottom:before,
.bootstrap-datepicker-dropdown.datepicker-orient-top:before {
  border-bottom-color: #f8f9fa; /* Background color */
}

.bootstrap-datepicker .datepicker-years .datepicker-switch {
  color: #495057; /* Text color */
}

.bootstrap-datepicker .datepicker-years .datepicker-switch:hover {
  background-color: #f8f9fa; /* Hover background color */
}

.bootstrap-datepicker .datepicker-years tbody span {
  display: inline-block;
  width: 45px; /* Adjust width as needed */
  height: 45px; /* Adjust height as needed */
  line-height: 45px; /* Center text vertically */
  text-align: center; /* Center text horizontally */
  cursor: pointer;
}

.bootstrap-datepicker .datepicker-years tbody span:hover {
  background-color: #f8f9fa; /* Hover background color */
  border-radius: 50%; /* Rounded corners */
}
/* Add custom styles here if needed */
</style>

