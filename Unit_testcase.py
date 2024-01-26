import unittest
import json
from Book_management import app, db, Book

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_book(self):
        # Test adding a new book
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "1234567890123",
            "price": 19.99,
            "quantity": 10
        }
        response = self.app.post('/add_book_protected',
                                 json=book_data,
                                 headers={'Content-Type': 'application/json'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['msg'], 'Book added successfully')

    def test_get_book(self):
        # Test getting a specific book
        book = Book(title="Test Book", author="Test Author", isbn="1234567890123", price=19.99, quantity=10)
        with app.app_context():
            db.session.add(book)
            db.session.commit()
            book_id = book.id

        response = self.app.get(f'/get_book/{book_id}')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], 'Test Book')

    def test_update_book(self):
        # Test updating a book
        book = Book(title="Test Book", author="Test Author", isbn="1234567890123", price=19.99, quantity=10)
        with app.app_context():
            db.session.add(book)
            db.session.commit()
            book_id = book.id

        updated_data = {
            "title": "Updated Test Book",
            "author": "Updated Test Author",
            "isbn": "1234567890123",
            "price": 29.99,
            "quantity": 20
        }
        response = self.app.put(f'/update_book/{book_id}',
                                json=updated_data,
                                headers={'Content-Type': 'application/json'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Book updated successfully')

    def test_delete_book(self):
        # Test deleting a book
        book = Book(title="Test Book", author="Test Author", isbn="1234567890123", price=19.99, quantity=10)
        with app.app_context():
            db.session.add(book)
            db.session.commit()
            book_id = book.id

        response = self.app.delete(f'/delete_book/{book_id}')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Book deleted successfully')

    def test_get_all_books(self):
        # Test getting all books
        book1 = Book(title="Book 1", author="Author 1", isbn="1111111111111", price=10.99, quantity=5)
        book2 = Book(title="Book 2", author="Author 2", isbn="2222222222222", price=15.99, quantity=8)
        with app.app_context():
            db.session.add_all([book1, book2])
            db.session.commit()

        response = self.app.get('/get_all_books')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], 'Book 1')
        self.assertEqual(data[1]['title'], 'Book 2')

if __name__ == '__main__':
    unittest.main()
