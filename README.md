# Farm-ways-backend-
Bookstore API Documentation
Base URL
The base URL for all endpoints is: http://127.0.0.1:5000

Authentication
To access protected endpoints, you need to obtain an access token by sending a POST request to the /login endpoint with valid credentials.

Login
Endpoint: /login
Method: POST
Request Body:
json


{
    "username": "your_username",
    "password": "your_password"
}
Response:
access_token: JWT token for authentication
Endpoints
Add Book
Endpoint: /add_book_protected
Method: POST
Headers: Authorization: Bearer <access_token>
Request Body:
json


{
    "title": "Book Title",
    "author": "Author Name",
    "isbn": "ISBN Number",
    "price": 12.99,
    "quantity": 10
}

Response:
Status Code:
201: Book added successfully
400: Book with this title or ISBN already exists
500: An error occurred while adding the book
Update Book
Endpoint: /update_book/<book_id>
Method: PUT
Headers: Authorization: Bearer <access_token>
Request Body:
json
C

{
    "title": "New Title",
    "author": "New Author",
    "isbn": "New ISBN",
    "price": 15.99,
    "quantity": 20
}

Response:
Status Code:
200: Book updated successfully
404: Book not found
Delete Book
Endpoint: /delete_book/<book_id>
Method: DELETE
Headers: Authorization: Bearer <access_token>
Response:
Status Code:
200: Book deleted successfully
404: Book not found
Get All Books
Endpoint: /get_all_books
Method: GET
Response:
JSON array containing details of all books
json
[
    {
        "id": 1,
        "title": "Book Title",
        "author": "Author Name",
        "isbn": "ISBN Number",
        "price": 12.99,
        "quantity": 10
    },
    {
        "id": 2,
        "title": "Another Book",
        "author": "Another Author",
        "isbn": "Another ISBN",
        "price": 19.99,
        "quantity": 15
    }
]
Get Book by ID
Endpoint: /get_book/<book_id>
Method: GET
Response:
Details of the book with the specified ID
json
Copy code
{
    "id": 1,
    "title": "Book Title",
    "author": "Author Name",
    "isbn": "ISBN Number",
    "price": 12.99,
    "quantity": 10
}
This documentation provides a clear overview of the available endpoints, their methods, request parameters, and expected responses, enabling users to effectively utilize the Bookstore API
OUTPUT:![image](https://github.com/vishnu810/Farm-ways-backend-/assets/83159673/b88790ff-c565-439a-945f-927c6b5408e3)
OUTPUT running unit test case:![image](https://github.com/vishnu810/Farm-ways-backend-/assets/83159673/8774723d-4ddc-498e-bb73-4d08b3db8a95)


