# from flask_mysqldb import MySQL, MySQLdb
# from werkzeug.security import generate_password_hash, check_password_hash
# from dotenv import load_dotenv
# from flask import request
# import os
# import json
# from typing import Dict, Optional, Tuple

# load_dotenv()


# class DatabaseConfig:
    
#     def __init__(self):
#         self.MYSQL_HOST = os.getenv("DBH", "localhost")
#         self.MYSQL_USER = os.getenv("DBU", "root")
#         self.MYSQL_PASSWORD = os.getenv("DBP", "")
#         self.MYSQL_DB = os.getenv("DBN", "sports_db")
#         self.SECRET_KEY = os.getenv("SCRTKEY", "your-secret-key-change-this")

# db_config = DatabaseConfig()

# def init_db(app):

#     try:
#         app.config['MYSQL_HOST'] = db_config.MYSQL_HOST
#         app.config['MYSQL_USER'] = db_config.MYSQL_USER
#         app.config['MYSQL_PASSWORD'] = db_config.MYSQL_PASSWORD
#         app.config['MYSQL_DB'] = db_config.MYSQL_DB
#         app.secret_key = db_config.SECRET_KEY
        

#         mysql = MySQL(app)
#         return mysql
#     except Exception as e:
#         print(f"Error configuring database: {e}")
#         raise

# def get_user_by_email(mysql: MySQL, email: str) -> Optional[Dict]:
#     try:
#         with mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cur:
#             cur.execute('SELECT * FROM users WHERE email = %s', (email.strip(),))
#             user = cur.fetchone()
#             return user
#     except MySQLdb.Error as e:
#         print(f"MySQL Error in get_user_by_email: {e}")
#         return None
#     except Exception as e:
#         print(f"Unexpected Error in get_user_by_email: {e}")
#         return None

# def verify_password(hashed_password: str, plain_password: str) -> bool:
#     try:
#         return check_password_hash(hashed_password, plain_password)
#     except Exception as e:
#         print(f"Error verifying password: {e}")
#         return False

# def parse_signup_json() -> Tuple[bool, Optional[Dict], str]:
#     try:
#         if not request.is_json:
#             content_type = request.content_type or 'unknown'
#             return False, None, f"Request must be JSON. Received content-type: {content_type}"
        
#         data = request.get_json(force=True, silent=False)
        
#         if data is None:
#             return False, None, "No JSON data provided or invalid JSON format"
        
#         if not isinstance(data, dict):
#             return False, None, "JSON data must be an object"
        
#         first_name = data.get('first_name', '').strip() if data.get('first_name') else ''
#         last_name = data.get('last_name', '').strip() if data.get('last_name') else ''
#         email = data.get('email', '').strip() if data.get('email') else ''
#         password = data.get('password', '').strip() if data.get('password') else ''
        
#         if not first_name:
#             return False, None, "First name is required"
#         if not last_name:
#             return False, None, "Last name is required"
#         if not email:
#             return False, None, "Email is required"
#         if '@' not in email or '.' not in email:
#             return False, None, "Invalid email format"
#         if not password:
#             return False, None, "Password is required"
#         if len(password) < 6:
#             return False, None, "Password must be at least 6 characters"
        
#         return True, {
#             'first_name': first_name,
#             'last_name': last_name,
#             'email': email,
#             'password': password
#         }, "Data parsed successfully"
#     except json.JSONDecodeError as e:
#         return False, None, f"Invalid JSON format: {str(e)}"
#     except Exception as e:
#         print(f"Error parsing signup JSON: {e}")
#         import traceback
#         traceback.print_exc()
#         return False, None, f"Error parsing request data: {str(e)}"

# def parse_login_json() -> Tuple[bool, Optional[Dict], str]:
#     try:
#         if not request.is_json:
#             content_type = request.content_type or 'unknown'
#             return False, None, f"Request must be JSON. Received content-type: {content_type}"
        
#         data = request.get_json(force=True, silent=False)
        
#         if data is None:
#             return False, None, "No JSON data provided or invalid JSON format"
        
#         if not isinstance(data, dict):
#             return False, None, "JSON data must be an object"
        
#         email = data.get('email', '').strip() if data.get('email') else ''
#         password = data.get('password', '').strip() if data.get('password') else ''
        
#         if not email:
#             return False, None, "Email is required"
#         if '@' not in email or '.' not in email:
#             return False, None, "Invalid email format"
#         if not password:
#             return False, None, "Password is required"
        
#         return True, {
#             'email': email,
#             'password': password
#         }, "Data parsed successfully"
#     except json.JSONDecodeError as e:
#         return False, None, f"Invalid JSON format: {str(e)}"
#     except Exception as e:
#         print(f"Error parsing login JSON: {e}")
#         import traceback
#         traceback.print_exc()
#         return False, None, f"Error parsing request data: {str(e)}"

# def create_user_from_json(mysql: MySQL) -> Tuple[bool, Optional[Dict], str]:
#     parse_success, user_data, parse_message = parse_signup_json()
#     if not parse_success:
#         return False, None, parse_message
    
#     first_name = user_data['first_name']
#     last_name = user_data['last_name']
#     email = user_data['email']
#     password = user_data['password']
    
#     success, message = create_user(mysql, first_name, last_name, email, password)
    
