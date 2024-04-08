from flask import Flask, jsonify, request
from config_dev import DevConfig
from database import init_app, get_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(DevConfig)

# Initialize the database
init_app(app)

# GET route for retrieving all books
@app.route('/api/books/get', methods=['GET'])
def get_books():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    cursor.close()
    return jsonify(books)

# POST route for adding a new book
@app.route('/api/books/add', methods=['POST'])
def add_book():
    db = get_db()
    cursor = db.cursor()
    data = request.json
    title = data.get('title')
    author = data.get('author')
    year = data.get('year')  # Optional field
    if title is None or author is None:
        return jsonify({'error': 'Both "title" and "author" parameters are required.'}), 400
    cursor.execute("INSERT INTO book (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Book added', 'title': title, 'author': author, 'year': year}), 201

# POST route for updating the read status of a book
@app.route('/api/books/update', methods=['POST'])
def update_book_status():
    db = get_db()
    cursor = db.cursor()

    # Parse JSON data from request body
    data = request.json
    book_id = data.get('book_id')
    new_status = data.get('status')

    # Check if both 'book_id' and 'status' parameters are provided
    if book_id is None or new_status is None:
        return jsonify({'error': 'Both "book_id" and "status" parameters are required.'}), 400

    # Convert status to boolean
    new_status = bool(new_status)

    # Update the read status of the book
    cursor.execute("UPDATE book SET read_status = %s WHERE id = %s", (new_status, book_id))
    db.commit()
    cursor.close()

    return jsonify({'message': 'Book updated', 'book_id': book_id, 'status': new_status}), 200
@app.route('/api/books/delete', methods=['POST'])
def delete_book():
    # Get the book ID from the request JSON data
    data = request.json
    book_id = data.get('book_id')

    if book_id is None:
        return jsonify({'error': 'Missing book_id parameter in request body'}), 400

    # Delete the book from the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM book WHERE id = %s", (book_id,))
    db.commit()
    cursor.close()

    return jsonify({'message': 'Book deleted successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8097)

