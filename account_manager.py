import mysql.connector
from config import DB_CONFIG
import bcrypt
from getpass import getpass

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
        
        # Hash the password with bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, hashed_password)
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

def login():
    try:
        # Connexion à la base de données
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        username = input("Entrez votre nom d'utilisateur: ")
        password = getpass("Entrez votre mot de passe (celui-ci est invisible): ")
        
        # Recherche de l'utilisateur dans la base de données
        sql = "SELECT id, password FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        
        if result:
            user_id, hashed_password = result
            # Vérification du mot de passe
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                print("Connexion réussie!")
                return user_id
            else:
                print("Mot de passe incorrect.")
                return None
        else:
            print("Utilisateur non trouvé.")
            return None
            
    except mysql.connector.Error as err:
        print(f"Erreur de base de données: {err}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()