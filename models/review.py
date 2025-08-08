from utils.database import get_connection

class ReviewModel:
    @staticmethod
    def create_review(user_id, book_id, rating, comment='', anonymous=False):
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO reviews (user_id, book_id, rating, comment, anonymous) 
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, book_id, rating, comment, anonymous))
        con.commit()
        review_id = cursor.lastrowid
        cursor.close()
        con.close()
        return review_id
    
    @staticmethod
    def update_review(review_id, rating, comment, anonymous):
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("""
            UPDATE reviews SET rating = %s, comment = %s, anonymous = %s 
            WHERE review_id = %s
        """, (rating, comment, anonymous, review_id))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        con.close()
        return rows_affected > 0
    
    @staticmethod
    def delete_review(review_id):
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        con.close()
        return rows_affected > 0