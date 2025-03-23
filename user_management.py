import sqlite3 as sql
import time
import random
import hashlib
import uuid


def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    salt, hashed_password = hashPassword(password)
    cur.execute(
        "INSERT INTO users (username, salt, password, dateOfBirth) VALUES (?,?,?,?)",
        (username, salt, hashed_password, DoB),
    )
    con.commit()
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
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
    
# ! used for hashing passwords
def hashPassword(password):
    salt = uuid.uuid4().hex 
    encoded_password = (password + salt).encode('utf-8') 
    hashed_password = hashlib.sha512(encoded_password).hexdigest()
    return salt, hashed_password