#     if success:
#         user = get_user_by_email(mysql, email)
#         if user:
#             user_safe = {k: v for k, v in user.items() if k != 'password'}
#             return True, user_safe, message
#         return True, None, message
    
#     return False, None, message

# def create_user(mysql: MySQL, first_name: str, last_name: str, email: str, password: str) -> Tuple[bool, str]:
#     try:
#         existing_user = get_user_by_email(mysql, email)
#         if existing_user:
#             return False, "Email already in use. Please choose another one."
        
#         hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
#         with mysql.connection.cursor() as cur:
#             cur.execute(
#                 "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
#                 (first_name.strip(), last_name.strip(), email.strip(), hashed_password)
#             )
#             mysql.connection.commit()
            
#         return True, "User created successfully"
        
#     except MySQLdb.Error as e:
#         print(f"MySQL Error in create_user: {e}")
#         mysql.connection.rollback()
#         return False, "Database error occurred while creating account"
#     except Exception as e:
#         print(f"Unexpected Error in create_user: {e}")
#         mysql.connection.rollback()
#         return False, "An error occurred while trying to sign you up. Please try again later."

# def authenticate_user_from_json(mysql: MySQL) -> Tuple[bool, Optional[Dict], str]:
#     parse_success, login_data, parse_message = parse_login_json()
#     if not parse_success:
#         return False, None, parse_message
    
#     email = login_data['email']
#     password = login_data['password']
    
#     return authenticate_user(mysql, email, password)

# def authenticate_user(mysql: MySQL, email: str, password: str) -> Tuple[bool, Optional[Dict], str]:
#     if not email or not password:
#         return False, None, "Please fill in both email and password"
    
#     user = get_user_by_email(mysql, email)
    
#     if not user:
#         return False, None, "No account found with this email address"
    
#     if not verify_password(user['password'], password):
#         return False, None, "Incorrect password"
    
#     user_safe = {k: v for k, v in user.items() if k != 'password'}
#     return True, user_safe, "Login successful"

# def get_user_by_id(mysql: MySQL, user_id: int) -> Optional[Dict]:
#     try:
#         with mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cur:
#             cur.execute('SELECT id, first_name, last_name, email FROM users WHERE id = %s', (user_id,))
#             user = cur.fetchone()
#             return user
#     except MySQLdb.Error as e:
#         print(f"MySQL Error in get_user_by_id: {e}")
#         return None
#     except Exception as e:
#         print(f"Unexpected Error in get_user_by_id: {e}")
#         return None

# def update_user(mysql: MySQL, user_id: int, **kwargs) -> Tuple[bool, str]:
#     try:
#         allowed_fields = ['first_name', 'last_name', 'email']
#         updates = []
#         values = []
        
#         for field, value in kwargs.items():
#             if field in allowed_fields:
#                 updates.append(f"{field} = %s")
#                 values.append(value.strip() if isinstance(value, str) else value)
        
#         if not updates:
#             return False, "No valid fields to update"
        
#         if 'password' in kwargs:
#             updates.append("password = %s")
#             values.append(generate_password_hash(kwargs['password'], method='pbkdf2:sha256'))
        
#         values.append(user_id)
        
#         with mysql.connection.cursor() as cur:
#             query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
#             cur.execute(query, values)
#             mysql.connection.commit()
            
#         return True, "User updated successfully"
        
#     except MySQLdb.Error as e:
#         print(f"MySQL Error in update_user: {e}")
#         mysql.connection.rollback()
#         return False, "Database error occurred"
#     except Exception as e:
#         print(f"Unexpected Error in update_user: {e}")
#         mysql.connection.rollback()
#         return False, "An error occurred while updating user"

# def delete_user(mysql: MySQL, user_id: int) -> Tuple[bool, str]:
#     try:
#         with mysql.connection.cursor() as cur:
#             cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
#             mysql.connection.commit()
            
#         return True, "User deleted successfully"
        
#     except MySQLdb.Error as e:
#         print(f"MySQL Error in delete_user: {e}")
#         mysql.connection.rollback()
#         return False, "Database error occurred"
#     except Exception as e:
#         print(f"Unexpected Error in delete_user: {e}")
#         mysql.connection.rollback()
#         return False, "An error occurred while deleting user"

# def execute_query(mysql: MySQL, query: str, params: tuple = None) -> Optional[list]:
#     try:
#         with mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cur:
#             if params:
#                 cur.execute(query, params)
#             else:
#                 cur.execute(query)
#             results = cur.fetchall()
#             return results
#     except MySQLdb.Error as e:
#         print(f"MySQL Error in execute_query: {e}")
#         return None
#     except Exception as e:
#         print(f"Unexpected Error in execute_query: {e}")
#         return None

# def execute_update(mysql: MySQL, query: str, params: tuple = None) -> Tuple[bool, str]:
#     try:
#         with mysql.connection.cursor() as cur:
#             if params:
#                 cur.execute(query, params)
#             else:
#                 cur.execute(query)
#             mysql.connection.commit()
#             return True, "Query executed successfully"
#     except MySQLdb.Error as e:
#         print(f"MySQL Error in execute_update: {e}")
#         mysql.connection.rollback()
#         return False, f"Database error: {str(e)}"
#     except Exception as e:
#         print(f"Unexpected Error in execute_update: {e}")
#         mysql.connection.rollback()
#         return False, f"Error: {str(e)}"
