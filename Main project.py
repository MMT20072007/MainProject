# Required libraries
import sqlite3
import datetime
import string
import random

# Different functions 

# Generate unique id for user
def generate_user_id():
  return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Register user
def register_user(conn):
  name = input("Please enter your name: ")
  user_id = generate_user_id()

  signup_date = datetime.date.today()

  conn.execute('''INSERT INTO users (id, name, signup_date) 
         VALUES (?, ?, ?)''', (user_id, name, signup_date))
  conn.commit()

  print("User registered successfully. Your ID is:", user_id)

# Lend book
def lend_book(conn, user_id):
  book_id = input("Enter book ID: ")

  # Check if book exists
  if not book_exists(conn, book_id):
    print("Invalid book ID")
    return

  # Check if user is valid
  if not valid_user(conn, user_id):
    print("Invalid user ID")
    return

  loan_date = datetime.date.today()
  due_date = loan_date + datetime.timedelta(weeks=2)

  conn.execute('''INSERT INTO loans (user_id, book_id, loan_date, due_date)
       VALUES (?, ?, ?, ?)''',
               (user_id, book_id, loan_date, due_date))
  conn.commit()

  print("Book loaned successfully. Please return by", due_date)

# Check if book exists
def book_exists(conn, book_id):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
  return cursor.fetchone() is not None

# Check if user is valid
def valid_user(conn, user_id):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
  return cursor.fetchone() is not None

# Main function
def main():
  conn = sqlite3.connect('library.db')

  conn.execute('''CREATE TABLE IF NOT EXISTS users
           (id TEXT PRIMARY KEY     NOT NULL,
           name           TEXT    NOT NULL,
           signup_date    DATE     NOT NULL);''')

  conn.execute('''CREATE TABLE IF NOT EXISTS books
           (id TEXT PRIMARY KEY     NOT NULL,  
           title          TEXT    NOT NULL,
           author         TEXT    NOT NULL);''')

  conn.execute('''CREATE TABLE IF NOT EXISTS loans
           (user_id        TEXT    NOT NULL,
           book_id        TEXT    NOT NULL,
           loan_date      DATE    NOT NULL,
           due_date DATE NOT NULL);''')
  
  register_user(conn)

if __name__ == '__main__':
  main()