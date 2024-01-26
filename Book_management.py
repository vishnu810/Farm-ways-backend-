from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1234'  # Set the secret key
app.config['JWT_SECRET_KEY'] = '456'  # Set the JWT secret key
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Define your Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'isbn', 'price', 'quantity')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Route to add a book (protected by JWT)
@app.route('/add_book_protected', methods=['POST'])
@jwt_required()
def add_book_protected():
    try:
        data = request.get_json()

        new_book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            price=data['price'],
            quantity=data['quantity']
        )

        db.session.add(new_book)
        db.session.commit()

        return jsonify({"msg": "Book added successfully"}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Book with this title or ISBN already exists"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while adding the book"}), 500
    
from flask_jwt_extended import create_access_token

# Mock authentication route
@app.route('/login', methods=['POST'])
def login():
    # Replace this with actual user authentication logic
    username = request.json.get('username')
    password = request.json.get('password')

    # Example: Validate username and password
    if username == 'test1' and password == 'test2':
        # Create and return a JWT token
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401
from flask import jsonify

@app.route('/get_book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'price': book.price,
            'quantity': book.quantity
        }), 200
    else:
        return jsonify({'error': 'Book not found'}), 404
from flask import jsonify

@app.route('/get_all_books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'price': book.price,
            'quantity': book.quantity
        }
        book_list.append(book_data)
    return jsonify(book_list), 200

# Update Book Route
@app.route('/update_book/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        data = request.get_json()
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.isbn = data.get('isbn', book.isbn)
        book.price = data.get('price', book.price)
        book.quantity = data.get('quantity', book.quantity)
        db.session.commit()
        return jsonify({"message": "Book updated successfully"}), 200
    else:
        return jsonify({"error": "Book not found"}), 404

# Delete Book Route
@app.route('/delete_book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200
    else:
        return jsonify({"error": "Book not found"}), 404




# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
