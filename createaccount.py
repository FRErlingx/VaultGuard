import mysql.connector
from config import DB_CONFIG

def signup():
    try:
        # Connexion à la base de données avec les paramètres sécurisés
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        while len(password) < 10:
            print("Password must be at least 10 characters long.")
            password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
        while confirm_password != password:
            print("Password don't match")
            confirm_password = input("Confirm your password: ")
        
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, password)
        cursor.execute(sql, values)
        db.commit()
        
        user_id = cursor.lastrowid
        print(f"Signup successful! Your user ID is: {user_id}")
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()