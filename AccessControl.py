import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import CalendarClass
import main
import secrets
import hashlib

class AccessControl:
    user_id = None
         
        
    def authenticate_user(self, username, password):
        # Retrieve user data from the database based on the entered username
        user_data = AccessControl.retrieve_user_data(self, username)

        if user_data:
            stored_salt = user_data['salt']
            stored_hashed_password = user_data['hashed_password']
            user_id = user_data['user_id']
            # Hash the entered password with the stored salt
            entered_password_hashed = PasswordHandler.hash_password(password, stored_salt)

            # Verify the entered password hash against the stored hash
            if entered_password_hashed == stored_hashed_password:
                AccessControl.user_id = user_id
                return True  # Authentication successful

        return False  # Authentication failed
    
    @classmethod
    def get_current_user_id(self):
        return self.user_id
    
    def retrieve_user_data(self, username):
        # Retrieve user data from the database based on the entered username

        # Open the database connection (make sure to handle exceptions)
        forecastDB = QSqlDatabase.database()

        if not forecastDB.isOpen():
            print("Database is not open. Cannot retrieve user data.")
            return None

        # Prepare and execute the query
        query = QSqlQuery()
        query.prepare("SELECT * FROM User WHERE username = :username")
        query.bindValue(":username", username)

        if not query.exec_():
            print("Error executing query:", query.lastError().text())
            return None

        # Fetch the result (assuming there is only one matching user)
        if query.next():
            user_data = {
                'user_id': query.value('user_id'),
                'salt': query.value('salt'),
                'hashed_password': query.value('hashed_password')
            }
            return user_data

        if query.next():
            user_data = {
                'user_id': query.value('user_id'),
                'salt': query.value('salt'),
                'hashed_password': query.value('hashed_password')
            }
            return user_data

        return None  # User not found
    
    def __init__(self):
        # any class specific variables
        pass # we will delete this once we add actual code so get rid of all 'pass'

    def logged_in(self, is_valid):
        #  are you logged in?
        pass

    def get_username(self, input_string):
        # user getting a username
        pass

    def get_password(self, input_string):
        # user getting a password
        pass

    def is_logged_in(self):
        # user logging in code
        pass

class LoginDialog(QDialog):
        def __init__(self):
            super(LoginDialog, self).__init__()
            main.loadUi("login.ui", self)
            self.init_ui()

        def init_ui(self):
            self.loginButton.clicked.connect(self.authenticate)
            self.createAccountLoginPageButton.clicked.connect(self.show_create_account_dialog)

        

        def show_create_account_dialog(self):
            self.close()
            create_account_dialog = CreateAccountDialog()
            create_account_dialog.exec_()  # Show the create account dialog
            
        def show_success_message(self, message):
            QMessageBox.information(self, "Success", message)
            
        def authenticate(self):
            username = self.userNameLineEdit.text()
            password = self.passwordLineEdit.text()

            # Use AccessControl to authenticate the user
            authenticated = AccessControl.authenticate_user(self, username, password)

            if authenticated:
                print("User authenticated successfully!")
                self.accept()  # Close the login dialog
            else:
                print("Authentication failed. Invalid username or password.")

            
        

class CreateAccountDialog(QDialog):
    def __init__(self):
        super(CreateAccountDialog, self).__init__()
        loadUi("createaccount.ui", self)
        self.init_ui()

    def init_ui(self):
        self.createAccountButton.clicked.connect(self.create_account)
        self.backToLoginPageButton.clicked.connect(self.show_login_dialog)

    def create_account(self):
        username = self.createUserNameLineEdit.text()
        password = self.createPasswordLineEdit.text()
        

        
        success = PasswordHandler.create_user(self, username, password)

        if success:
            print("Account created successfully!")
            self.close()

            # Show the login dialog with a success message
            login_dialog = LoginDialog()
            login_dialog.show_success_message("Account created successfully!")
            login_dialog.exec_()
        else:
            print("Account creation failed. Handle the error as needed.")
            
    

    def show_login_dialog(self):
        # Close the create account dialog
        self.close()

        # Show the login dialog
        login_dialog = LoginDialog()
        login_dialog.exec_()
    
    
class PasswordHandler:
    @staticmethod
    def generate_salt():
        # """Generate a random salt.
        return secrets.token_hex(16)  # 16 bytes, 32 characters

    @staticmethod
    def hash_password(password, salt):
        # Hash the password with the provided salt.
        # Combine password and salt before hashing
        combined_data = password.encode('utf-8') + salt.encode('utf-8')

        # Use a secure hash function (e.g., SHA-256)
        hashed_password = hashlib.sha256(combined_data).hexdigest()
        return hashed_password

    def create_user(self, username, password):
        # Create a new user and hash their password.
        

        salt = PasswordHandler.generate_salt()
        hashed_password = PasswordHandler.hash_password(password, salt)
      

        # Open the database connection
        

        # Prepare and execute the query
        insertUserQuery = QSqlQuery()
        insertUserQuery.prepare(
            """
            INSERT INTO User (username, hashed_password, salt)
            VALUES (:username, :hashed_password, :salt)
            """
        )
        insertUserQuery.bindValue(":username", username)
        insertUserQuery.bindValue(":hashed_password", hashed_password)
        insertUserQuery.bindValue(":salt", salt)

        # Execute the query
        if insertUserQuery.exec_():
            print("User inserted successfully")
        else:
            print("Error inserting user:", insertUserQuery.lastError().text())

        return {
            'username': username,
            'salt': salt,
            'hashed_password': hashed_password
        }


    def verify_password(self, entered_password, stored_salt, stored_hashed_password):
        """Verify a password during login."""
        entered_password_hashed = self.hash_password(entered_password, stored_salt)
        return entered_password_hashed == stored_hashed_password
    
    
    
    
    
    
    
    
    
    
    
    


# Example usage:
# if __name__ == "__main__":
#     access_control_instance = AccessControl()

#     # Example calls
#     validity = access_control_instance.is_valid()
#     username = access_control_instance.get_username("example_input")
#     password = access_control_instance.get_password("example_input")
#     logged_in = access_control_instance.is_logged_in()
