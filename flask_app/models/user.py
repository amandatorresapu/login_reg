from flask import flash
import re
import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls,data):
        hash_yellow = bcrypt.generate_password_hash(data['password'])
        hashed_dict = {
            "username": data["username"],
            "email": data["email"],
            "password": hash_yellow
        }
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        return connectToMySQL("login_reg.db").query_db(query,hashed_dict)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_reg.db").query_db(query, data)
        if result: 
            return cls(result[0])

    @staticmethod
    def login_validator(data):
        user = User.get_by_email(data)

        if not user:
            return False
        
        if not bcrypt.check_password_hash(user.password, data["password"]):
            return False

        return True

    @staticmethod
    def registry_validator(data):
        is_valid = True

        if len(data["username"]) <= 1:
            flash("username must be at least 2 characters!!")
            is_valid = False

            user = User.get_by_email(data)
        if user:
            flash("email already in use")
            is_valid = False


        if len(data["email"]) <= 3:
            flash("Emails must be at least 4 characters long!")

        if len(data["password"]) <= 7:
            flash("Password must be 8 charaters or more")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Password and confirm must match")
            is_valid = False

        return is_valid
