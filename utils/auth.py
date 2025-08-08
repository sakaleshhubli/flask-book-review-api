from utils.database import get_connection

def check_admin(user_id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    con.close()
    
    return result and result[0] == 'admin'