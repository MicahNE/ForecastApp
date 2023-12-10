import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import AccessControl
import main

class Register:
    def __init__(self):
        # we will delete pass when adding the actual code
        pass

    def new_username_input(self, new_username):
        # new username logic
        pass

    def new_password_input(self, new_password):
        # new password input logic
        pass

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

        # Perform account creation logic (add salt, hash password, store in database, etc.)
        # Example: Assume you have a function in AccessControl.py to handle account creation

        if self.username_exists(username):
            QMessageBox.warning(self, "Username Exists", "Username already exists. Please choose a different username.")
            return

        else:
            success = AccessControl.create_user(username, password)

        if success:
            print("Account created successfully!")
            self.accept()  # Close the create account dialog
        else:
            print("Account creation failed. Handle the error as needed.")

    @staticmethod
    def username_exists(username):
        query = QSqlQuery()
        query.prepare("SELECT user_id FROM User WHERE username = :username")
        query.bindValue(":username", username)

        if query.exec_() and query.next():
            # If a record is found, the username already exists
            return True

    
    def show_login_dialog(self):
        # Close the create account dialog
        self.close()

        # Show the login dialog
        login_dialog = AccessControl.LoginDialog()
        login_dialog.exec_()

# Example usage:
# if __name__ == "__main__":
#     register_instance = Register()

#     # Example calls
#     register_instance.new_username_input("new_example_username")
#     register_instance.new_password_input("new_example_password")
