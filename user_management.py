import sqlite3 as sql
import time
import random
import hashlib
import uuid

# * inserts the user information from the signup page
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

# * retireves the user password and compares the entered one to the current one, returns true if they are the same
# ! Since the password is hashed, it retrieves its salt and hashed password and does a hashed comparison to check
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


# * inserts feedback into the feedback database
# ! feedback is entered in a SQL-injection safe way
def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,))
    con.commit()
    con.close()

# * lists the feedback from the database and returns it
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

# ! purely just checks if a username exists, returns false if it doesn't exist
def checkUserExists(username):
    try:
        with sql.connect('database_files/database.db') as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            result = cursor.fetchone()  
            return result is not None  
    except sql.Error as e:
        return False
    except Exception as e:
        return False
