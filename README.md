# flask-book-review-api
A simple Flask API for managing book reviews using a MySQL backend.

### Database ERD

![App Screenshot](./db.png)

### Features

- **Book Management**: Add and view books (admin only for adding)
- **User Management**: Create and view users
- **Role-based Access**: Admin authentication for book operations
- **Anonymous Reviews**: Option to post reviews anonymously


### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sakaleshhubli/flask-book-review-api.git
   cd book-review-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL Database**
   - Create a MySQL database named `flaskapi`
   - Update database credentials as shown in picture
  
4. **Run the program**
   ```bash
     flask run --debug
     ```


## API Endpoints (CRUD Operations)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/` | Welcome message and instructions |
| GET    | `/tables` | List all database tables |
| GET    | `/tables/<table_name>` | View contents of specific table |
| GET    | `/books/` | View all books |
| GET    | `/users/` | View all users |
| GET    | `/reviews/` | View all reviews |
| POST   | `/users/` | Create a new user |
| POST   | `/books/` | Add a new book (admin only) |
| POST   | `/reviews/` | Add a new review |
| PUT    | `/users/<user_id>` | Update details of a specific user |
| PUT    | `/books/<book_id>` | Update details of a specific book |
| PUT    | `/reviews/<review_id>` | Update a specific review |
| DELETE | `/users/<user_id>` | Delete a specific user |
| DELETE | `/books/<book_id>` | Delete a specific book |
| DELETE | `/reviews/<review_id>` | Delete a specific review |



The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (missing required fields)
- `403`: Forbidden (insufficient permissions)
