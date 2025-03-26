import sqlite3 as sql
import time
import random
import hashlib
import uuid
import sqlite3  

# ! prevents race condtions by checking the database, if a race condition occurs it returns false
def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    salt, hashed_password = hashPassword(password)

    try:
        cur.execute("BEGIN TRANSACTION;")
        
        cur.execute(
            "INSERT INTO users (username, salt, password, dateOfBirth) VALUES (?, ?, ?, ?)",
            (username, salt, hashed_password, DoB),
        )

        con.commit()  
        return True 

    except sql.IntegrityError:
        con.rollback()
        return False 

    except Exception as e: 
        con.rollback()
        return False

    finally:
        con.close()


# ! finds the hash and its salt stored for username and compares the new password + salt with the hash
def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    cur.execute("SELECT salt, password FROM users WHERE username = ?", (username,))
    result = cur.fetchone()

    if result is None:
        con.close()
        return False  

    stored_salt, stored_hash = result
    
    encoded_password = (password + stored_salt).encode('utf-8')
    hashed_password = hashlib.sha512(encoded_password).hexdigest()

    con.close()
    return hashed_password == stored_hash 



def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,))
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    return data

# ! used for hashing passwords
def hashPassword(password):
    salt = uuid.uuid4().hex 
    encoded_password = (password + salt).encode('utf-8') 
    hashed_password = hashlib.sha512(encoded_password).hexdigest()
    return salt, hashed_password


def checkUserExists(username):
    try:
        with sqlite3.connect('database_files/database.db') as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            result = cursor.fetchone()  # Fetch the first result (if any)
            return result is not None  # Return True if a result is found, else False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
