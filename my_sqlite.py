# telegram_id, full_name
import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

def create_users():
    command = """CREATE TABLE IF NOT EXISTS USERS (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE,
    full_name VARCHAR(30)
    )"""
    cursor.execute(command)
    connection.commit()

def add_user(telegram_id,full_name):
    command = f"""INSERT INTO USERS (telegram_id,full_name) 
    VALUES ({telegram_id},"{full_name}")"""
    cursor.execute(command)
    connection.commit()  

def count_users():
    command = """SELECT count(*) FROM USERS"""
    cursor.execute(command)
    return cursor.fetchone()

def get_all_user_ids():
    command = """SELECT telegram_id FROM USERS"""
    cursor.execute(command)
    return cursor.fetchall()