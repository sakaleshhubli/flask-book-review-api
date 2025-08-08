from utils.database import get_connection

class BookModel:
    @staticmethod
    def create_book(title, author, isbn=None, published_year=None, average_rating=None):
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, isbn, published_year, average_rating) 
            VALUES (%s, %s, %s, %s, %s)
        """, (title, author, isbn, published_year, average_rating))
        con.commit()
        book_id = cursor.lastrowid
        cursor.close()
        con.close()
        return book_id
    
    @staticmethod
    def update_book(book_id, title, author, isbn, published_year, average_rating):
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("""
            UPDATE books SET title = %s, author = %s, isbn = %s, 
            published_year = %s, average_rating = %s WHERE book_id = %s
        """, (title, author, isbn, published_year, average_rating, book_id))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        con.close()
        return rows_affected > 0
    
    @staticmethod
    def delete_book(book_id):
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        con.close()
        return rows_affected > 0
